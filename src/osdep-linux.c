#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include <ctype.h>
#include <time.h>
#include <limits.h>

#include "watchy.h"

void watchy_getStats (struct watchy_metric * const stats, const pid_t ipid)
{
  stats->cpid = ipid;

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

void watchy_getHostStats (struct watchy_metric * const stats)
{
  strncpy (stats->status, "running", sizeof (stats->status));

  FILE * fd = fopen ("/proc/meminfo", "rb");
  if (fd == NULL)
    return;

  size_t len = 0;
  ssize_t read;
  char * line = NULL;

  int total = 0, tfree = 0;
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
      
      if (!strcmp (key, "MemTotal"))
	total = atoi (tval);
      else if (!strcmp (key, "MemFree"))
	tfree = atoi (tval);

      free (tval);
    }
  if (line)
    free (line);
  fclose (fd);
  stats->memory = total - tfree;

  // gracefully stole from: http://stackoverflow.com/questions/3769405/determining-cpu-utilization
  long double a[4], b[4], loadavg;
  FILE *fp;

  fp = fopen("/proc/stat","r");
  if (fp == NULL)
    return;

  fscanf(fp,"%*s %Lf %Lf %Lf %Lf",&a[0],&a[1],&a[2],&a[3]);
  fclose(fp);

  sleep(1);

  fp = fopen("/proc/stat","r");
  if (fp == NULL)
    return;

  fscanf(fp,"%*s %Lf %Lf %Lf %Lf",&b[0],&b[1],&b[2],&b[3]);
  fclose(fp);

  loadavg = ((b[0]+b[1]+b[2]) - (a[0]+a[1]+a[2])) /
    ((b[0]+b[1]+b[2]+b[3]) - (a[0]+a[1]+a[2]+a[3]));
  stats->usage = (loadavg * 100);
}

