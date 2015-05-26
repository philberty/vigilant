#include <vigilant.h>

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main (int argc, char **argv)
{
  if (obs_attach ("binding_test", "/tmp/vigilant.pid", "/tmp/vigilant.sock") != 0)
    {
      fprintf (stderr, "Unable to attach to daemon!\n");
      return -1;
    }
  obs_post_message("Hello world from c land!!");
  obs_detach ();
  return 0;
}
