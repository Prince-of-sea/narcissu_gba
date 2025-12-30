# imgファイルの先頭に、画像の縦、横のパラメータを追加
from pathlib import Path
import subprocess
import struct
from PIL import Image

# ---------------------------------------------------------------------------
# ここGPL2.0なんでこのまま使うとgpl2.0になる

def Param(i, f):
	# 元画像のサイズだけ取得
	p = Image.open(i)
	iw, ih = p.size
	p.close()

	# imgファイルを全て読み込む
	s = open(f, "rb")
	x = s.read()
	s.close()

	# サイズ情報をファイル先頭に付与
	d = open(f, 'wb')
	d.write(struct.pack('HH', iw, ih))
	d.write(x)
	d.close()

# ---------------------------------------------------------------------------
# f = sys.argv[1]
# 
# print("img_para... " + f)
# Param(f)
IMG_LIST = [
	['img010','e/amazora02.jpg'],
	['img011','e/amazora03.jpg'],
	['img012','e/b.jpg'],
	['img013','e/byoin7_rouka.jpg'],
	['img014','e/byoin_chusyajo.jpg'],
	['img015','e/byoin_heya_yu2.jpg'],
	['img016','e/byoin_rouka.jpg'],
	['img017','e/c00.jpg'],
	['img018','e/c001.jpg'],
	['img019','e/c001a.jpg'],
	['img020','e/c001b.jpg'],
	['img021','e/c002.jpg'],
	['img022','e/c003.jpg'],
	['img023','e/c004.jpg'],
	['img024','e/c005.jpg'],
	['img025','e/c0052.jpg'],
	['img026','e/c02.jpg'],
	['img027','e/c03.jpg'],
	['img028','e/c032.jpg'],
	['img029','e/c033.jpg'],
	['img030','e/c04.jpg'],
	['img031','e/c042.jpg'],
	['img032','e/car_byoin_chusyajo.jpg'],
	['img033','e/car_byoin_chusyajo_yoru.jpg'],
	['img034','e/car_byoin_chusyajo_yoru_ame.jpg'],
	['img035','e/car_michi01.jpg'],
	['img036','e/car_naname_michi01.jpg'],
	['img037','e/carkey.jpg'],
	['img038','e/chara_001.jpg'],
	['img039','e/chara_0012.jpg'],
	['img040','e/chara_0013.jpg'],
	['img041','e/chara_0013b.jpg'],
	['img042','e/chara_k01.jpg'],
	['img043','e/chara_k02.jpg'],
	['img044','e/chusha_hamabe_yu.jpg'],
	['img045','e/chusha_michi2_yoru.jpg'],
	['img046','e/chusha_michi2_yu.jpg'],
	['img047','e/chusha_michi_ame_yoru.jpg'],
	['img048','e/coin_tennai.jpg'],
	['img049','e/danwa.jpg'],
	['img050','e/danwa_ame.jpg'],
	['img051','e/danwa_yoru.jpg'],
	['img052','e/gs.jpg'],
	['img053','e/hashigeta.jpg'],
	['img054','e/hiki_kosoku2.jpg'],
	['img055','e/hiki_shigai_yu.jpg'],
	['img056','e/image01.jpg'],
	['img057','e/imege03.jpg'],
	['img058','e/imege04.jpg'],
	['img059','e/imege05.jpg'],
	['img060','e/imege06.jpg'],
	['img061','e/imege07.jpg'],
	['img062','e/imege072.jpg'],
	['img063','e/imege09.jpg'],
	['img064','e/imege92.jpg'],
	['img065','e/imege93.jpg'],
	['img066','e/imege94.jpg'],
	['img067','e/imege95.jpg'],
	['img068','e/imege96.jpg'],
	['img069','e/imege97.jpg'],
	['img070','e/joku_kosoku.jpg'],
	['img071','e/joku_kosoku_yu.jpg'],
	['img072','e/joku_shigaichi.jpg'],
	['img073','e/naname_inaka_ame2.jpg'],
	['img074','e/naname_inaka_yoru.jpg'],
	['img075','e/naname_inaka_yu.jpg'],
	['img076','e/naname_machi.jpg'],
	['img077','e/naname_machi2.jpg'],
	['img078','e/naname_machi2_yoru.jpg'],
	['img079','e/naname_michi.jpg'],
	['img080','e/naname_michi_yoru.jpg'],
	['img081','e/naname_yuki.jpg'],
	['img082','e/nar01.jpg'],
	['img083','e/nar01c.jpg'],
	['img084','e/nar01d.jpg'],
	['img085','e/narcissu_b.jpg'],
	['img086','e/narcissu_yoru_ame.jpg'],
	['img087','e/pachi.jpg'],
	['img088','e/setsumi_kaisou.jpg'],
	['img089','e/shanai_inaka.jpg'],
	['img090','e/shanai_michi01.jpg'],
	['img091','e/shanai_michi01_yoru.jpg'],
	['img092','e/shanai_michi01_yu.jpg'],
	['img093','e/shanai_michi01b.jpg'],
	['img094','e/shanai_michi02_yoru.jpg'],
	['img095','e/shanai_michi03_yu.jpg'],
	['img096','e/shanai_michi04.jpg'],
	['img097','e/sora01.jpg'],
	['img098','e/sora02.jpg'],
	['img099','e/sora03.jpg'],
	['img100','e/sora06.jpg'],
	['img101','e/sora07.jpg'],
	['img102','e/sora_ame01.jpg'],
	['img103','e/sora_ame01b.jpg'],
	['img104','e/sora_ame02.jpg'],
	['img105','e/sora_ame03.jpg'],
	['img106','e/sora_yoru01.jpg'],
	['img107','e/sora_yu.jpg'],
	['img108','e/soukou.jpg'],
	['img109','e/soukou_machi.jpg'],
	['img110','e/soukou_machi_yoru.jpg'],
	['img111','e/soukou_machi_yu.jpg'],
	['img112','e/soukou_yoru.jpg'],
	['img113','e/st00.jpg'],
	['img114','e/st01.jpg'],
	['img115','e/st02.jpg'],
	['img116','e/st03.jpg'],
	['img117','e/st04.jpg'],
	['img118','e/st05.jpg'],
	['img119','e/tv_hana.jpg'],
	['img120','e/umibe_yoru.jpg'],
	['img121','e/w.jpg'],
	['img122','e/yakkyoku.jpg'],
	['img123','e/yuki_kohan.jpg'],
	['img124','e/yukizora.jpg'],
	['img125','tui2/c0432.bmp'],
	['img126','tui2/c044.bmp'],
	['img127','tui2/c0442.bmp'],
	['img128','tui2/c045.bmp'],
	['img129','tui2/c046.bmp'],
	['img130','tui2/c047.bmp'],
	['img131','tui2/c049.bmp'],
	['img132','tui2/cat02.bmp'],
	['img133','tui2/cat03.bmp'],
	['img134','tui2/cat05.bmp'],
	['img135','tui2/cat06.bmp'],
	['img136','tui2/cat07.bmp'],
	['img137','tui2/cat072.bmp'],
	['img138','tui2/cat073.bmp'],
	['img139','tui/imege98.bmp'],
	['img140','tui/naname_inaka_yoru2.bmp'],
	['img141','yobi/car_byoin_chusyajo_yu.bmp'],
	['img142','yobi/cat03.bmp'],
	['img143','yobi/cat09.bmp'],
]

