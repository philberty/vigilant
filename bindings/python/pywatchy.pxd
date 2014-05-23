cdef extern from "watchy.h":
    const char * watchy_strerror (const int)
    int watchy_watchme  (const char *, const char *, const int)
    int watchy_watchpid (const char *, const char *, const int, const int)
