#include "config.h"

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include "watchy.h"

static int pfd;
static bool init = false;

int watchy_writePacket (const struct watchy_data * data, const int fd)
{
  return 0;
}

int watchy_cAttachRuntime (const char * fifo, const char * bind, const int port)
{
  return;
}

void watchy_detachRuntime (void)
{
  return;
}
