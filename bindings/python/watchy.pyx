cimport watchy

def PyWatchy_WatchMe (name, host, port):
    cdef const char * pname = name
    cdef const char * phost = host
    cdef int ret = watchy_watchme (pname, phost, port)
    cdef const char * estr = watchy_strerror (ret)
    if ret != watchy.WTCY_NO_ERROR:
        raise Exception (estr)
    return ret
