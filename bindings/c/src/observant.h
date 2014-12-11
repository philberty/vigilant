#ifndef OBSERVANT_H__
#define OBSERVANT_H__

// Initilize Python and Observant module
extern int obs_attach(const char *, const char *);

// detach from observant and cleanup python
extern void obs_detach(void);

// helper function to tell the daemon to watch this process - key
extern int obs_watch_me(const char *);

#endif //OBSERVANT_H__
