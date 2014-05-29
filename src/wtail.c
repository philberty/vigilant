#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include <getopt.h>
#include <signal.h>

#include <watchy.h>

static volatile bool running;
static void tail (const int, const char *);
static void print_help    (const char *);
static void print_version (const char *);

static void
shandler (int signo)
{
  running = false;
}

static void
print_help (const char * arg)
{
  printf ("Usage: %s [options] stdin\nOptions:\n", arg);
  printf ("\t--help|-h\tPrint this help\n");
  printf ("\t--key|-k\tKey to send host stats to\n");
  printf ("\t--version|-v\tPrint version string\n");
  printf ("\t--port|-p\tPort of server\n");
  printf ("\t--hostname|-b\tHostname of server\n");
  printf ("\n");
}

static void
print_version (const char * arg)
{
  printf ("%s version %s\n", arg, PACKAGE_STRING);
}

static void
tail (const int fd, const char * key)
{
  signal (SIGINT, shandler);
  running = true;

  ssize_t read;
  size_t len = 128;
  char * line = calloc (len, sizeof (char));

  struct watchy_data packet;
  while (running)
    {
      read = getline (&line, &len, stdin);
      if (read != -1 && len > 0)
	{
	  memset (&packet, 0, sizeof (packet));
	  watchy_logPacket (&packet, line, key);
	  watchy_writePacket (&packet, fd);
	}
    }
  if (line != NULL)
    free (line);
}

int main (int argc, char **argv)
{
  char * fifo = WTCY_DEFAULT_FIFO;
  int c, port = 0;
  char * bind = NULL, * key = NULL;
  while (1)
    {
      static struct option long_options [] = {
        { "help",     no_argument,       0, 'h' },
        { "version",  no_argument,       0, 'v' },
        { "hostname", required_argument, 0, 'b' },
        { "port",     required_argument, 0, 'p' },
	{ "key",      required_argument, 0, 'k' },
	{ "pipe",     required_argument, 0, 'f' },
        { 0, 0, 0, 0 }
      };
      int option_index = 0;
      c = getopt_long (argc, argv, "hvb:p:i:k:f:", long_options, &option_index);
      if (c == -1)
        break;

      switch (c)
        {
        case 'h':
          print_help (*argv);
          return 0;

        case 'v':
          print_version (*argv);
          return 0;

        case 'b':
          bind = strdup (optarg);
          break;

        case 'p':
          port = atoi (optarg);
          break;

	case 'k':
	  key = strdup (optarg);
	  break;

	case 'f':
	  fifo = strdup (optarg);
	  break;

        default:
          break;
        }
    }

  if ((bind == NULL) || (port == 0))
    {
      fprintf (stderr, "Stats destination bind and port unset see --help\n");
      return -1;
    }

  int fd;
  int ret = watchy_cAttachRuntime (fifo, bind, port, &fd);
  if (fifo != WTCY_DEFAULT_FIFO)
    free (fifo);

  if (ret != WTCY_NO_ERROR)
    {
      fprintf (stderr, "Unable to attach to runtime [%i:%s]", ret, watchy_strerror (ret));
      return -1;
    }
  tail (fd, key);

  watchy_detachRuntime (fd);
  return 0;
}
