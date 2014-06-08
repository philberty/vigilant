#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <sys/un.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>
#include <errno.h>

#include <syslog.h>
#include <sys/queue.h>

#include <event2/event.h>
#include <event2/event_struct.h>
#include <event2/bufferevent.h>
#include <event2/buffer.h>

#include "watchy.h"

static void shandler (int);
static struct event_base *evbase;
static pid_t opener, spid;
static int sockfd;
static struct sockaddr_in servaddr;
static bool running = false;
static bool persist = false;
static bool watch_host = false;
static bool ready = false;
static char buffer [WTCY_PACKET_SIZE];
static struct timeval one_sec = { 1, 0 };
static char ** _ARGV0 = NULL;

#define _PROC_NAME "WatchyDaemon"

struct watchy_pid {
  pid_t pid;
  struct watchy_data node;
  struct event * ev;
  TAILQ_ENTRY(watchy_pid) entries;
};
TAILQ_HEAD(, watchy_pid) watchy_pids_head;

static void
shandler (int signo)
{
  switch (signo)
    {
    case SIGTERM:
      {
	syslog (LOG_INFO, "Caught sigterm!");
	event_base_loopbreak (evbase);
	running = false;
      }
      break;

    case SIGUSR1:
      ready = true;
      break;

    default:
      syslog (LOG_INFO, "Unhandled signal [%i]", signo);
      break;
    }
}

int
watchy_writePacketSync (struct watchy_data * const data, const int sockfd,
			const struct sockaddr_in * const servaddr)
{
  memset (buffer, 0, sizeof (buffer));
  watchy_statsToJson (data, WTCY_PACKET_SIZE, buffer);
  return sendto (sockfd, buffer, WTCY_PACKET_SIZE, 0,
		 (const struct sockaddr *) servaddr, sizeof (struct sockaddr_in));
}

int watchy_writePacket (struct watchy_data * const data, const int fd)
{
  return send (fd, data, sizeof (struct watchy_data), 0);
}

int setnonblock (int fd)
{
  int flags;

  flags = fcntl (fd, F_GETFL);
  if (flags < 0)
    return flags;

  flags |= O_NONBLOCK;
  if (fcntl (fd, F_SETFL, flags) < 0)
    return -1;

  return 0;
}

void callback_doStats (int fd, short event, void * arg)
{
  struct watchy_pid * node = arg;
  syslog (LOG_INFO, "Watch pid [%i]", node->pid);

  if (kill (node->pid, 0) == -1)
    {
      syslog (LOG_INFO, "pid [%i] is no longer alive", node->pid);
      struct watchy_pid * item, * tmp_item;
      for (item = TAILQ_FIRST (&watchy_pids_head); item != NULL; item = tmp_item)
	{
	  tmp_item = TAILQ_NEXT (item, entries);
	  if (item->pid == node->pid)
	    {
	      TAILQ_REMOVE (&watchy_pids_head, item, entries);
	      event_del (item->ev);
	      free (item);
	    }
	}
    }
  else
    { 
      struct watchy_data data;
      memset (&data, 0, sizeof (data));

      data.T = PROCESS;
      strncpy (data.key, node->node.key, sizeof (data.key));
      watchy_setTimeStamp (data.tsp, sizeof (data.tsp));
      watchy_getStats (&data.value.metric, node->pid);
      
      watchy_writePacketSync (&data, sockfd, &servaddr);
    }
}

void callback_doHostStats (int fd, short event, void * arg)
{
  struct watchy_pid * node = arg;
  struct watchy_data data;
  memset (&data, 0, sizeof (data));

  data.T = HOST;
  strncpy (data.key, node->node.key, sizeof (data.key));
  watchy_setTimeStamp (data.tsp, sizeof (data.tsp));
  watchy_getHostStats (&data.value.metric);
      
  watchy_writePacketSync (&data, sockfd, &servaddr);
}

void
callback_client_read (struct bufferevent *bev, void *arg)
{
  struct watchy_data data;
  memset (&data, 0, sizeof (data));

  int c = bufferevent_read (bev, &data, sizeof (data));
  if (c >= 0)
    {
      switch (data.T)
	{
	  // shutdown message
	case SDOWN:
	  {
	    if (persist == false)
	      {
		syslog (LOG_INFO, "Shutting down Daemon not told to persist on detach!");
		event_base_loopbreak (evbase);
		running = false;
	      }
	  }
	  break;

	case PERSIST:
	  persist = data.value.persist;
	  break;

	case INTERNAL:
	  {
	    struct watchy_pid * item;
	    pid_t ipid = data.value.intern.pid;
	    bool watch = data.value.intern.watch;
	    bool exists = false;

	    if (data.value.intern.host == true)
	      {
		if (watch_host)
		  return;
		watch_host = true;

		item = malloc (sizeof (struct watchy_pid));
		memset (item, 0, sizeof (struct watchy_pid));
		memcpy (&item->node, &data, sizeof (struct watchy_data));

	        item->ev = event_new (evbase, 0, EV_PERSIST, callback_doHostStats, item);
		evtimer_add (item->ev, &one_sec);
	      }
	    else
	      {
		struct watchy_pid * tmp_item;
		for (item = TAILQ_FIRST (&watchy_pids_head); item != NULL; item = tmp_item)
		  {
		    tmp_item = TAILQ_NEXT (item, entries);
		    if (item->pid == ipid)
		      {
			exists = true;
			if (watch == false)
			  {
			    TAILQ_REMOVE (&watchy_pids_head, item, entries);
			    event_del (item->ev);
			    free (item);
			  }
		      }
		  }
		if (!exists && (watch == true))
		  {
		    item = malloc (sizeof (struct watchy_pid));
		    memset (item, 0, sizeof (struct watchy_pid));

		    item->pid = ipid;
		    memcpy (&item->node, &data, sizeof (struct watchy_data));
		    TAILQ_INSERT_TAIL (&watchy_pids_head, item, entries);
		    
		    item->ev = event_new (evbase, 0, EV_PERSIST, callback_doStats, item);
		    evtimer_add (item->ev, &one_sec);
		  }
	      }
	  }
	  break;

	default:
	  watchy_writePacketSync (&data, sockfd, &servaddr);
	  break;
	}
    }
}

