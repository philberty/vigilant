#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include <ctype.h>
#include <time.h>
#include <limits.h>

#include "watchy.h"

void watchy_getStats (struct watchy_data * const stats, const pid_t ipid)
{
  stats->cpid = ipid;

  time_t ltime = time (NULL);
  struct tm *tm;
  tm = localtime (&ltime);

  snprintf (stats->tsp, sizeof (stats->tsp),"%04d%02d%02d%02d%02d%02d",
	    tm->tm_year+1900, tm->tm_mon, tm->tm_mday,
	    tm->tm_hour, tm->tm_min, tm->tm_sec);

  // looking up /proc/pid/status for these stats for now.
  char buf [PATH_MAX];
  memset (buf, 0, sizeof (buf));
  snprintf (buf, sizeof (buf), "/proc/%i/status", ipid);

  FILE * fd = fopen (buf, "r");
  if (fd == NULL)
    return;

  size_t len = 0;
  ssize_t read;
  char * line = NULL;
  while ((read = getline (&line, &len, fd)) != -1)
    {
      char key [len], value [len];
      memset (key, 0, sizeof (key));
      memset (value, 0, sizeof (value));

      size_t i;
      for (i = 0; i < len; ++i)
	{
	  if (line [i] == ':')
	    break;
	}
      strncpy (key, line, i);

      for (i += 1; i < len; ++i)
	{
	  if (isgraph (line [i]) && !isspace (line [i]))
	    break;
	}

      size_t vlen = len - i;
      strncpy (value, line + i, vlen);
      char * tval = watchy_trim (value, vlen);

      if (!strcmp (key, "State"))
	strncpy (stats->status, tval, sizeof (stats->status));
      else if (!strcmp (key, "Threads"))
	stats->nthreads = atoi (tval);
      else if (!strcmp (key, "VmSize"))
	stats->memory = atoi (tval);

      free (tval);
    }
  if (line)
    free (line);

  fclose (fd);
}
