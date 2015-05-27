bin_PROGRAMS = daemon$(EXEEXT)
lib_LTLIBRARIES = libvigilant.la

libvigilant_la_SOURCES = \
	vigilant.h \
	transport.cc \
	udp_transport.cc \
	stats_monitor.cc \
	ipc_protocol.cc \
	async_server.cc

daemon_SOURCES = daemon.cc
daemon_LDADD = libvigilant.la
