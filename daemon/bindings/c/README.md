# C/C++ - Bindings ⛨
This is C bindings direectly to the stats daemon.

```bash
$ ./config/autogen.sh
$ ./configure --prefix=/opt/observant
$ make
$ make install
```

## Usage

Test program such as:

```c
// test.c
#include <observant.h>

int main(int argc, char **argv) {

  int retval = obs_attach("/tmp/observant.pid", "/tmp/observant.sock");
  if (!retval) {
    fprintf(stderr, "Unable to attach to daemon");
    return -1;
  }

  obs_watch_me();

  obs_detach();

  return 0;
}
```

Compile:

```bash
$ gcc/clang -g -O2 -Wall -c test.c -o test.o -I/opt/observant/include
$ gcc/clang -g -O2 -Wall -o test test.o -L/opt/observant/lib -lobservant
$ ./test
```

Note this build will result in the error:

```bash
/libobservant.h:15:31: error: expected function body after function declarator
__PYX_EXTERN_C DL_IMPORT(int) obs_attach_to_stats_daemon(char const *, char const *);
```

This is a bug with cython i have proposed the fix: https://github.com/cython/cython/pull/341

To get around this error, run make once to generate the libobservant.h and add in this snippet:

```c
#ifndef DL_IMPORT
#  define DL_IMPORT(_T) _T
#endif
```