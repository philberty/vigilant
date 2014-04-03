#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "watchy.h"

// gcc/clang -g -O2 -Wall test.c -o test -lwatchy -I/usr/local/include/watchy -L/usr/local/lib
int main (int argc, char **argv)
{
  assert (watchy_watchme ("test", "localhost", 7878) == WTCY_NO_ERROR);
  int i;
  for (i = 0; i < 2; ++i)
    {
      printf ("Look Busy %i\n", i+1);
      sleep (5);
    }
  return 0;
}
