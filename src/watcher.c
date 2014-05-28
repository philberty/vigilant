#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include <getopt.h>
#include <errno.h>

#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>

#include "watchy.h"

static void print_help    (const char *);
static void print_version (const char *);
static void shandler      (int);

static volatile bool running;

static void
shandler (int signo)
{
  running = false;
}

static void
print_help (const char * arg)
{
  printf ("Usage: %s [options] name:pid name:pid...\nOptions:\n", arg);
  printf ("\t--help|-h\tPrint this help\n");
  printf ("\t--key|-k\tKey to send host stats to\n");
  printf ("\t--version|-v\tPrint version string\n");
  printf ("\t--port|-p\tPort of server\n");
  printf ("\t--hostname|-b\tHostname of server\n");
  printf ("\t--daemon|-F\tDaemonize this\n");
  printf ("\n");
}

static void
print_version (const char * arg)
{
  printf ("%s version %s\n", arg, PACKAGE_STRING);
}

int main (int argc, char **argv)
{
  int c, port = 0;
  char * bind = NULL, * key = NULL;
  bool forkme = false;
  while (1)
    {
      static struct option long_options [] = {
        { "help",     no_argument,       0, 'h' },
        { "version",  no_argument,       0, 'v' },
	{ "daemon",   no_argument,       0, 'F' },
        { "hostname", required_argument, 0, 'b' },
        { "port",     required_argument, 0, 'p' },
	{ "key",      required_argument, 0, 'k' },
        { 0, 0, 0, 0 }
      };
      int option_index = 0;
      c = getopt_long (argc, argv, "hvFb:p:i:k:", long_options, &option_index);
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

	case 'F':
	  forkme = true;
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

  // TODO
  if (forkme)
    ; // daemonize here...

  // add option to new fifo
  char * dfifo = WTCY_DEFAULT_FIFO;
  char * fifo = dfifo;

  int fd = 0;
  int ret = watchy_cAttachRuntime (fifo, bind, port, &fd);
  if (fifo != dfifo)
    free (fifo);

  if (ret != WTCY_NO_ERROR)
    {
      fprintf (stderr, "Error initilizing watchy runtime [%s]\n",
	       watchy_strerror (ret));
      printf ("errno = [%s]\n", strerror (errno));
      return -1;
    }

  struct watch_node {
    pid_t pid;
    char * key;
  };
  size_t offs = 0, plen = argc - optind;
  struct watch_node nodes [plen];
  memset (&nodes, 0, sizeof (nodes));

  while (optind < argc)
    {
      const char * pair = argv [optind++];

      size_t len = strlen (pair);
      char key [len];
      char value [len];
      memset (key, 0, len);
      memset (value, 0, len);

      char * p = strchr (pair, ':');
      size_t poffs = p - pair + 1;
      if (poffs >= len || poffs == 0)
	{
	  fprintf (stderr, "Pid pair [%s] seems invalid\n", pair);
	  continue;
	}

      strncpy (key, pair, poffs - 1);
      strncpy (value, pair + poffs, len - poffs);
      const pid_t ipid = atoi (value);

      int rkill = kill (ipid, 0);
      if (rkill != 0)
	{
	  fprintf (stderr, "pid [%i] invalid [%s]\n", ipid, strerror (errno));
	  continue;
	}
      printf ("Trying to watch pid [%i] posting to [udp://%s@%s:%i]\n", ipid, key, bind, port);

      nodes [offs].pid = ipid;
      nodes [offs].key = strdup (key);
      offs++;
    }
  signal (SIGINT, shandler);

  if (key != NULL)
    running = true;
  else if (offs > 0)
    running = true;
  else
    {
      fprintf (stderr, "Nothing to watch closing..\n");
      running = false;
    }

  size_t i;
  while (running)
    {
      struct watchy_data data;
      for (i = 0; i < offs; ++i)
	{
	  memset (&data, 0, sizeof (data));
	  if (kill (nodes [i].pid, 0) == 0)
	    {
	      data.T = PROCESS;
	      strncpy (data.key, nodes [i].key, sizeof (data.key));
	      watchy_setTimeStamp (data.tsp, sizeof (data.tsp));
	      watchy_getStats (&data.value.metric, nodes [i].pid);

	      watchy_writePacket (&data, fd);
	    }
	}
      if (key != NULL)
	{
	  memset (&data, 0, sizeof (data));

	  data.T = HOST;
	  strncpy (data.key, key, sizeof (data.key));
	  watchy_setTimeStamp (data.tsp, sizeof (data.tsp));
	  watchy_getHostStats (&data.value.metric);

	  watchy_writePacket (&data, fd);
	}

      sleep (1);
    }

  for (i = 0; i < offs; ++i)
    free (nodes [i].key);
  watchy_detachRuntime (fd);

  return 0;
}
