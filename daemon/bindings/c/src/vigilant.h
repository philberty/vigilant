#ifndef OBSERVANT_H__
#define OBSERVANT_H__

#include <Python.h>

#ifndef DL_IMPORT
# define DL_IMPORT(_T) _T
#endif
#include <libvigilant.h>

// Initilize Python and Observant module
extern int obs_attach(const char *, const char *, const char *);

// detach from observant and cleanup python
extern void obs_detach(void);

#endif //OBSERVANT_H__
