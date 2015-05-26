#include <vigilant.h>

int
obs_attach(const char *key, const char *lock, const char *sock) 
{
  Py_Initialize();
  PyInit_libvigilant();
  return obs_attach_to_stats_daemon(key, lock, sock);
}

void
obs_detach(void)
{
  obs_detach_daemon();
  Py_Finalize();
}
