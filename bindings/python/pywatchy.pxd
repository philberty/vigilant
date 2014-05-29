from posix.unistd cimport pid_t
from libcpp cimport bool

DEF WTCY_PACKET_SIZE = 256

cdef extern from "watchy.h":
    enum WATCHY_TYPE:
        INTERNAL,
        METRIC,
        HOST,
        PROCESS,
        LOG,
        SDOWN

    struct watchy_metric:
        char status [16]
        pid_t cpid
        size_t nthreads
        unsigned int memory

    struct watchy_intern:
        bool host
        char key [32]
        bool watch
        pid_t pid

    union watchy_union:
        watchy_metric metric
        watchy_intern intern
        char buffer [WTCY_PACKET_SIZE-25]

    struct watchy_data:
        WATCHY_TYPE T
        char key [32]
        char tsp [32]
        watchy_union value

    const char * watchy_strerror (const int)
    int watchy_setTimeStamp (char * const, const size_t)
    void watchy_logPacket (watchy_data * const, const char *, const char *)
    void watchy_getStats (watchy_metric * const, const pid_t)
    void watchy_getHostStats (watchy_metric * const)
    int watchy_statsToJson (const watchy_data * const, const size_t, char * const)
    int watchy_writePacket (watchy_data * const, const int)
    int watchy_cAttachRuntime (const char *, const char *, const int, int * const)
    void watchy_detachRuntime (int)
