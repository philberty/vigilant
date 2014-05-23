#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>

#include <sys/types.h>
#include <sys/wait.h>

#include "watchy.h"

static void print_help    (const char *);
static void print_version (const char *);

static void
print_help (const char * arg)
{
  printf ("Usage: %s [options] name:pid name:pid...\nOptions:\n", arg);
  printf ("\t--help|-h\tPrint this help\n");
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

int main (int argc, char **argv)
{
  char * bind = NULL;
  int c, port = 0;
  while (1)
    {
      static struct option long_options [] = {
        { "help",     no_argument,       0, 'h' },
        { "version",  no_argument,       0, 'v' },
        { "hostname", required_argument, 0, 'b' },
        { "port",     required_argument, 0, 'p' },
        { 0, 0, 0, 0 }
      };
      int option_index = 0;
      c = getopt_long (argc, argv, "hvb:p:i:", long_options, &option_index);
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

        default:
          break;
        }
    }

  if ((bind == NULL) || (port == 0))
    {
      fprintf (stderr, "Stats destination bind and port unset see --help\n");
      return -1;
    }

  if (optind >= argc)
    {
      fprintf (stderr, "Please specify pids to watch\n");
      return -1;
    }

  size_t offs = 0;
  pid_t pids [argc - optind];
  memset (&pids, 0, sizeof (pids));

  while (optind < argc)
    {
      const char * pair = argv [optind++];

      size_t len = strlen (pair);
      char key [len];
      char value [len];
      memset (key, 0, len);
      memset (value, 0, len);

      char * p = strchr (pair, ':');
      size_t offs = p - pair + 1;
      if (offs >= len || offs == 0)
	{
	  fprintf (stderr, "Pid pair [%s] seems invalid\n", pair);
	  continue;
	}

      strncpy (key, pair, offs - 1);
      strncpy (value, pair + offs, len - offs);
      const pid_t ipid = atoi (value);

      printf ("Trying to watch pid [%i] posting to [udp://%s@%s:%i]\n",
	      ipid, key, bind, port);
      pids [offs] = fork ();
      switch (pids [offs])
	{
	case -1:
	  fprintf (stderr, "Error forking watcher for %i\n", ipid);
	  break;

	case 0:
	  {
	    int retval = watchy_watchpid (key, bind, port, ipid);
	    if (retval != WTCY_NO_ERROR)
	      fprintf (stderr, "Error watching pid %i - %s\n",
		       ipid, watchy_strerror (retval));
	    exit (0);
	  }
	  break;

	default:
	  break;
	}
      offs++;
    }
  free (bind);

  // don't care about error conditions here
  size_t i;
  for (i = 0; i < offs; ++ i)
    waitpid (pids [i], NULL, 0);
  return 0;
}
