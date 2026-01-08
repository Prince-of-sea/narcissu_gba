#include "se.h"
#include "libmy/snd.arm.h"
#include "file.h"

//---------------------------------------------------------------------------
ST_SE Se;


//---------------------------------------------------------------------------
void SeInit(void)
{
	_Memset(&Se, 0x00, sizeof(ST_SE));
}
//---------------------------------------------------------------------------
void SePlay(s32 no)
{
	Se.no = no;

	TRACE("[SePlay no:%d]\n", no);

	u8* p = FileGetFmx(no);
	s32 size = FileGetSize();

	/* ソース改変ここから */
	
	// pythonより FMX_LIST ループ再生SE
	// [ 10,"se/amadare.wav"],
	// [ 44,"se/rain_12.wav"],
	
	if(no == 10 || no == 44)
	{
		SndPlay(SND_ID_FMX, p, size, 2, true);	// ループ
	}
	else
	{
		SndPlay(SND_ID_FMX, p, size, 2, false);
	}
	
	/* ソース改変ここまで */
}
//---------------------------------------------------------------------------
void SeStop(void)
{
	if(SndIsPlay(SND_ID_FMX) == false)
	{
		return;
	}

	SndStop(SND_ID_FMX);
}
//---------------------------------------------------------------------------
bool SeIsPlay(void)
{
	return SndIsPlay(SND_ID_FMX);
}