GRIT_EXE = Path(r"D:/132_shuumatsu_gba/gbfs/exe/img/grit.exe")

input_dir = Path(r'D:/132_shuumatsu_gba/__test_ex')
temp_dir = Path(r'D:/132_shuumatsu_gba/__temp_ex')


def main():

	for p in IMG_LIST:
		input_path = (input_dir / Path(p[1]))
		temppng_path = (temp_dir / f'{p[0]}.png')
		tempbin_path = (temp_dir / f'{p[0]}.img.bin')
		output_path = (temp_dir / f'{p[0]}.bin')

		# リサイズ@pil
		# 1. 画像を読み込み
		with Image.open(input_path) as img:
			# 2. 240x180にリサイズ（縮小）
			img_resized = img.resize((240, 180), Image.LANCZOS)
			
			# 3. 上下10pxを捨てる（240x160にクロップ）
			# cropの引数は (左, 上, 右, 下)
			left = 0
			top = 10
			right = 240
			bottom = 180 - 10
			img_cropped = img_resized.crop((left, top, right, bottom))

			# 4. PNGで保存
			img_cropped.save(temppng_path, "PNG")

		# 変換@grit
		cmd = [GRIT_EXE, temppng_path, '-gb', '-gB16', '-ftb', '-gu16', '-fh!']
		subprocess.run(cmd, cwd = temp_dir)

		# パラメータ@Param
		Param(temppng_path, tempbin_path)

		# png削除
		temppng_path.unlink()

		# デバッグ:元々あったら消す
		if output_path.exists(): output_path.unlink()

		tempbin_path.rename(output_path)


		

	return

main()