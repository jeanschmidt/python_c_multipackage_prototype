#ifndef MESSAGE_INTERNAL_H
#define MESSAGE_INTERNAL_H

/* Define export/import macros for Windows DLL */
#ifdef _WIN32
    #ifdef BUILDING_DLL
        #define EXPORT __declspec(dllexport)
    #else
        #define EXPORT __declspec(dllimport)
    #endif
#else
    #define EXPORT
#endif

EXPORT void do_message_print(char *message);

#endif
