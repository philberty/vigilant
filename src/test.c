#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <assert.h>
#include <errno.h>

#include "watchy.h"

#define BIND "localhost"
#define PORT 7878

int main (int argc, char **argv)
{
  int sockfd;
  struct sockaddr_in servaddr;
  memset (&servaddr, 0, sizeof (servaddr));

  int ret = watchy_socket (BIND, PORT, &sockfd, &servaddr);
  if (ret != WTCY_NO_ERROR)
    {
      fprintf (stderr, "Error setting up socket [%i:%s]\n",
	       ret, watchy_strerror (ret));
      return -1;
    }

  struct watchy_data data;
  memset (&data, 0, sizeof (data));

  data.T = HOST;
  strncpy (data.key, "test", sizeof (data.key));
  watchy_setTimeStamp (data.tsp, sizeof (data.tsp));
  watchy_getHostStats (&data.value.metric);

  ret = watchy_writePacketSync (&data, sockfd, &servaddr);
  if (ret == -1)
    {
      fprintf (stderr, "errono = [%i][%s]\n", errno, strerror (errno));
      return -1;
    }

  return 0;
}
