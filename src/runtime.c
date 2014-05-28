#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include "watchy.h"

static int setnonblock (int);
static void watchy_runtimeLoop (int, const int, const struct sockaddr_in *);

int
watchy_writePacketSync (struct watchy_data * const data, const int sockfd,
			const struct sockaddr_in * const servaddr)
{
  char buffer [WTCY_PACKET_SIZE];
  memset (buffer, 0, sizeof (buffer));
  watchy_setTimeStamp (data->tsp, sizeof (data->tsp));
  watchy_statsToJson (data, WTCY_PACKET_SIZE, buffer);
  return sendto (sockfd, buffer, WTCY_PACKET_SIZE, 0,
		 (const struct sockaddr *) servaddr, sizeof (servaddr));
}

int watchy_writePacket (struct watchy_data * const data, const int fd)
{
  return 0;
}

static int
setnonblock (int fd)
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

static void
watchy_runtimeLoop (int fd, const int sockfd, const struct sockaddr_in * servaddr)
{
  setnonblock (fd);

  fd_set inputs, read_fd_set;
  FD_ZERO (&inputs);
  FD_SET (fd, &inputs);

  while (1)
    {
      read_fd_set = inputs;
      select (FD_SETSIZE, &read_fd_set, NULL, NULL, NULL);
     
      sleep (1);
    }
}

int
watchy_cAttachRuntime (const char * fifo, const char * bind,
		       const int port, int * const fd)
{
  int sockfd;
  struct sockaddr_in servaddr;
  memset (&servaddr, 0, sizeof (servaddr));

  int retval = watchy_socket (bind, port, &sockfd, &servaddr);
  if (retval != WTCY_NO_ERROR)
    return retval;

  if (access (fifo, R_OK) == 0)
    *fd = open (fifo, O_RDONLY | O_NDELAY);
  else
    {
      mknod (fifo, S_IFIFO | 0666, 0);
      *fd = open (fifo, O_RDONLY | O_NDELAY);
      switch (fork ())
	{
	case -1:
	  return WTCY_DAEMON_ERR;

	case 0:
	  {
	    if (daemon (0, 0) != 0)
	      exit (1);
	    watchy_runtimeLoop (*fd, sockfd, &servaddr);
	    exit (0);
	  }
	  break;

	default:
	  break;
	}
    }
  return WTCY_NO_ERROR;
}

void
watchy_detachRuntime (void)
{
  return;
}
