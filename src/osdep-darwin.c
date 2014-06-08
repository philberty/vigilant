#include "config.h"

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <libproc.h>

#include "watchy.h"

void watchy_getStats (struct watchy_metric * const stats, const pid_t ipid)
{
  stats->cpid = ipid;

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

void watchy_getHostStats (struct watchy_metric * const stats)
{
  // TODO
  ;
}
