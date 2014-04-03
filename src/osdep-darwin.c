#include "config.h"

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <libproc.h>

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

  struct proc_taskinfo tinfo;
  memset (&tinfo, 0, sizeof (tinfo));
  int nb = proc_pidinfo (ipid, PROC_PIDTASKINFO, 0,  &tinfo, sizeof (tinfo));
  if (nb <= 0)
    return;
  else if ((size_t) nb < sizeof (tinfo))
    return;

  stats->memory = tinfo.pti_resident_size / 1024;
  stats->nthreads = tinfo.pti_threadnum;
  strncpy (stats->status, "running", sizeof (stats->status));
}
