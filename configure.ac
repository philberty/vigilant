AC_PREREQ(2.59)
AC_REVISION($Revision$)

AC_INIT(watchy, 0.01, https://github.com/redbrain/watchy)
AC_CONFIG_SRCDIR([src/test.c])
AC_CONFIG_HEADER([src/config.h])
dnl keep the autoconf generated stuff neatly in a folder 
AC_CONFIG_AUX_DIR([config])
AM_SANITY_CHECK

dnl Last slash shouldn't be stripped if prefix=/
if test "$prefix" != "/"; then
    prefix=`echo "$prefix" | sed -e 's/\/$//g'`
fi 

dnl Checks for programs.
AC_DEFINE_UNQUOTED([CONFIG_CC], "$CC", [C Compiler used])
AC_PROG_INSTALL
AC_PROG_CC
AC_PROG_CXX

AC_EXEEXT
AC_GNU_SOURCE
AC_PROG_INSTALL

AC_PROG_LIBTOOL
AM_PROG_LIBTOOL

AM_PROG_CC_C_O
AC_C_INLINE
AC_CANONICAL_HOST

AC_CHECK_PROG(CYTHON_CHECK,cython,yes)
if test x"$CYTHON_CHECK" != x"yes" ; then
   AC_MSG_ERROR([Please install cython])
fi
PKG_CHECK_MODULES([py], [python], [],
[
  AC_ERROR([Couldn't find libpython.so])
])
AC_SUBST(py_CFLAGS)
AC_SUBST(py_LIBS)

AM_INIT_AUTOMAKE
AC_CONFIG_FILES([Makefile
                 src/Makefile
                 src/watchy.pc])
AC_OUTPUT

echo "---"
echo "Configuration summary for $PACKAGE_NAME version $VERSION"
echo ""
echo "   * Installation prefix:       $prefix"
echo "   * C Compiler:                $CC"
echo "   * C++ Compiler:              $CXX"
echo "   * C Flags:                   $CFLAGS"
echo "   * C++ Flags:                 $CXXFLAGS"
echo "   * LD Flags:                  $LDFLAGS"
echo ""
echo "---"

dnl libtoolize scans configure.ac  and needs to see some text
m4_define([LIBTOOLIZE_AC_INIT], [])
