lib_LTLIBRARIES = libobservant.la

SUFFIXES = .pyx
.pyx.c:
	@echo "  CPY   " $<
	@cython -3 -o $@ $<

libobservant_la_SOURCES = libobservant.pyx
include_HEADERS = libobservant.h
