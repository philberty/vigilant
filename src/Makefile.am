bin_PROGRAMS = \
	proTest$(EXEEXT) \
	logTest$(EXEEXT) \
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

watcher_SOURCES = watcher.c
watcher_LDADD = libwatchy.la

wtail_SOURCES = wtail.c
wtail_LDADD = libwatchy.la

proTest_SOURCES = test.c
proTest_LDADD = libwatchy.la

logTest_SOURCES = log.c
logTest_LDADD = libwatchy.la
