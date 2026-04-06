#include "mode3.arm.h"
#include "../libbios/swi.h"
#include "mem.arm.h"

// 例外処理　VRAMに直接書いています（チラつき注意

//---------------------------------------------------------------------------
ST_MODE3 Mode3 EWRAM_BSS;


//---------------------------------------------------------------------------
void Mode3Init(void)
{
	MemClear(&Mode3, sizeof(ST_MODE3));
}
//---------------------------------------------------------------------------
IWRAM_CODE void Mode3DrawBg(u16* pImg)
{
	u16* pDst = Mode3.buf + Mode3.idx * MODE3_MAX_SCN_SIZE;

	///// ソース改変ここから /////
	// 横解像度を4:3相当(212)から最大値(240)へ変更 以下改変部分も同様
	/*
	MemIncFast(pImg, pDst, 212*160*2);
	*/
	MemIncLZ77(pImg, pDst);
	///// ソース改変ここまで /////
}
//---------------------------------------------------------------------------
///// ソース改変ここから /////
// 使わなくなったため削除
/*
IWRAM_CODE void Mode3DrawChr(s32 sx, s32 sy, s32 cx, s32 cy, u16* pImg, u8* pMsk)
{
	u16* pDst = Mode3.buf + Mode3.idx * MODE3_MAX_SCN_SIZE + sy * 212 + sx;
	s32  x, y;

	for(y=0; y<cy; y++)
	{
		for(x=0; x<cx; x++)
		{
			u32 m = pMsk[x];

			if(m == 0x00)
			{
				continue;
			}

			u32 src = pImg[x];

			if(m == 0x1f)
			{
				pDst[x] = src;

				continue;
			}

			u32 dst = pDst[x];

			u32 rbSrc = src & 0x7c1f;
			u32  gSrc = src & 0x03e0;
			u32 rbDst = dst & 0x7c1f;
			u32  gDst = dst & 0x03e0;

			rbDst += ((rbSrc - rbDst) * m) >> 5;
			 gDst += (( gSrc  - gDst) * m) >> 5;

			pDst[x] = (rbDst & 0x7c1f) | (gDst & 0x03e0);
		}

		pImg += cx;
		pMsk += cx;
		pDst += 212;
	}
}
*/
///// ソース改変ここまで /////
//---------------------------------------------------------------------------
IWRAM_CODE void Mode3VramEffCls(s32 cnt, u8* pEff)
{
	u16* pSrc = Mode3.buf + (Mode3.idx ^ 1) * MODE3_MAX_SCN_SIZE;
	u16* pDst = Mode3.buf + (Mode3.idx    ) * MODE3_MAX_SCN_SIZE;
	///// ソース改変ここから /////
	/*
	u16* pVrm = ((u16*)VRAM) + ((240 - 212) / 2);
	*/
	u16* pVrm = ((u16*)VRAM);
	///// ソース改変ここまで /////

	///// ソース改変ここから /////
	/*
	pEff += 212 * 160 * cnt;
	*/
	pEff += 240 * 160 * cnt;
	///// ソース改変ここまで /////

	s32 x, y;
	s32 i;

	// 4ピクセル単位アンローリング
	// 渦巻CLSで VBLANK 93 -> 86に軽減
	for(y=0; y<160; y++)
	{
// type1
		///// ソース改変ここから /////
		/*
		for(x=0; x<212; x+=4)
		*/
		for(x=0; x<240; x+=4)
		///// ソース改変ここまで /////
		{
			for(i=0; i<4; i++)
			{
				u32 eff = pEff[x+i];

				if(eff == 0)
				{
					pVrm[x+i] = pDst[x+i];
				}
				else if(eff == 0x1F)
				{
					pVrm[x+i] = pSrc[x+i];
				}
				else
				{
					u32 src = pSrc[x+i];
					u32 dst = pDst[x+i];

					u32 rbSrc = src & 0x7c1f;
					u32  gSrc = src & 0x03e0;
					u32 rbDst = dst & 0x7c1f;
					u32  gDst = dst & 0x03e0;

					u32 rb = rbDst + (((rbSrc - rbDst) * eff) >> 5);
					u32 g  =  gDst + ((( gSrc -  gDst) * eff) >> 5);

					pVrm[x+i] = (rb & 0x7c1f) | (g & 0x03e0);
				}
			}
		}
		///// ソース改変ここから /////
		/*
		pSrc += 212;
		pDst += 212;
		pVrm += 240;
		pEff += 212;
		*/
		pSrc += 240;
		pDst += 240;
		pVrm += 240;
		pEff += 240;
		///// ソース改変ここまで /////
	}
// type1 ここまで

/*
// type2
		for(x=0; x<212; x++)
		{
			u32 eff = pEff[x];

			if(eff == 0)
			{
				pVrm[x] = pDst[x];
			}
			else if(eff == 0x1F)
			{
				pVrm[x] = pSrc[x];
			}
			else
			{
				u32 src = pSrc[x];
				u32 dst = pDst[x];

				u32 rbDst = dst & 0x7c1f;
				u32  gDst = dst & 0x03e0;
				u32 rbSrc = src & 0x7c1f;
				u32  gSrc = src & 0x03e0;

				u32 rb = rbDst + (((rbSrc - rbDst) * eff) >> 5);
				u32 g  =  gDst + ((( gSrc -  gDst) * eff) >> 5);

				pVrm[x] = (rb & 0x7c1f) | (g & 0x03e0);
			}
		}

		pSrc += 212;
		pDst += 212;
		pVrm += 240;
		pEff += 212;
	}
// type2 ここまで
*/
}
//---------------------------------------------------------------------------
IWRAM_CODE void Mode3VramEffAlpha(s32 cnt)
{
	u16* pSrc = Mode3.buf + (Mode3.idx ^ 1) * MODE3_MAX_SCN_SIZE;
	u16* pDst = Mode3.buf + (Mode3.idx    ) * MODE3_MAX_SCN_SIZE;
	///// ソース改変ここから /////
	/*
	u16* pVrm = ((u16*)VRAM) + ((240 - 212) / 2);
	*/
	u16* pVrm = ((u16*)VRAM);
	///// ソース改変ここまで /////
	u32  msk  = 31 - cnt;

	s32 x, y;
	s32 i;

	// 4ピクセル単位アンローリング
	for(y=0; y<160; y++)
	{
		///// ソース改変ここから /////
		/*
		for(x=0; x<212; x+=4)
		*/
		for(x=0; x<240; x+=4)
		///// ソース改変ここまで /////
		{
			for(i=0; i<4; i++)
			{
				u32 src = pSrc[x+i];
				u32 dst = pDst[x+i];

				u32 rbSrc = src & 0x7c1f;
				u32  gSrc = src & 0x03e0;
				u32 rbDst = dst & 0x7c1f;
				u32  gDst = dst & 0x03e0;

				u32 rb = rbDst + (((rbSrc - rbDst) * msk) >> 5);
				u32 g  =  gDst + ((( gSrc -  gDst) * msk) >> 5);

				pVrm[x+i] = (rb & 0x7c1f) | (g & 0x03e0);
			}
		}

		///// ソース改変ここから /////
		/*
		pSrc += 212;
		pDst += 212;
		pVrm += 240;
		*/
		pSrc += 240;
		pDst += 240;
		pVrm += 240;
		///// ソース改変ここまで /////
	}
}
//---------------------------------------------------------------------------
IWRAM_CODE void Mode3VramCpyStep1(void)
{
	u16* pSrc = (Mode3.buf + (Mode3.idx) * MODE3_MAX_SCN_SIZE);
	///// ソース改変ここから /////
	/*
	u16* pCpy = (Mode3.cpy + (240 - 212) / 2);
	*/
	u16* pCpy = (Mode3.cpy);
	///// ソース改変ここまで /////
	s32  y;

	for(y=0; y<160; y++)
	{
		///// ソース改変ここから /////
		/*
		MemInc(pSrc, pCpy, 212*2);

		pSrc += 212;
		pCpy += 240;
		*/
		MemInc(pSrc, pCpy, 240*2);

		pSrc += 240;
		pCpy += 240;
		///// ソース改変ここまで /////
	}
}
//---------------------------------------------------------------------------
IWRAM_CODE void Mode3VramCpyStep2(void)
{
	MemIncFast(Mode3.cpy, (u16*)VRAM, 240*160*2);
}
//---------------------------------------------------------------------------
IWRAM_CODE void Mode3VramImg(u16* pImg)
{
	///// ソース改変ここから /////
	/*
	u16* pVrm = ((u16*)VRAM) + ((240 - 212) / 2);
	*/
	u16* pVrm = ((u16*)VRAM);
	///// ソース改変ここまで /////
	s32  y;

	for(y=0; y<160; y++)
	{
		///// ソース改変ここから /////
		/*
		MemInc(pImg, pVrm, 212*2);

		pImg += 212;
		pVrm += 240;
		*/
		MemInc(pImg, pVrm, 240*2);

		pImg += 240;
		pVrm += 240;
		///// ソース改変ここまで /////
	}
}
//---------------------------------------------------------------------------
IWRAM_CODE void Mode3ScrollX(s32 cnt)
{
	///// ソース改変ここから /////
	/*
	REG_BG2X = (-212 + cnt) << 8;
	*/
	REG_BG2X = (-240 + cnt) << 8;
	///// ソース改変ここまで /////
}
//---------------------------------------------------------------------------
IWRAM_CODE void Mode3FlipBuf(void)
{
	Mode3.idx ^= 1;
}
