#include <observant.h>

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static void
myprogram (void)
{
  printf("Doing something: ");
  size_t i;
  for (i = 0; i < 15; ++i)
    {
      printf (".");
      sleep (1);
    }
  printf("\nDone!\n");
}

int main (int argc, char **argv)
{
  if (obs_attach ("/tmp/observant.pid", "/tmp/observant.sock") != 0)
    {
      fprintf (stderr, "Unable to attach to daemon!\n");
      return -1;
    }
  obs_watch_me (argv[0]);
  myprogram ();
  obs_detach ();
  return 0;
}
