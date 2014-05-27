#ifndef __WATCHY_H__
#define __WATCHY_H__

// for struct tm
#include <time.h>
// for pid_t
#include <unistd.h>
#include <sys/types.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>

  // error codes...
#define WTCY_NO_ERROR   0
#define WTCY_NEXIST_PID 1
#define WTCY_FORK_FAIL  2
#define WTCY_SOCK_FAIL  3
#define WTCY_IS_RUNNING 4
#define WTCY_PACKET_ERR 5
#define WTCY_UNKNOWN    6

// this is a very basic protocol thsi is the size of every object
// means the server can simly .read (256) and you know you will
// get all the data no need to keep reading etc..
#define WTCY_PACKET_SIZE 256

#ifdef __cplusplus
extern "C" {
#endif

  typedef enum { METRIC, HOST, LOG } WATCHY_TYPE;

  struct watchy_metric {
    char status [16];
    pid_t cpid;
    size_t nthreads;
    unsigned int memory;
  };

  struct watchy_data {
    WATCHY_TYPE T;
    char key [32];
    char tsp [32];
    union {
      struct watchy_metric metric;
      char buffer [WTCY_PACKET_SIZE-25];
    } value ;
  };

  // this return is allocated..
  extern char * watchy_trim (const char *, const size_t);
  
  // setup socket [bind, port, fd, addr_Desc]
  extern int watchy_socket (const char *, const int, int * const, struct sockaddr_in * const);

  // utility functions
  extern int watchy_setTimeStamp (char * const, const size_t);
  extern int watchy_logPacket (struct watchy_data * const, const char *, const char *);

  // get the stats this function is osdep-*.c depends at compile time
  extern void watchy_getStats (struct watchy_metric * const, const pid_t);
  extern void watchy_getHostStats (struct watchy_metric * const);

  // agnostic of tagged union
  extern int watchy_statsToJson (const struct watchy_data * const, const size_t, char * const);

  // return the error string for the error code (string is not allocated)
  extern const char * watchy_strerror (const int);

  // FIXME fork/daemon issues
  extern int watchy_watchme  (const char *, const char *, const int);
  // watch a specified pid [name, host, port, pid] - blocking
  extern int watchy_watchpid (const char *, const char *, const int, const pid_t);
  // watch the host system [name, host, port] - blocking
  extern int watchy_watchHost (const char *, const char *, const int);
  
#ifdef __cplusplus
}
#endif

#endif //__WATCHY_H__
