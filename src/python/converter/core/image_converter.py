#!/usr/bin/env python3
import concurrent.futures
import subprocess
import struct
from pathlib import Path
from PIL import Image

from core.config import AppConfig
from .paths import IMG_LIST


#####後で消す#####
# GRIT_EXE = Path(r"D:/132_shuumatsu_gba/gbfs/exe/img/grit.exe")
# nsa_extract_dir = Path(r'D:/132_shuumatsu_gba/__test_ex/arc~.nsa')
# convert_dir = Path('D:/132_shuumatsu_gba/gbfs/data/tmp/')

# arc_unpackerはbmpをpngでデコードするので治す

##############

# def compress_image(img):
#     """圧縮処理"""
#     pass


# def crop_image(img):
#     """クロップ処理"""
#     pass


# def apply_common_effects(img):
#     """汎用特殊効果 (アンシャープマスク等)"""
#     pass


# def apply_special_effects(img):
#     """個別特殊効果 (黒塗り等)"""
#     pass


# def reduce_color(img):
#     """減色処理"""
#     pass


# def export_temp_file(img, out_path: str):
#     """一時ファイルとして保存"""
#     pass


def run_grit(cfg: AppConfig, in_path: Path) -> None:
    """grit.exe を使って変換"""

    cmd = [cfg.grit_exe, in_path, '-gb', '-gB16', '-ftb', '-gu16', '-fh!']
    subprocess.run(cmd, cwd = cfg.convert_dir)
    
    return


def append_footer_data(i: Path, f: Path) -> None:
    """末尾に独自データを追記"""

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

    return


def convert_image_parallel(cfg: AppConfig, img_info: list[int, str]) -> None:
    """画像の並列変換処理"""

    p_relative_path = img_info[1]
    nsa_extract_path = (cfg.nsa_extract_dir / Path(p_relative_path))

    p_index = str(img_info[0]).zfill(3)
    temppng_path = (cfg.convert_dir / f'img{p_index}.png')
    tempbin_path = (cfg.convert_dir / f'img{p_index}.img.bin')
    output_path = (cfg.convert_dir / f'img{p_index}.bin')

    # arc_unpackerはbmpをpngでデコードするのでパスもそれに合わせる
    if (nsa_extract_path.suffix == '.bmp'):
        nsa_extract_path = (nsa_extract_path.with_suffix('.png'))

    # リサイズ@pil - ここも関数分け予定
    # 1. 画像を読み込み
    with Image.open(nsa_extract_path) as img:

        # 2. 240x180にリサイズ（縮小）
        img = img.resize((240, 180), Image.LANCZOS)
        
        # 3. 上下10pxを捨てる（240x160にクロップ）
        # cropの引数は (左, 上, 右, 下)
        img = img.crop((0, 11, 240, 171))

        # X. この辺に画像ごとの個別処理追加予定

        # 4. PNGで保存
        img.save(temppng_path, "PNG")

    # grit.exeを使って変換
    run_grit(cfg, temppng_path)

    # 末尾に独自データを追記
    append_footer_data(temppng_path, tempbin_path)

    # 変換し終わったpngファイルを削除
    temppng_path.unlink()

    # 競合するファイルがあれば削除
    if output_path.exists():
        output_path.unlink()
    
    # 変換したbinファイルをrenameして出力パスに移動
    tempbin_path.rename(output_path)

    return


def convert_images(cfg: AppConfig) -> None:
    """画像の全変換処理"""

    # 並列ファイル変換
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for img_info in IMG_LIST:
            # 画像の並列変換処理
            futures.append(executor.submit(
                convert_image_parallel, cfg, img_info))
        
        # gui対応時にはプログレスバー用に改良予定
        concurrent.futures.as_completed(futures)

    return