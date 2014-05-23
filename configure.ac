AC_INIT(watchy, 0.01, https://github.com/redbrain/watchy)
AC_CONFIG_SRCDIR([src/test.c])
AC_CONFIG_HEADER([src/config.h])
dnl keep the autoconf generated stuff neatly in a folder 
AC_CONFIG_AUX_DIR([config])
AC_CONFIG_MACRO_DIR([m4])
AM_SANITY_CHECK

dnl Last slash shouldn't be stripped if prefix=/
if test "$prefix" != "/"; then
    prefix=`echo "$prefix" | sed -e 's/\/$//g'`
fi 

dnl Checks for programs.
AC_PROG_CC
AC_PROG_CXX

AC_EXEEXT
AC_GNU_SOURCE
AC_PROG_INSTALL

AC_PROG_INSTALL
AC_PROG_LIBTOOL
AM_PROG_LIBTOOL

AM_PROG_CC_C_O
AC_C_INLINE
AC_CANONICAL_HOST

# Figure out the platform for osdep-*.c and forkpty-*.c.
AC_MSG_CHECKING(platform)
case "$host_os" in
	*darwin*)
		AC_MSG_RESULT(darwin)
		PLATFORM=darwin
		;;
	*linux*)
		AC_MSG_RESULT(linux)
		PLATFORM=linux
		;;
	*)
		AC_MSG_RESULT(unknown)
		PLATFORM=unknown
		;;	
esac
AC_SUBST(PLATFORM)

if test "x$PLATFORM" == "xunknown"; then
   AC_MSG_ERROR("Host Platform $PLATFORM unknown")
fi

AM_INIT_AUTOMAKE
AC_CONFIG_FILES([Makefile
                 src/Makefile
                 src/watchy.pc])
AC_OUTPUT

echo "---"
echo "Configuration summary for $PACKAGE_NAME version $VERSION"
echo ""
echo "   * Installation prefix:       $prefix"
echo "   * Platform osdep:            osdep-$PLATFORM.c"
echo "   * C Compiler:                $CC"
echo "   * C++ Compiler:              $CXX"
echo "   * C Flags:                   $CFLAGS"
echo "   * C++ Flags:                 $CXXFLAGS"
echo "   * LD Flags:                  $LDFLAGS"
echo ""
echo "---"

dnl libtoolize scans configure.ac  and needs to see some text
m4_define([LIBTOOLIZE_AC_INIT], [])
