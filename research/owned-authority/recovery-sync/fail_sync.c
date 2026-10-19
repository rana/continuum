#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* Single-threaded Linux laboratory interposer, never loaded into upstream code.
   Returning EIO at the selected call deliberately does not invoke real fsync.
   This is not a kernel/device error or a persistence emulator. */
int fsync(int descriptor) {
    static unsigned long count = 0;
    int (*underlying)(int) = (int (*)(int))dlsym(RTLD_NEXT, "fsync");
    const char *failure = getenv("CONTINUUM_SYNC_FAIL_AT");
    const char *log = getenv("CONTINUUM_SYNC_LOG");
    unsigned long number = ++count;
    char link[64], resource[4096];
    snprintf(link, sizeof(link), "/proc/self/fd/%d", descriptor);
    ssize_t size = readlink(link, resource, sizeof(resource) - 1);
    if (size < 0) size = 0;
    resource[size] = '\0';
    int result, saved;
    if (failure && strtoul(failure, NULL, 10) == number) {
        result = -1; saved = EIO;
    } else if (underlying) {
        result = underlying(descriptor); saved = errno;
    } else {
        result = -1; saved = ENOSYS;
    }
    if (log) {
        int output = open(log, O_WRONLY | O_CREAT | O_APPEND, 0600);
        if (output >= 0) {
            char line[4608];
            int length = snprintf(line, sizeof(line), "%lu\t%d\t%d\t%s\n", number, result, result ? saved : 0, resource);
            if (length > 0 && length < (int)sizeof(line)) {
                ssize_t ignored = write(output, line, (size_t)length);
                (void)ignored;
            }
            close(output);
        }
    }
    errno = saved;
    return result;
}
