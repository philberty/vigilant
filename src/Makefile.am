bin_PROGRAMS = test$(EXEEXT) picklectl$(EXEEXT)
lib_LTLIBRARIES = libpicklejar.la

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = picklejar.pc

libpicklejar_cindludedir = $(includedir)/picklejar
libpicklejar_cindlude_HEADERS = picklejar.h

libpicklejar_la_YFLAGS = -d
libpicklejar_la_CFLAGS = $(json_CFLAGS) $(event_CFLAGS) $(py_CFLAGS)
libpicklejar_la_LDFLAGS = -rpath '$(libdir)' $(json_LIBS) $(event_LIBS) $(py_LIBS)
libpicklejar_la_SOURCES = \
	picklejarFlask.pyx \
	picklejar-api.c \
	picklejar-restful.c \
	picklejar-unix.c

picklectl_SOURCES = picklectl.c
picklectl_LDADD = libpicklejar.la

test_SOURCES = test.c
test_LDADD = libpicklejar.la

SUFFIXES = .pyx
.pyx.c:
	cython -2 -o $@ $<
