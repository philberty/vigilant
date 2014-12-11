AC_PREREQ(2.59)
AC_REVISION($Revision$)

AC_INIT(libobservant, 0.1, https://github.com/redbrain/observant)
AC_CONFIG_SRCDIR([src/libobservant.pyx])
AC_CONFIG_HEADER([config.h])
AC_CONFIG_AUX_DIR([config])
AM_SANITY_CHECK

dnl Last slash shouldn't be stripped if prefix=/
if test "$prefix" != "/"; then
    prefix=`echo "$prefix" | sed -e 's/\/$//g'`
fi 

dnl Checks for programs.
AC_DEFINE_UNQUOTED([CONFIG_CC], "$CC", [C Compiler used])

AC_PROG_AWK
AC_PROG_CPP
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_MAKE_SET
AC_PROG_RANLIB
AC_CHECK_PROGS(AR, ar aal, ar)
AC_PROG_CC

AC_EXEEXT
AC_GNU_SOURCE
AC_PROG_INSTALL

AC_PROG_LIBTOOL
AM_PROG_LIBTOOL

AM_PROG_CC_C_O

AC_CANONICAL_HOST

# When CFLAGS isn't set at this stage and gcc is detected by the macro below,
# autoconf will automatically use CFLAGS="-O2 -g". Prevent that by using an
# empty default.
: ${CFLAGS=""}

AC_CHECK_PROG(CYTHON_CHECK,cython,yes)
if test x"$CYTHON_CHECK" != x"yes" ; then
   AC_MSG_ERROR([Please install cython])
fi

AC_CHECK_PROG(PYTHON_CHECK,python3-config,yes)
if test x"$PYTHON_CHECK" != x"yes" ; then
   AC_MSG_ERROR([Please install python3-config])
fi

PYINCS=`python3-config --includes`
PYLIBS=`python3-config --ldflags`
AC_SUBST(PYINCS)
AC_SUBST(PYLIBS)

# Check whether --with-system-type or --without-system-type was given.
AC_ARG_WITH([system-type],
    [AS_HELP_STRING([--with-system-type],
       [Set the system type, like "sun-solaris10"])],
    [SYSTEM_TYPE="$withval"],
    [SYSTEM_TYPE="$host_vendor-$host_os"])
AC_ARG_WITH([machine-type],
    [AS_HELP_STRING([--with-machine-type],
       [Set the machine type, like "sparc"])],
    [MACHINE_TYPE="$withval"],
    [MACHINE_TYPE="$host_cpu"])
AC_SUBST(SYSTEM_TYPE)
AC_DEFINE_UNQUOTED([SYSTEM_TYPE], ["$SYSTEM_TYPE"],
                   [Name of system, eg sun-solaris])
AC_SUBST(MACHINE_TYPE)
AC_DEFINE_UNQUOTED([MACHINE_TYPE], ["$MACHINE_TYPE"],
                   [Machine type name, eg sparc])


AM_INIT_AUTOMAKE
AC_CONFIG_FILES([Makefile
                src/Makefile])
AC_OUTPUT

echo "---"
echo "Configuration summary for $PACKAGE_NAME version $VERSION"
echo ""
echo "   * Installation prefix:       $prefix"
echo "   * System type:               $SYSTEM_TYPE"
echo "   * Host CPU:                  $host_cpu"
echo "   * C Compiler:                $CC"
echo "   * CFlags:                    $CFLAGS"
echo "   * Python Includes:           $PYINCS"
echo "   * Python Libs:               $PYLIBS"
echo ""
echo "---"

dnl libtoolize scans configure.ac  and needs to see some text
m4_define([LIBTOOLIZE_AC_INIT], [])