void callback_client_error (struct bufferevent *bev, short what, void *arg)
{
  bufferevent_free (bev);
  int *fd = (int *) arg;
  close (*fd);
}

void callback_client_connect (int fd, short ev, void *arg)
{
  struct sockaddr_in client_addr;
  socklen_t client_len = sizeof (client_addr);
  int client_fd = accept (fd, (struct sockaddr *)&client_addr,
			  &client_len);
  /* if (client_fd < 0) */
  /*   return; */

  struct bufferevent * bev = bufferevent_socket_new (evbase, client_fd, 0);
  bufferevent_setwatermark (bev, EV_READ, sizeof (struct watchy_data),
			    sizeof (struct watchy_data));
  bufferevent_setcb (bev,
		     &callback_client_read,  // read event
		     NULL,                   // write event
		     &callback_client_error, // on error
		     &client_fd);            // argument
  bufferevent_enable (bev, EV_READ);
}

static void
watchy_runtimeLoop (int fd)
{
  running = true;
  TAILQ_INIT (&watchy_pids_head);

  signal (SIGTERM, shandler);
  setlogmask (LOG_UPTO (LOG_INFO));
  openlog (_PROC_NAME, LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL1);
  syslog (LOG_NOTICE, "Watchy Daemon started by User %d", getuid ());

  evbase = event_base_new ();
  struct event ev_accept;
  event_assign (&ev_accept, evbase, fd,
		EV_READ | EV_PERSIST,
		&callback_client_connect,
		NULL);
  event_add (&ev_accept, NULL);

  while (running)
    event_base_loop (evbase, EVLOOP_NONBLOCK);

  syslog (LOG_NOTICE, "Watchy Daemon shutting down");
  event_base_free (evbase);
  closelog ();

  struct watchy_pid * item;
  while ((item = TAILQ_FIRST (&watchy_pids_head)))
    {
      TAILQ_REMOVE (&watchy_pids_head, item, entries);
      free (item);
    }
}

int
watchy_cAttachRuntime (const char * fifo, const char * host,
		       const int port, int * const fd, char ** const argv0)
{
  _ARGV0 = argv0;
  memset (&servaddr, 0, sizeof (servaddr));
  int ret = watchy_socket (host, port, &sockfd, &servaddr);
  if (ret != WTCY_NO_ERROR)
    return ret;

  struct sockaddr_un address;
  memset (&address, 0, sizeof (address));
  address.sun_family = AF_UNIX;
  strcpy (address.sun_path, fifo);

  if (access (fifo, R_OK) == 0)
    {
      *fd = socket (PF_UNIX, SOCK_STREAM, 0);
      int ret = connect (*fd, (struct sockaddr *) &address, sizeof(address));
      if (ret != 0)
	return WTCY_USOCK_FAIL;
    }
  else
    {
      opener = getpid ();
      switch ((spid = fork ()))
	{
	case -1:
	  return WTCY_DAEMON_ERR;

	case 0:
	  {
	    setsid ();
	    if (_ARGV0 != NULL)
	      {
		size_t len = strlen (*_ARGV0);
		memset (*_ARGV0, 0, len - 1);
		snprintf (*_ARGV0, len, "%s", _PROC_NAME);
	      }

	    int sfd = socket (AF_UNIX, SOCK_STREAM, 0);
	    setnonblock (sfd);

	    unlink (fifo);
	    bind (sfd, (struct sockaddr *) &address, sizeof (address));
	    listen (sfd, 1);

	    kill (getppid (), SIGUSR1);
	    watchy_runtimeLoop (sfd);

	    close (sfd);
	    unlink (fifo);
	    exit (0);
	  }
	  break;

	default:
	  {
	    signal (SIGUSR1, shandler);
	    *fd = socket (PF_UNIX, SOCK_STREAM, 0);

	    // timeout on 5 sleeps
	    size_t i;
	    for (i = 0; i < 5; ++i)
	      {
		if (ready)
		  break;
		sleep (1);
	      }
	    if (!ready)
	      return WTCY_ATIMEOUT;

	    int ret = connect (*fd, (struct sockaddr *) &address, sizeof(address));
	    if (ret != 0)
	      return WTCY_USOCK_FAIL;
	  }
	  break;
	}
    }
  return WTCY_NO_ERROR;
}

void
watchy_persistRuntime (int fd, bool persist)
{
  struct watchy_data data;
  memset (&data, 0, sizeof (data));

  data.T = PERSIST;
  data.value.persist = persist;

  watchy_writePacket (&data, fd);
}

void
watchy_detachRuntime (int fd)
{
  struct watchy_data data;
  memset (&data, 0, sizeof (data));
  data.T = SDOWN;

  watchy_writePacket (&data, fd);
  close (fd);
}
