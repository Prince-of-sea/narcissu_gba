#include "info.h"

//---------------------------------------------------------------------------
ROM_DATA s32 InfoImg[] = {
	///// ソース改変ここから /////
	/*
	8,		// BACK1
	46,		// BACK2
	36,		// BACK3
	29,		// BACK4
	37,		// BACK5
	47,		// BACK6
	28,		// BACK7
	7,		// BACK8
	39,		// BACK9
	138,	// BADIRH
//	2,		// BLACK
	59,		// CBAFTER
	56,		// CBBEFORE
	90,		// CHIEH1
	91,		// CHIEH2
	92,		// CHIEH3
	93,		// CHIEH4
	125,	// CHIEKAKO
	94,		// CHIEKISS
	67,		// CHIEMOGU
	69,		// DOMKANA
//	135,	// END
//	95,		// FRI
	48,		// FURIIRO
	127,	// FURIKOR
	14,		// GROCHIE
	15,		// GROSHIGE
	145,	// HAPPYIRH
	143,	// HAPPYKOR
	144,	// HAPPYMDR
	107,	// HIZAKAO
	16,		// HOKERUKI
	84,		// IRHHOSSA
	113,	// IROH1
	114,	// IROH2
	115,	// IROH3
	116,	// IROH4
	117,	// IROKISS
	9,		// JUGYOCHI
	10,		// JUGYOKAO
	98,		// KAGIIRO
	118,	// KANAH1
	119,	// KANAH2
	120,	// KANAH3
	121,	// KANAH4
	61,		// KANAIRO
	122,	// KANAKISS
	101,	// KAOH1
	102,	// KAOH2
	103,	// KAOH3
	104,	// KAOH4
	105,	// KAOH4B
	106,	// KAOKISS
	146,	// KCYOZORA
	85,		// KMIOROSI
	54,		// KOKERUKI
	89,		// KOUEN
	139,	// KURAKANA
	137,	// KURAKOR
	142,	// KURARKTH
//	0,		// LOGO1
//	1,		// LOGO2
	68,		// MADOKAO
	83,		// MADOMI1
	82,		// MADOMI2
	109,	// MIDOH1
	110,	// MIDOH2
	111,	// MIDOH3
	112,	// MIDOH4
	17,		// MIDOHON
	108,	// MIDOKISS
	97,		// MIDOMEGA
	128,	// MIDOMIO
//	6,		// MON
	62,		// MUSATWO
	12,		// OKUIRO
	13,		// OKUKANA
	100,	// ONBUCHIE
	124,	// RKHEIWA
	132,	// ROCKETKN
	74,		// RUKIGYU
	76,		// RUKIH1
	77,		// RUKIH2
	78,		// RUKIH3
	79,		// RUKIH4
	141,	// RUKIKISS
//	123,	// SAT
	126,	// SCCHIE
	99,		// SCKAIWA
	58,		// SEITOH1
	87,		// SEITOH2
	11,		// SORA
	81,		// TEREKAO
//	80,		// THU
//	990,	// TITLEX
//	18,		// TOPFONT
//	55,		// TUE
//	66,		// WED
	75,		// YUBIIRO
//	991,	// TITLE3
	*/
	 10,		// e/amazora02.jpg
	 11,		// e/amazora03.jpg
	 12,		// e/b.jpg
	 13,		// e/byoin7_rouka.jpg
	 14,		// e/byoin_chusyajo.jpg
	 15,		// e/byoin_heya_yu2.jpg
	 16,		// e/byoin_rouka.jpg
	 32,		// e/car_byoin_chusyajo.jpg
	 33,		// e/car_byoin_chusyajo_yoru.jpg
	 34,		// e/car_byoin_chusyajo_yoru_ame.jpg
	 35,		// e/car_michi01.jpg
	 36,		// e/car_naname_michi01.jpg
	 37,		// e/carkey.jpg
	 38,		// e/chara_001.jpg
	 39,		// e/chara_0012.jpg
	 40,		// e/chara_0013.jpg
	 42,		// e/chara_k01.jpg
	 43,		// e/chara_k02.jpg
	 44,		// e/chusha_hamabe_yu.jpg
	 45,		// e/chusha_michi2_yoru.jpg
	 46,		// e/chusha_michi2_yu.jpg
	 47,		// e/chusha_michi_ame_yoru.jpg
	 48,		// e/coin_tennai.jpg
	 49,		// e/danwa.jpg
	 50,		// e/danwa_ame.jpg
	 51,		// e/danwa_yoru.jpg
	 52,		// e/gs.jpg
	 53,		// e/hashigeta.jpg
	 54,		// e/hiki_kosoku2.jpg
	 55,		// e/hiki_shigai_yu.jpg
	 56,		// e/image01.jpg
	 57,		// e/imege03.jpg
	 58,		// e/imege04.jpg
	 59,		// e/imege05.jpg
	 60,		// e/imege06.jpg
	 61,		// e/imege07.jpg
	 62,		// e/imege072.jpg
	 63,		// e/imege09.jpg
	 64,		// e/imege92.jpg
	 65,		// e/imege93.jpg
	 66,		// e/imege94.jpg
	 67,		// e/imege95.jpg
	 68,		// e/imege96.jpg
	 69,		// e/imege97.jpg
	 70,		// e/joku_kosoku.jpg
	 71,		// e/joku_kosoku_yu.jpg
	 72,		// e/joku_shigaichi.jpg
	 73,		// e/naname_inaka_ame2.jpg
	 74,		// e/naname_inaka_yoru.jpg
	 75,		// e/naname_inaka_yu.jpg
	 76,		// e/naname_machi.jpg
	 77,		// e/naname_machi2.jpg
	 78,		// e/naname_machi2_yoru.jpg
	 79,		// e/naname_michi.jpg
	 80,		// e/naname_michi_yoru.jpg
	 81,		// e/naname_yuki.jpg
	 82,		// e/nar01.jpg
	 83,		// e/nar01c.jpg
	 84,		// e/nar01d.jpg
	 85,		// e/narcissu_b.jpg
	 86,		// e/narcissu_yoru_ame.jpg
	 87,		// e/pachi.jpg
	 88,		// e/setsumi_kaisou.jpg
	 89,		// e/shanai_inaka.jpg
	 90,		// e/shanai_michi01.jpg
	 91,		// e/shanai_michi01_yoru.jpg
	 92,		// e/shanai_michi01_yu.jpg
	 93,		// e/shanai_michi01b.jpg
	 94,		// e/shanai_michi02_yoru.jpg
	 95,		// e/shanai_michi03_yu.jpg
	 96,		// e/shanai_michi04.jpg
	 97,		// e/sora01.jpg
	 98,		// e/sora02.jpg
	 99,		// e/sora03.jpg
	100,		// e/sora06.jpg
	101,		// e/sora07.jpg
	102,		// e/sora_ame01.jpg
	103,		// e/sora_ame01b.jpg
	104,		// e/sora_ame02.jpg
	105,		// e/sora_ame03.jpg
	106,		// e/sora_yoru01.jpg
	107,		// e/sora_yu.jpg
	108,		// e/soukou.jpg
	109,		// e/soukou_machi.jpg
	110,		// e/soukou_machi_yoru.jpg
	111,		// e/soukou_machi_yu.jpg
	112,		// e/soukou_yoru.jpg
	119,		// e/tv_hana.jpg
	120,		// e/umibe_yoru.jpg
	121,		// e/w.jpg
	122,		// e/yakkyoku.jpg
	123,		// e/yuki_kohan.jpg
	124,		// e/yukizora.jpg
	140,		// tui/naname_inaka_yoru2.bmp
	141,		// yobi/car_byoin_chusyajo_yu.bmp
	///// ソース改変ここまで /////
};

