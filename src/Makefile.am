bin_PROGRAMS = \
	test$(EXEEXT) \
	wtail$(EXEEXT) \
	watcher$(EXEEXT)
lib_LTLIBRARIES = libwatchy.la

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = watchy.pc

libwatchy_cindludedir = $(includedir)/watchy
libwatchy_cindlude_HEADERS = watchy.h
libwatchy_la_LDFLAGS = -rpath '$(libdir)'
libwatchy_la_SOURCES = \
	libwatchy.c \
	runtime.c \
	osdep-@PLATFORM@.c

test_SOURCES = test.c
test_LDADD = libwatchy.la

watcher_SOURCES = watcher.c
watcher_LDADD = libwatchy.la

wtail_SOURCES = wtail.c
wtail_LDADD = libwatchy.la
