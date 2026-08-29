#ifndef BUILD_TEST_H
#define BUILD_TEST_H

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <float.h>
#include <math.h>

#ifdef __cplusplus

class CCoffFile
{
public:
    enum { SUCCESS = 0, ERR_OPEN = -1, ERR_CREATE = -2, ERR_RD = -3, ERR_WR = -4 }; 

    CCoffFile();
    ~CCoffFile();

    int Read(char* strFilename);
    int Write(char* strFilename);

private:
    void InitData(int nFillWord );
};

#else // !__cplusplus

// Simple demo logger to stdout.
int common_Log(char level, const char* format, ...);

/// Helper macro to check then handle error. If error, never returns.
#define PROCESS_LUA_ERROR(L, err, fmt, ...)  if (err >= LUA_ERRRUN) { lua_error(L); }

#endif //__cplusplus

#endif // BUILD_TEST_H