// 昇順（アーカイブ順でなく）
ROM_DATA s32 InfoBgm[] = {
	///// ソース改変ここから /////
	/*
	1,		// SILENCE
	0,		// 01_OP03
	5,		// 02_OP06
	10,		// 03_OP08
	8,		// 04_OP11
	14,		// 05_OP12
	12,		// 06_OP13
	13,		// 07_OP14
	6,		// 08_OP16
	9,		// 09_OP17
	7,		// 10_OP18
	4,		// 12_OP20_
	16,		// 13_OP21
	17,		// 14_OP22
	2,		// 15_OP23
	15,		// 16_OP28
	18,		// 17_OP29
	20,		// 18_OP30
//	3,		// RADIO
//	11,		// RADIONZ
	*/
	10,		// bgm/3_12.mp3
	11,		// bgm/a01.mp3
	12,		// bgm/e02.mp3
	13,		// bgm/n03.mp3
	14,		// bgm/n04.mp3
	15,		// bgm/n05.mp3
	16,		// bgm/o01.mp3
	17,		// bgm/o012.mp3
	18,		// bgm/o02.mp3
	19,		// bgm/sen02.mp3
	20,		// bgm/sen02_20.mp3
	21,		// tui2/e01.mp3
	22,		// tui/sen032.mp3
	///// ソース改変ここまで /////
};

