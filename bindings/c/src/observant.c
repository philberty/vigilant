
#include <Python.h>

#include <libobservant.h>
#include <observant.h>

#include <sys/types.h>
#include <unistd.h>

int
obs_attach(const char *lock, const char *sock) 
{
  Py_Initialize();
  PyInit_libobservant();
  return obs_attach_to_stats_daemon(lock, sock);
}

int
obs_watch_me(const char *key)
{
  pid_t me = getpid();
  return obs_watch_pid(me, key);
}

void
obs_detach(void)
{
  obs_detach_daemon();
  Py_Finalize();
}
