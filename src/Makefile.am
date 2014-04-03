bin_PROGRAMS = test$(EXEEXT) watcher$(EXEEXT)
lib_LTLIBRARIES = libwatchy.la

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = watchy.pc

libwatchy_cindludedir = $(includedir)/watchy
libwatchy_cindlude_HEADERS = watchy.h
libwatchy_la_LDFLAGS = -rpath '$(libdir)'
libwatchy_la_SOURCES = \
	libwatchy.c \
	osdep-@PLATFORM@.c

watcher_SOURCES = watcher.c
watcher_LDADD = libwatchy.la

test_SOURCES = test.c
test_LDADD = libwatchy.la
