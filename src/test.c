#include <stdio.h>
#include <string.h>
#include <watchy.h>

int main (int argc, char **argv)
{
  struct watchy_data test;
  memset (&test, 0, sizeof (test));

  watchy_logPacket (&test, "123\n456\n7\n\n", "key");
  printf ("buffer = [%s]", test.value.buffer);

  return 0;
}
