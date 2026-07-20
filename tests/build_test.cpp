#include <stdarg>
#include <string>
#include "build_test2.h"

using namespace std;

CCoffFile::CCoffFile()
{
}

CCoffFile::~CCoffFile()
{
}

int CCoffFile::Read(char* strFilename)
{
    // init
    InitData(99);

    return 0;
}

int CCoffFile::Write(char* strFilename)
{
    return 0;
}

void CCoffFile::InitData(int nFillWord )
{
}
