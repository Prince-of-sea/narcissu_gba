#include "bgm.h"
#include "libmy/snd.arm.h"
#include "libmy/vgm.arm.h"
#include "file.h"

//---------------------------------------------------------------------------
ST_BGM Bgm;

///// ソース改変ここから /////
s32 adjustList[13] = {
	36,		// bgm10.bin
	35,		// bgm11.bin
	40,		// bgm12.bin
	51,		// bgm13.bin
	60,		// bgm14.bin
	41,		// bgm15.bin
	66,		// bgm16.bin
	76,		// bgm17.bin
	50,		// bgm18.bin
	42,		// bgm19.bin
	42,		// bgm20.bin
	31,		// bgm21.bin
	32,		// bgm22.bin
};
///// ソース改変ここまで /////

//---------------------------------------------------------------------------
void BgmInit(void)
{
	_Memset(&Bgm, 0x00, sizeof(ST_BGM));

	Bgm.vol = VgmGetVol();
}
//---------------------------------------------------------------------------
void BgmPlay(s32 no)
{
	Bgm.no = no;

	if(no == 1)
	{
		BgmStop();

		return;
	}

	///// ソース改変ここから /////
	/*
	if(no == 3 || no == 11)
	{
		BgmPlayRaw(no);
	}
	else
	{
		BgmPlayVgm(no);
	}
	*/
	BgmPlayRaw(no);
	///// ソース改変ここまで /////
}
//---------------------------------------------------------------------------
void BgmPlayRaw(s32 no)
{
	TRACE("[BgmPlayRaw %d]\n", no);

	u8* p = FileGetBgm(no);
	s32 size = FileGetSize();

	///// ソース改変ここから /////
	/*
	SndPlay(SND_ID_BGM, p, size, 2, false);
	*/
	s32 adjust = adjustList[no - 10]; // BGMナンバーはbgm10始まり
	SndPlay(SND_ID_BGM, p, size, adjust, true);
	///// ソース改変ここまで /////
}
//---------------------------------------------------------------------------
///// ソース改変ここから /////
// 使わなくなったため削除
/*
void BgmPlayVgm(s32 no)
{
	TRACE("[BgmPlayVgm %d]\n", no);

	u8* p = FileGetBgm(no);

	VgmPlay(p, true);
}
*/
///// ソース改変ここまで /////
//---------------------------------------------------------------------------
void BgmSetVol(s32 vol)
{
	if(Bgm.vol == vol)
	{
		return;
	}

	VgmSetVol(vol);
	Bgm.vol = vol;
}
//---------------------------------------------------------------------------
s32 BgmGetVol(void)
{
	return Bgm.vol;
}
//---------------------------------------------------------------------------
void BgmLoadPlay(void)
{
	s32 tmp = Bgm.no;

	BgmStop();


	if(Bgm.vol != VgmGetVol())
	{
		VgmSetVol(Bgm.vol);
	}

	BgmPlay(tmp);
}
//---------------------------------------------------------------------------
void BgmStop(void)
{
	TRACE("[BgmStop]\n");

	if(VgmIsPlay() == true)
	{
		VgmStop();
	}

	if(SndIsPlay(SND_ID_BGM) == true)
	{
		SndStop(SND_ID_BGM);
	}

	Bgm.no = 1;
}
