cimport pywatchy
from libc.string cimport memset, strncpy

DEF WTCY_DEFAULT_FIFO = "/tmp/watchy.sock"

DEF WTCY_NO_ERROR    = 0
DEF WTCY_NEXIST_PID  = 1
DEF WTCY_FORK_FAIL   = 2
DEF WTCY_SOCK_FAIL   = 3
DEF WTCY_IS_RUNNING  = 4
DEF WTCY_PACKET_ERR  = 5
DEF WTCY_DAEMON_ERR  = 6
DEF WTCY_USOCK_FAIL  = 7
DEF WTCY_ATIMEOUT    = 8
DEF WTCY_UNKNOWN     = 9

class WatchyDaemon:
    def __init__ (self, host, port, fifo=WTCY_DEFAULT_FIFO):
        cdef int fd
        cdef int cport = port
        cdef const char * chost = host
        cdef int ret = watchy_cAttachRuntime (fifo, chost, cport, &fd, NULL)
        cdef const char * sret = watchy_strerror (ret)
        if ret != WTCY_NO_ERROR:
            raise Exception ('Unable to attach [%i][%s]' % (ret, sret))
        self._csock = fd
        self.port = cport
        self.host = chost

    def __dealloc__ (self):
        watchy_detachRuntime (self._csock)

    def postMessage (self, key, message):
        cdef watchy_data data
        memset (&data, 0, sizeof (data))
        watchy_logPacket (&data, message, key)
        watchy_writePacket (&data, self._csock)

    def watchHost (self, key):
        cdef watchy_data data
        memset (&data, 0, sizeof (data))
        data.T = INTERNAL
        watchy_setTimeStamp (data.tsp, sizeof (data.tsp))
        strncpy (data.key, key, sizeof (data.key))
        data.value.intern.host = True
        watchy_writePacket (&data, self._csock)

    def watchPid (self, key, pid):
        cdef watchy_data data
        memset (&data, 0, sizeof (data))
        data.T = INTERNAL
        watchy_setTimeStamp (data.tsp, sizeof (data.tsp))
        strncpy (data.key, key, sizeof (data.key))
        data.value.intern.pid = pid
        data.value.intern.watch = True
        watchy_writePacket (&data, self._csock)

    def stopWatchPid (self, pid):
        cdef watchy_data data
        memset (&data, 0, sizeof (data))
        data.T = INTERNAL
        watchy_setTimeStamp (data.tsp, sizeof (data.tsp))
        data.value.intern.pid = pid
        data.value.intern.watch = False
        watchy_writePacket (&data, self._csock)

    def persistRuntime (self, persist=True):
        cdef bool p = persist
        watchy_persistRuntime (self._csock, p)
