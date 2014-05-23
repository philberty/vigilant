DEF WTCY_NO_ERROR   = 0
DEF WTCY_NEXIST_PID = 1
DEF WTCY_FORK_FAIL  = 2
DEF WTCY_SOCK_FAIL  = 3
DEF WTCY_UNKNOWN    = 4

cdef extern from "watchy.h":
    const char * watchy_strerror (const int)
    int watchy_watchme  (const char *, const char *, const int)
    int watchy_watchpid (const char *, const char *, const int, const int)
