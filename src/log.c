#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

#include "watchy.h"

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>

int main (int argc, char **argv)
{  
  int sockfd;
  struct sockaddr_in servaddr;
  memset (&servaddr, 0, sizeof (servaddr));
  watchy_socket ("localhost", 7878, &sockfd, &servaddr);

  size_t i;
  for (i = 0; i < 5; ++i)
    {
      struct watchy_data stats;
      memset (&stats, 0, sizeof (stats));

      watchy_logPacket (&stats, "Hello World", "log1");

      char buffer [WTCY_PACKET_SIZE];
      memset (buffer, 0, sizeof (buffer));
      watchy_statsToJson (&stats, WTCY_PACKET_SIZE, buffer);
      sendto (sockfd, buffer, WTCY_PACKET_SIZE, 0,
	      (const struct sockaddr *) &servaddr, sizeof (servaddr));

      sleep (1);
    }
  close (sockfd);

  return 0;
}
