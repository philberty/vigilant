#ifndef __WATCHY_H__
#define __WATCHY_H__

//for bool
#include <stdbool.h>
// for struct tm
#include <time.h>
// for pid_t
#include <unistd.h>
#include <sys/types.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>

// error codes...
#define WTCY_NO_ERROR    0
#define WTCY_NEXIST_PID  1
#define WTCY_FORK_FAIL   2
#define WTCY_SOCK_FAIL   3
#define WTCY_IS_RUNNING  4
#define WTCY_PACKET_ERR  5
#define WTCY_DAEMON_ERR  6
#define WTCY_USOCK_FAIL  7
#define WTCY_ATIMEOUT    8
#define WTCY_UNKNOWN     9

// this is a very basic protocol thsi is the size of every object
// means the server can simly .read (256) and you know you will
// get all the data no need to keep reading etc..
#define WTCY_PACKET_SIZE 256

// hardcoded /tmp ok for now... autoconf can fix this and command line option
#define WTCY_DEFAULT_FIFO "/tmp/watchy.sock"

#ifdef __cplusplus
extern "C" {
#endif

  typedef enum {
    INTERNAL  = 0,
    METRIC    = 1,
    HOST      = 2,
    PROCESS   = 3,
    LOG       = 4,
    SDOWN     = 5,
    PERSIST   = 6,
    HEARTBEAT = 7
  } WATCHY_TYPE;

  struct watchy_metric {
    char status [16];
    pid_t cpid;
    size_t nthreads;
    unsigned int memory;
    long double usage;
  };

  struct watchy_intern {
    bool host;
    char key [32];
    bool watch;
    pid_t pid;
  };

  struct watchy_data {
    WATCHY_TYPE T;
    char key [32];
    char tsp [32];
    union {
      struct watchy_metric metric;
      struct watchy_intern intern;
      char buffer [WTCY_PACKET_SIZE-25];
      bool persist;
      pid_t heartbeat;
    } value ;
  };

  // this return is allocated..
  extern char * watchy_trim (const char *, const size_t);
  
  // setup socket [bind, port, fd, addr_Desc]
  extern int watchy_socket (const char *, const int, int * const, struct sockaddr_in * const);

  // utility functions
  extern int watchy_setTimeStamp (char * const, const size_t);
  extern void watchy_logPacket (struct watchy_data * const, const char *, const char *);

  // get the stats this function is osdep-*.c depends at compile time
  extern void watchy_getStats (struct watchy_metric * const, const pid_t);
  extern void watchy_getHostStats (struct watchy_metric * const);

  // agnostic of tagged union
  extern int watchy_statsToJson (const struct watchy_data * const, const size_t, char * const);

  // return the error string for the error code (string is not allocated)
  extern const char * watchy_strerror (const int);

  // runtime functions
  extern int watchy_writePacketSync (struct watchy_data * const, const int,
				     const struct sockaddr_in * const );
  extern int watchy_writePacket (struct watchy_data * const, const int);
  extern int watchy_cAttachRuntime (const char *, const char *, const int, int * const,
				    char ** const);

  extern void watchy_persistRuntime (int, bool);
  extern void watchy_detachRuntime (int);
  
#ifdef __cplusplus
}
#endif

#endif //__WATCHY_H__
