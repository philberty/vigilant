bin_PROGRAMS = test
lib_LTLIBRARIES = libvigilant.la

SUFFIXES = .pyx
.pyx.c:
	cython -3 -o $@ $<

test_SOURCES = test.c
test_LDADD = libvigilant.la

libvigilant_la_SOURCES = libvigilant.pyx vigilant.c
include_HEADERS = libvigilant.h vigilant.h

CFLAGS += $(PYINCS)
libvigilant_la_LIBADD = $(PYLIBS)
