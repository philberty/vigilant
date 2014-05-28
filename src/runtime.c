#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>

#include <syslog.h>

#include "watchy.h"

static void shandler           (int);
static void watchy_runtimeLoop (int, const int, const struct sockaddr_in * const);
static int  watchy_forkdaemon  (const char *, const int, const struct sockaddr_in * const);

static pid_t opener, spid;
static volatile bool running;
static char buffer [WTCY_PACKET_SIZE];

static void
shandler (int signo)
{
  syslog (LOG_INFO, "Caught sigterm stopping runtime!");
  running = false;
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

static void
watchy_runtimeLoop (int fd, const int sockfd,
		    const struct sockaddr_in * const servaddr)
{
  signal (SIGTERM, shandler);
  setlogmask (LOG_UPTO (LOG_INFO));
  openlog ("WatchyBus", LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL1);

  syslog (LOG_NOTICE, "Watchy Server started by User %d", getuid ());

  struct timeval timeout;
  timeout.tv_sec  = 10;
  timeout.tv_usec = 0;

  fd_set inputs;
  FD_ZERO (&inputs);
  FD_SET (fd, &inputs);

  running = true;
  while (running)
    {
      int n = select (fd + 1, &inputs, NULL, NULL, &timeout);
      if (n > 0)
	{
	  struct watchy_data data;
	  memset (&data, 0, sizeof (data));
	  int c = read (fd, &data, sizeof (data));
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
	      watchy_writePacketSync (&data, sockfd, servaddr);
	    }
	}
    }
  closelog ();
}

static int
watchy_forkdaemon (const char * fifo, const int sockfd,
		   const struct sockaddr_in * const servaddr)
{
  //unmask the file mode
  umask (0);
  //set new session
  setsid ();
  // Change the current working directory to root.
  chdir ("/");
  // Close stdin. stdout and stderr
  close (STDIN_FILENO);
  close (STDOUT_FILENO);
  close (STDERR_FILENO);

  int fd = open (fifo, O_RDONLY);
  watchy_runtimeLoop (fd, sockfd, servaddr);
  close (fd);
  unlink (fifo);

  return 0;
}

int
watchy_cAttachRuntime (const char * fifo, const char * bind,
		       const int port, int * const fd)
{
  int sockfd;
  struct sockaddr_in servaddr;
  memset (&servaddr, 0, sizeof (servaddr));
  int ret = watchy_socket (bind, port, &sockfd, &servaddr);
  if (ret != WTCY_NO_ERROR)
    return ret;

  if (access (fifo, R_OK) == 0)
    *fd = open (fifo, O_WRONLY);
  else
    {
      opener = getpid ();
      mknod (fifo, S_IFIFO | 0666, 0);
      switch ((spid = fork ()))
	{
	case -1:
	  return WTCY_DAEMON_ERR;

	case 0:
	  exit (watchy_forkdaemon (fifo, sockfd, &servaddr));
	  break;

	default:
	  *fd = open (fifo, O_WRONLY);
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
