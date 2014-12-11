lib_LTLIBRARIES = libobservant.la

SUFFIXES = .pyx
.pyx.c:
	cython -3 -o $@ $<

libobservant_la_SOURCES = libobservant.pyx observant.c
include_HEADERS = libobservant.h observant.h

CFLAGS += $(PYINCS)
libobservant_la_LIBADD = $(PYLIBS)
