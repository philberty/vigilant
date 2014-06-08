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
#include <netdb.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>

#ifndef nitems
# define nitems(_a) (sizeof((_a)) / sizeof((_a)[0]))
#endif

static const char * watchy_error_strings [] = {
  [WTCY_NO_ERROR]   = "no error",
  [WTCY_NEXIST_PID] = "specified pid does not exist",
  [WTCY_FORK_FAIL]  = "fork of runtime has failed",
  [WTCY_SOCK_FAIL]  = "create socket failed see errno",
  [WTCY_IS_RUNNING] = "watch me is already running",
  [WTCY_PACKET_ERR] = "Error converting to json",
  [WTCY_DAEMON_ERR] = "Error forking daemon watchy",
  [WTCY_USOCK_FAIL] = "Error connecting to unix socket",
  [WTCY_ATIMEOUT]   = "Error timeout waiting for server",
  [WTCY_UNKNOWN]    = "unknown error code",
};

inline int
watchy_setTimeStamp (char * const buffer, const size_t len)
{
  time_t ltime = time (NULL);
  struct tm *tm;
  tm = localtime (&ltime);

  return snprintf (buffer, len,"%04d%02d%02d%02d%02d%02d",
		   tm->tm_year+1900, tm->tm_mon, tm->tm_mday,
		   tm->tm_hour, tm->tm_min, tm->tm_sec);
}

/* Utility trim function */
char *
watchy_trim (const char * buffer, const size_t len)
{
  char * rbuf = calloc (sizeof (char), len + 1);

  size_t s, e;
  for (s = 0; s < len; ++s)
    if (isgraph (buffer [s]))
      break;

  for (e = len - 1; e < len; --e)
    if (isgraph (buffer [e]))
      break;

  strncpy (rbuf, buffer + s, e - s + 1);
  return rbuf;
}

void
watchy_logPacket (struct watchy_data * const data, const char * message, const char * key)
{
  data->T = LOG;
  strncpy (data->key, key, sizeof (data->key));
  watchy_setTimeStamp (data->tsp, sizeof (data->tsp));
  memset (data->value.buffer, 0, sizeof (data->value.buffer));

  char buffer [sizeof (data->value.buffer)];
  memset (buffer, 0, sizeof (buffer));

  size_t ncpy = (strlen (message) >= sizeof (buffer)) ? sizeof (buffer) - 1 : strlen (message) - 1;
  if (message [ncpy] == '\n')
    ncpy -= 1;

  strncpy (buffer, message, ncpy);
  strncpy (data->value.buffer, buffer, sizeof (buffer));
}

const char *
watchy_strerror (const int code)
{
  if ((code >= 0) && (code < nitems (watchy_error_strings) - 1))
    return watchy_error_strings [code];
  return watchy_error_strings [WTCY_UNKNOWN];
}

int
watchy_socket (const char * bind, const int port, int * const sockfd,
	       struct sockaddr_in * const servaddr)
{
  *sockfd = socket (AF_INET, SOCK_DGRAM, IPPROTO_UDP);
  if (*sockfd < 0)
    return WTCY_SOCK_FAIL;

  servaddr->sin_family = AF_INET;
  servaddr->sin_port = htons (port);
  // TODO ERROR CHECK
  inet_aton (bind, &servaddr->sin_addr);

  return WTCY_NO_ERROR;
}

/**
 * this is a dirty method but its handy for now and we only need a very simply json object
 **/
int
watchy_statsToJson (const struct watchy_data * const stats, const size_t blen, char * const buffer)
{
  char type [10];
  memset (type, 0, sizeof (type));

  if (stats->T == PROCESS || stats->T == HOST)
    {
      if (stats->T == PROCESS)
	strncpy (type, "process", sizeof (type));
      else
	strncpy (type, "host", sizeof (type));
      return snprintf (buffer, blen, "{ "
		       "\"type\" : \"%s\", "
		       "\"name\" : \"%s\", "
		       "\"timeStamp\" : \"%s\", "
		       "\"state\" : \"%s\", "
		       "\"pid\" : %i, "
		       "\"threads\" : %zi, "
		       "\"memory\" : %i, "
		       "\"usage\" : %Lf"
		       " }", type,
		       stats->key, stats->tsp,
		       stats->value.metric.status,
		       stats->value.metric.cpid,
		       stats->value.metric.nthreads,
		       stats->value.metric.memory,
		       stats->value.metric.usage);
    }
  else if (stats->T == LOG)
    {
      strncpy (type, "log", sizeof (type));
      return snprintf (buffer, blen, "{ "
		       "\"type\" : \"%s\", "
		       "\"name\" : \"%s\", "
		       "\"timeStamp\" : \"%s\", "
		       "\"message\" : \"%s\""
		       " }", type,
		       stats->key, stats->tsp,
		       stats->value.buffer);
    }
  return WTCY_PACKET_ERR;
}
