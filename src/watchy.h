#ifndef __WATCHY_H__
#define __WATCHY_H__

extern "C" {

// for struct tm
#include <time.h>
// for pid_t
#include <unistd.h>
#include <sys/types.h>

  // error codes...
#define WTCY_NO_ERROR   0
#define WTCY_NEXIST_PID 1
#define WTCY_FORK_FAIL  2
#define WTCY_SOCK_FAIL  3
#define WTCY_IS_RUNNING 4
#define WTCY_UNKNOWN    5

  typedef enum { METRIC, HOST } WATCHY_TYPE;
  struct watchy_data {
    WATCHY_TYPE T;
    char pname [32];
    char tsp [32];
    char status [16];
    pid_t cpid;
    size_t nthreads;
    unsigned int memory;
  };

  // this return is allocated..
  extern char * watchy_trim (const char *, const size_t);
  
  // get the stats this function is osdep-*.c depends at compile time
  extern void watchy_getStats (struct watchy_data * const, const pid_t);
  extern int watchy_statsToJson (const struct watchy_data * const, const size_t, char * const);

  // return the error string for the error code (string is not allocated)
  extern const char * watchy_strerror (const int);
  // watch the current process [name, host, port] - non blocking
  extern int watchy_watchme  (const char *, const char *, const int);
  // watch a specified pid [name, host, port, pid] - blocking
  extern int watchy_watchpid (const char *, const char *, const int, const pid_t);
  // watch the host system [name, host, port] - blocking
  extern int watchy_watchHost (const char *, const char *, const int);
}

#endif //__WATCHY_H__
