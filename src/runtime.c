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

#include <event2/event.h>
#include <event2/event_struct.h>
#include <event2/bufferevent.h>
#include <event2/buffer.h>

#include <syslog.h>

#include "watchy.h"

static void shandler (int);
static struct event_base *evbase;
static pid_t opener, spid;
static int sockfd;
static struct sockaddr_in servaddr;

static volatile bool running = false;
static volatile bool ready = false;
static char buffer [WTCY_PACKET_SIZE];

static void
shandler (int signo)
{
  switch (signo)
    {
    case SIGTERM:
      {
	syslog (LOG_INFO, "Caught sigterm stopping runtime!");
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
  return write (fd, data, sizeof (struct watchy_data));
}

int setnonblock (int fd)
{
  int flags;

  flags = fcntl (fd, F_GETFL);
  if (flags < 0)
    return flags;

  flags |= O_NONBLOCK;
  if (fcntl(fd, F_SETFL, flags) < 0)
    return -1;

  return 0;
}

void
callback_client_read (struct bufferevent *bev, void *arg)
{
  struct watchy_data data;
  memset (&data, 0, sizeof (data));

  int c = bufferevent_read (bev, &data, sizeof (data));
  if (c >= 0)
    {
      char type [12];
      memset (type, 0, sizeof (type));

      switch (data.T)
	{
	case METRIC:
	  strcpy (type, "metric");
	  break;

	case HOST:
	  strcpy (type, "host");
	  break;

	case PROCESS:
	  strcpy (type, "process");
	  break;

	case LOG:
	  strcpy (type, "log");
	  break;

	default:
	  strcpy (type, "unknown");
	  break;
	}
      syslog (LOG_INFO, "Got data packet [%s]", type);
      watchy_writePacketSync (&data, sockfd, &servaddr);
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
  int client_fd;
  struct sockaddr_in client_addr;
  socklen_t client_len = sizeof (client_addr);

  client_fd = accept (fd, (struct sockaddr *)&client_addr,
		      &client_len);
  if (client_fd < 0)
    return;

  setnonblock (client_fd);
  struct bufferevent * bev = bufferevent_socket_new (evbase, client_fd, 0);
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
  signal (SIGTERM, shandler);
  setlogmask (LOG_UPTO (LOG_INFO));
  openlog ("WatchyBus", LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL1);
  syslog (LOG_NOTICE, "Watchy Server started by User %d", getuid ());

  evbase = event_base_new ();
  struct event ev_accept;
  event_assign (&ev_accept, evbase, fd,
		EV_READ | EV_PERSIST,
		&callback_client_connect,
		NULL);

  event_add (&ev_accept, NULL);
  event_base_dispatch (evbase);
  closelog ();
}

int
watchy_cAttachRuntime (const char * fifo, const char * host,
		       const int port, int * const fd)
{
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
	    int sfd = socket (AF_UNIX, SOCK_STREAM, 0);
	    setnonblock (sfd);

	    unlink (fifo);
	    bind (sfd, (struct sockaddr *) &address, sizeof (address));
	    listen (sfd, 1);

	    kill (getppid (), SIGUSR1);
	    watchy_runtimeLoop (sfd);

	    close (sfd);
	    unlink (fifo);
	    remove (fifo);

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
watchy_detachRuntime (int fd)
{
  close (fd);
  if (getpid () == opener)
    kill (spid, SIGTERM);
}
