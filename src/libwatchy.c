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
#include <signal.h>

#ifndef nitems
# define nitems(_a) (sizeof((_a)) / sizeof((_a)[0]))
#endif

static bool running = false;
static const char * watchy_error_strings [] = {
  [WTCY_NO_ERROR]   = "no error",
  [WTCY_NEXIST_PID] = "specified pid does not exist",
  [WTCY_FORK_FAIL]  = "fork of runtime has failed",
  [WTCY_SOCK_FAIL]  = "create socket failed see errno",
  [WTCY_IS_RUNNING] = "watch me is already running",
  [WTCY_PACKET_ERR] = "Error converting to json",
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

inline int
watchy_logPacket (struct watchy_data * const data, const char * message, const char * key)
{
  data->T = LOG;
  strncpy (data->key, key, sizeof (data->key));
  watchy_setTimeStamp (data->tsp, sizeof (data->tsp));
  memset (data->value.buffer, 0, sizeof (data->value.buffer));
  return snprintf (data->value.buffer, sizeof (data->value.buffer) - 1, "%s", message);
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

  if (stats->T == METRIC || stats->T == HOST)
    {
      if (stats->T == METRIC)
	strncpy (type, "metric", sizeof (type));
      else
	strncpy (type, "host", sizeof (type));
      return snprintf (buffer, blen, "{ "
		       "\"type\" : \"%s\", "
		       "\"name\" : \"%s\", "
		       "\"timeStamp\" : \"%s\", "
		       "\"state\" : \"%s\", "
		       "\"pid\" : %i, "
		       "\"threads\" : %zi, "
		       "\"memory\" : %i"
		       " }", type,
		       stats->key, stats->tsp,
		       stats->value.metric.status,
		       stats->value.metric.cpid,
		       stats->value.metric.nthreads,
		       stats->value.metric.memory);
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

int
watchy_watchme (const char * name, const char * bind, const int port)
{
  if (running)
    return WTCY_IS_RUNNING;
  running = true;

  int sockfd;
  struct sockaddr_in servaddr;
  memset (&servaddr, 0, sizeof (servaddr));

  int retval = watchy_socket (bind, port, &sockfd, &servaddr);
  if (retval != WTCY_NO_ERROR)
    return retval;

  pid_t cpid = fork ();
  switch (cpid)
    {
    case -1:
      return WTCY_FORK_FAIL;

    case 0:
      // turn the caller into the child and watch it!
      return WTCY_NO_ERROR;

    default:
      {
	setsid ();
	umask (022);
      }
      break;
    }

  sleep (1);
  int status = 0;
  while (waitpid (cpid, &status, WNOHANG) != -1)
    {
      struct watchy_data stats;
      memset (&stats, 0, sizeof (stats));

      stats.T = METRIC;
      strncpy (stats.key, name, sizeof (stats.key));
      watchy_setTimeStamp (stats.tsp, sizeof (stats.tsp));

      watchy_getStats (&stats.value.metric, cpid);

      char buffer [WTCY_PACKET_SIZE];
      memset (buffer, 0, sizeof (buffer));
      watchy_statsToJson (&stats, WTCY_PACKET_SIZE, buffer);
      sendto (sockfd, buffer, WTCY_PACKET_SIZE, 0,
	      (const struct sockaddr *) &servaddr, sizeof (servaddr));

      sleep (1);
    }
  close (sockfd);

  // exit with the same code as the child to preserve correct $?
  exit (status);

  // just to stop the warning and correctness
  return WTCY_NO_ERROR;
}

/**
 * Calls to this will block until the pid to watch is finished
 **/
int
watchy_watchpid (const char * name, const char * bind, const int port, const pid_t iproc)
{
  // check if pid exsits
  int rkill = kill (iproc, 0);
  if (rkill != 0)
    return WTCY_NEXIST_PID;

  int sockfd;
  struct sockaddr_in servaddr;
  memset (&servaddr, 0, sizeof (servaddr));

  int retval = watchy_socket (bind, port, &sockfd, &servaddr);
  if (retval != WTCY_NO_ERROR)
    return retval;

  // kind of inefficient would be nice to use libevent here if poss
  // or look for some more efficient interface
  while (!(rkill = kill (iproc, 0)))
    {
      struct watchy_data stats;
      memset (&stats, 0, sizeof (stats));

      stats.T = METRIC;
      strncpy (stats.key, name, sizeof (stats.key));
      watchy_setTimeStamp (stats.tsp, sizeof (stats.tsp));

      watchy_getStats (&stats.value.metric, iproc);

      char buffer [WTCY_PACKET_SIZE];
      memset (buffer, 0, sizeof (buffer));
      watchy_statsToJson (&stats, WTCY_PACKET_SIZE, buffer);
      sendto (sockfd, buffer, WTCY_PACKET_SIZE, 0,
	      (const struct sockaddr *) &servaddr, sizeof (servaddr));

      sleep (1);
    }
  close (sockfd);

  return WTCY_NO_ERROR;
}

/* This blocks */
int
watchy_watchHost (const char * name, const char * bind, const int port)
{
  int sockfd;
  struct sockaddr_in servaddr;
  memset (&servaddr, 0, sizeof (servaddr));

  int retval = watchy_socket (bind, port, &sockfd, &servaddr);
  if (retval != WTCY_NO_ERROR)
    return retval;

  while (true)
    {
      struct watchy_data stats;
      memset (&stats, 0, sizeof (stats));

      stats.T = HOST;
      strncpy (stats.key, name, sizeof (stats.key));
      watchy_setTimeStamp (stats.tsp, sizeof (stats.tsp));

      watchy_getHostStats (&stats.value.metric);

      char buffer [WTCY_PACKET_SIZE];
      memset (buffer, 0, sizeof (buffer));
      watchy_statsToJson (&stats, WTCY_PACKET_SIZE, buffer);
      sendto (sockfd, buffer, WTCY_PACKET_SIZE, 0,
	      (const struct sockaddr *) &servaddr, sizeof (servaddr));

      sleep (1);
    }
  close (sockfd);
  return WTCY_NO_ERROR;
}