ROM_DATA s32 InfoFmx[] = {
	///// ソース改変ここから /////
	/*
	0,		// TIMEBELL
	1,		// OD_M
	2,		// OD_P
	3,		// PAPER
	4,		// SD_M
	5,		// SD_P
	6,		// IDO
	7,		// DOM
	8,		// OD_WO
	9,		// OD_WC
	10,		// PAPERBAG
	11,		// OD_MO
	*/
	10,		// se/amadare.wav
	11,		// se/autodoor.wav
	12,		// se/c-1.wav
	13,		// se/c-2.wav
	14,		// se/camera.wav
	15,		// se/car1.wav
	16,		// se/car2.wav
	17,		// se/car3.wav
	18,		// se/car_s.wav
	19,		// se/car_s3.wav
	20,		// se/car_s4.wav
	21,		// se/car_start.wav
	22,		// se/car_start2.wav
	23,		// se/close.wav
	24,		// se/coin.wav
	25,		// se/coin2.wav
	26,		// se/coin_d.wav
	27,		// se/engin_s.wav
	28,		// se/engine_start.wav
	29,		// se/faan1_b.wav
	30,		// se/g_crash2.wav
	31,		// se/hayaasi.wav
	32,		// se/kati.wav
	33,		// se/kaze13.wav
	34,		// se/kaze3.wav
	35,		// se/kaze3_2.wav
	36,		// se/key2.wav
	37,		// se/knocking.wav
	38,		// se/nami02b.wav
	39,		// se/nami3.wav
	40,		// se/open.wav
	41,		// se/pachinko1.wav
	42,		// se/rain01.wav
	43,		// se/rain_1.wav
	44,		// se/rain_12.wav
	45,		// se/umi13.wav
	46,		// se/umitori.wav
	47,		// se/water_x2.wav
	48,		// se/z42r.wav
	///// ソース改変ここまで /////
};

//---------------------------------------------------------------------------
void InfoInit(void)
{
	// EMPTY
}
//---------------------------------------------------------------------------
s32 InfoGetImg(s32 idx)
{
	_ASSERT(idx < INFO_MAX_IMG_CNT);

	return InfoImg[idx];
}
//---------------------------------------------------------------------------
s32 InfoGetBgm(s32 idx)
{
	_ASSERT(idx < INFO_MAX_BGM_CNT);

	return InfoBgm[idx];
}
//---------------------------------------------------------------------------
s32 InfoGetFmx(s32 idx)
{
	_ASSERT(idx < INFO_MAX_FMX_CNT);

	return InfoFmx[idx];
}
//---------------------------------------------------------------------------
// キャラクタ番号からマスク番号を取得します
s32 InfoGetMskNo(s32 no)
{
	///// ソース改変ここから /////
	/*
	// chieko
	if(no == 41 || no == 43 || no == 44 || no == 45 || no == 63 || no == 96)
	{
		return 0;
	}

	// chihiro
	if(no == 24 || no == 26 || no == 27)
	{
		return 1;
	}

	// iroha
	if(no == 49 || no == 50 || no == 51)
	{
		return 2;
	}

	// kana
	if(no == 52 || no == 53 || no == 86 || no == 130 || no == 131)
	{
		return 3;
	}

	// kaori
	if(no == 19 || no == 20 || no == 21 || no == 57)
	{
		return 4;
	}

	// midori
	if(no == 22 || no == 23 || no == 25 || no == 38 || no == 60 || no == 129)
	{
		return 5;
	}

	// ruki
	if(no == 30 || no == 33 || no == 34 || no == 72 || no == 73)
	{
		return 6;
	}

	// shige
	if(no == 40 || no == 42 || no == 64 || no == 65 || no == 88)
	{
		return 7;
	}

	// tahiro
	if(no == 31 || no == 32 || no == 35 || no == 70 || no == 71)
	{
		return 8;
	}


	SystemError("[Err] InfoGetMsk no=%x\n", no);
	*/
	///// ソース改変ここまで /////

	return 0;
}
