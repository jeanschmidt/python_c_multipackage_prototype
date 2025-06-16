#include <stdio.h>
#ifdef _WIN32
#define BUILDING_DLL
#endif
#include "message_internal.h"

void do_message_print(char *message) {
    if (message) {
        printf("[ALTERNATIVE IMPLEMENTATION] '%s'\n", message);
    }
}
