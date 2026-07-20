#ifndef BUILD_TEST2_H
#define BUILD_TEST2_H


class CCoffFile
{
public:
    enum
    {
        SUCCESS          =   0,
        ERR_OPEN         =  -1,
        ERR_CREATE       =  -2,
        ERR_RD_HEADER    =  -3,
        ERR_WR_HEADER    =  -4,
        ERR_RD_SECTION   =  -5,
        ERR_WR_SECTION   =  -6,

        ERR_RD_HEX       = -10,
        ERR_WR_HEX       = -11,

        ERR_RD_S3        = -20,
        ERR_WR_S3        = -21,
    };

    CCoffFile();
    ~CCoffFile();

    int Read(char* strFilename);
    int Write(char* strFilename);

protected:
    void InitData(int nFillWord );

};

#endif // BUILD_TEST2_H
