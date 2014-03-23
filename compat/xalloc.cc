#include "squid.h"
#include "compat/xalloc.h"
#include "profiler/Profiler.h"

#if XMALLOC_STATISTICS
#define XMS_DBG_MAXSIZE   (1024*1024)
#define XMS_DBG_SPLIT     (256)     /* mallocs below this value are tracked with DBG_GRAIN_SM precision instead of DBG_GRAIN */
#define XMS_DBG_GRAIN     (16)
#define XMS_DBG_GRAIN_SM  (4)
#define XMS_DBG_OFFSET    (XMS_DBG_SPLIT/XMS_DBG_GRAIN_SM - XMS_DBG_SPLIT/XMS_DBG_GRAIN )
#define XMS_DBG_MAXINDEX  (XMS_DBG_MAXSIZE/XMS_DBG_GRAIN + XMS_DBG_OFFSET)
static int malloc_sizes[XMS_DBG_MAXINDEX + 1];
static int malloc_histo[XMS_DBG_MAXINDEX + 1];
static int dbg_stat_init = 0;

static int
XMS_DBG_INDEX(int sz)
{
    if (sz >= XMS_DBG_MAXSIZE)
        return XMS_DBG_MAXINDEX;

    if (sz <= XMS_DBG_SPLIT)
        return (sz + XMS_DBG_GRAIN_SM - 1) / XMS_DBG_GRAIN_SM;

    return (sz + XMS_DBG_GRAIN - 1) / XMS_DBG_GRAIN + XMS_DBG_OFFSET;
}

static void
stat_init(void)
{
    for (int i = 0; i <= XMS_DBG_MAXINDEX; ++i)
        malloc_sizes[i] = malloc_histo[i] = 0;

    dbg_stat_init = 1;
}

static int
malloc_stat(int sz)
{
    if (!dbg_stat_init)
        stat_init();

    return malloc_sizes[XMS_DBG_INDEX(sz)] += 1;
}

void
malloc_statistics(void (*func) (int, int, int, void *), void *data)
{
    int i = 0;

    for (; i <= XMS_DBG_SPLIT; i += XMS_DBG_GRAIN_SM)
        func(i, malloc_sizes[XMS_DBG_INDEX(i)], malloc_histo[XMS_DBG_INDEX(i)], data);

    i -= XMS_DBG_GRAIN_SM;

    for (; i <= XMS_DBG_MAXSIZE; i += XMS_DBG_GRAIN)
        func(i, malloc_sizes[XMS_DBG_INDEX(i)], malloc_histo[XMS_DBG_INDEX(i)], data);

    memcpy(&malloc_histo, &malloc_sizes, sizeof(malloc_sizes));
}
#endif /* XMALLOC_STATISTICS */

void *
xcalloc(size_t n, size_t sz)
{
    PROF_start(xcalloc);

    if (n < 1)
        n = 1;

    if (sz < 1)
        sz = 1;

    PROF_start(calloc);
    void *p = calloc(n, sz);
    PROF_stop(calloc);

    if (p == NULL) {
        if (failure_notify) {
            static char msg[128];
            snprintf(msg, 128, "xcalloc: Unable to allocate %lu blocks of %lu bytes!\n", (unsigned long)n, (unsigned long)sz);
            failure_notify(msg);
        } else {
            perror("xcalloc");
        }
        exit(1);
    }

#if XMALLOC_DEBUG
    check_malloc(p, sz * n);
#endif
#if XMALLOC_STATISTICS
    malloc_stat(sz * n);
#endif
#if MEM_GEN_TRACE
    if (tracefp)
        fprintf(tracefp, "c:%u:%u:%p\n", (unsigned int) n, (unsigned int) sz, p);
#endif

    PROF_stop(xcalloc);
    return p;
}

void *
xmalloc(size_t sz)
{
    PROF_start(xmalloc);

    if (sz < 1)
        sz = 1;

    PROF_start(malloc);
    void *p = malloc(sz);
    PROF_stop(malloc);

    if (p == NULL) {
        if (failure_notify) {
            static char msg[128];
            snprintf(msg, 128, "xmalloc: Unable to allocate %lu bytes!\n", (unsigned long)sz);
            failure_notify(msg);
        } else {
            perror("malloc");
        }
        exit(1);
    }

#if XMALLOC_DEBUG
    check_malloc(p, sz);
#endif
#if XMALLOC_STATISTICS
    malloc_stat(sz);
#endif
#if MEM_GEN_TRACE
    if (tracefp)
        fprintf(tracefp, "m:%d:%p\n", sz, p);
#endif

    PROF_stop(xmalloc);
    return (p);
}

void *
xrealloc(void *s, size_t sz)
{
    PROF_start(xrealloc);

    if (sz < 1)
        sz = 1;

#if XMALLOC_DEBUG
    if (s != NULL)
        check_free(s);
#endif
    PROF_start(realloc);
    void *p= realloc(s, sz);
    PROF_stop(realloc);

    if (p == NULL) {
        if (failure_notify) {
            static char msg[128];
            snprintf(msg, 128, "xrealloc: Unable to reallocate %lu bytes!\n", (unsigned long)sz);
            failure_notify(msg);
        } else {
            perror("realloc");
        }

        exit(1);
    }

#if XMALLOC_DEBUG
    check_malloc(p, sz);
#endif
#if XMALLOC_STATISTICS
    malloc_stat(sz);
#endif
#if MEM_GEN_TRACE
    if (tracefp)                /* new ptr, old ptr, new size */
        fprintf(tracefp, "r:%p:%p:%d\n", p, s, sz);
#endif
    PROF_stop(xrealloc);
    return (p);
}

void
free_const(const void *s_const)
{
    void *s = const_cast<void *>(s_const);

    PROF_start(free_const);

#if XMALLOC_DEBUG
    check_free(s);
#endif

    PROF_start(free);
    free(s);
    PROF_stop(free);

#if MEM_GEN_TRACE
    if (tracefp)
        fprintf(tracefp, "f:%p\n", s);
#endif
    PROF_stop(free_const);
}
