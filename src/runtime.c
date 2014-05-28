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

static bool running;
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
	    watchy_writePacketSync (&data, sockfd, servaddr);
	}
      sleep (1);
    }
  closelog ();
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
    *fd = open (fifo, O_WRONLY | O_NDELAY);
  else
    {
      mknod (fifo, S_IFIFO | 0666, 0);
      switch (fork ())
	{
	case -1:
	  return WTCY_DAEMON_ERR;

	case 0:
	  {
	    int ffd = open (fifo, O_RDONLY);
	    if (daemon (0, 0) != 0)
	      exit (1);
	    watchy_runtimeLoop (ffd, sockfd, &servaddr);
	    close (ffd);
	    unlink (fifo);
	    exit (0);
	  }
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
}
