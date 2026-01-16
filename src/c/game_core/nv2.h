#ifndef __NV2_H__
#define __NV2_H__
#ifdef __cplusplus
extern "C" {
#endif


#include "libgba/gba.h"

//---------------------------------------------------------------------------


//---------------------------------------------------------------------------

typedef struct {
	char* cmd;
	s32   argv;
	void  (*pExec)(void);

} ST_NV_PARSE_TBL;

//---------------------------------------------------------------------------
void NvExecParse(void);
void NvExecParseSub(void);

void NvExecParse1R(void);
void NvExecParse1T(void);
void NvExecParse1M(void);
void NvExecParse1N(void);
void NvExecParse2G(void);
void NvExecParse2B(void);
void NvExecParse2E(void);
///// ソース改変ここから /////
/*
void NvExecParse2X(void);
*/
///// ソース改変ここまで /////
void NvExecParse2J(void);
void NvExecParse2T(void);
void NvExecParse2S(void);
///// ソース改変ここから /////
/*
void NvExecParse3G(void);
void NvExecParse3R(void);
void NvExecParse3L(void);
void NvExecParse3N(void);
void NvExecParse3I(void);
*/
///// ソース改変ここまで /////
void NvExecParse3W(void);
void NvExecParse3T(void);
void NvExecParseSel(void);
///// ソース改変ここから /////
/*
void NvExecParseCal(void);
*/
///// ソース改変ここまで /////


///// ソース改変ここから /////
/*
bool NvIsExecParseCmd(char* p);
*/
///// ソース改変ここまで /////


#ifdef __cplusplus
}
#endif
#endif
