#include "file.h"
#include "libmy/gbfs.h"
#include "info.h"


//---------------------------------------------------------------------------


//---------------------------------------------------------------------------
void FileInit(void)
{
	// EMPTY
}
//---------------------------------------------------------------------------
u8* FileGetScn(s32 no)
{
	char buf[20];
	_Sprintf(buf, "SCN%03d.bin", no);

	return GbfsGetSafePointer(buf);
}
//---------------------------------------------------------------------------
u8* FileGetImg(s32 no)
{
	char buf[20];
	_Sprintf(buf, "img%03d.bin", no);

	return GbfsGetSafePointer(buf);
}
//---------------------------------------------------------------------------
///// ソース改変ここから /////
// 使わなくなったため削除
/*
u8* FileGetMsk(s32 no)
{
	char buf[20];
	_Sprintf(buf, "msk%02d.bin", InfoGetMskNo(no));

	return GbfsGetSafePointer(buf);
}
*/
///// ソース改変ここまで /////
//---------------------------------------------------------------------------
///// ソース改変ここから /////
// 使わなくなったため削除
/*
u8* FileGetEff(s32 no)
{
	char buf[20];
	_Sprintf(buf, "CLS%02d.bin", no);

	return GbfsGetSafePointer(buf);
}
*/
///// ソース改変ここまで /////
//---------------------------------------------------------------------------
u8* FileGetBgm(s32 no)
{
	char buf[20];
	///// ソース改変ここから /////
	/*
	_Sprintf(buf, "bgm%02d.bin", no);
	*/
	if(no == 2)
	{
		// タイトルで利用 "se/umi13.wav"
		// こいつだけ効果音をBGM扱いさせるので特別に2を割り当て
		_Sprintf(buf, "fmx045.bin");
	}
	else
	{
		_Sprintf(buf, "bgm%02d.bin", no);
	}
	///// ソース改変ここまで /////

	return GbfsGetSafePointer(buf);
}
//---------------------------------------------------------------------------
u8* FileGetFmx(s32 no)
{
	char buf[20];
	///// ソース改変ここから /////
	/*
	_Sprintf(buf, "fmx%02d.bin", no);
	*/
	_Sprintf(buf, "fmx%03d.bin", no);
	///// ソース改変ここまで /////

	return GbfsGetSafePointer(buf);
}
//---------------------------------------------------------------------------
s32 FileGetSize(void)
{
	return GbfsGetFileSize();
}
