AC_PREREQ(2.59)
AC_REVISION($Revision$)

AC_INIT(vigilant, 0.01, http://vigilantlabs.co.uk)
AC_CONFIG_SRCDIR([src/daemon.cc])
AC_CONFIG_HEADER([src/config.h])
dnl keep the autoconf generated stuff neatly in a folder :)
AC_CONFIG_AUX_DIR([config])
AM_SANITY_CHECK

dnl Last slash shouldn't be stripped if prefix=/
if test "$prefix" != "/"; then
    prefix=`echo "$prefix" | sed -e 's/\/$//g'`
fi 

dnl Checks for programs.
AC_DEFINE_UNQUOTED([CONFIG_CC], "$CC", [C Compiler used])
AC_DEFINE_UNQUOTED([CONFIG_CXX], "$CXX", [C++ Compiler used])

AC_PROG_AWK
AC_PROG_CPP
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_MAKE_SET
AC_PROG_RANLIB
AC_CHECK_PROGS(AR, ar aal, ar)
AC_PROG_CC
AC_PROG_CXX

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

# Just to make sure we dont do debug on default!
debug=no
AC_ARG_WITH(debug,
  [AS_HELP_STRING([--with-debug=yes/no],
    [With Debug symbols, default no.])],
  [debug="$withval"])
AM_CONDITIONAL(IS_DEBUG, test "x$debug" = xyes)

# Is this a static build?
AC_ARG_ENABLE(
       static,
       AC_HELP_STRING(--enable-static, create a static build),
       found_static=$enable_static
)
if test "x$found_static" = xyes; then
   LDFLAGS="$LDFLAGS -static"
fi

# Is this gcc?
AM_CONDITIONAL(IS_GCC, test "x$GCC" = xyes)
AC_MSG_CHECKING(for gcc that whines about -I)
AC_EGREP_CPP(
        yes,
        [
                #if __GNUC__ > 3
                yes
                #endif
        ],
        found_gcc4=yes,
        found_gcc4=no
)
AM_CONDITIONAL(IS_GCC4, test "x$found_gcc4" = xyes)
AC_MSG_RESULT($found_gcc4)

# Is this Sun CC?
AC_EGREP_CPP(
        yes,
        [
              #ifdef __SUNPRO_C
              yes
              #endif
        ],
        found_suncc=yes,
        found_suncc=no
)
AM_CONDITIONAL(IS_SUNCC, test "x$found_suncc" = xyes)

# Is this glibc?
AC_MSG_CHECKING(for glibc)
AC_EGREP_CPP(
        yes,
        [
                #include <features.h>
                #ifdef __GLIBC__
                yes
                #endif
        ],
        found_glibc=yes,
        found_glibc=no
)
AM_CONDITIONAL(IS_GLIBC, test "x$found_glibc" = xyes)
AC_MSG_RESULT($found_glibc)

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
AM_SILENT_RULES([yes])

AC_HEADER_STDBOOL
AC_HEADER_STDC

# Checks for typedefs, structures, and compiler characteristics.
AC_C_CONST
AC_TYPE_SIZE_T

# Checks for library functions.
AC_FUNC_MALLOC
AC_FUNC_VPRINTF
AC_CONFIG_FILES([Makefile
                 src/Makefile])
AC_OUTPUT

echo "---"
echo "Configuration summary for $PACKAGE_NAME version $VERSION"
echo ""
echo "   * Installation prefix:       $prefix"
echo "   * System type:               $SYSTEM_TYPE"
echo "   * Host CPU:                  $host_cpu"
echo "   * C++ Compiler:              $CXX"
echo "   * DEBUG Symbols:             $debug"
echo ""
echo "---"

dnl libtoolize scans configure.ac  and needs to see some text
m4_define([LIBTOOLIZE_AC_INIT], [])
