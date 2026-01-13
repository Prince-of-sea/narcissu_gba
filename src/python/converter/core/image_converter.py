#!/usr/bin/env python3
import concurrent.futures
import subprocess
import struct
from pathlib import Path
from PIL import Image

from core.config import AppConfig
from .image_special import convert_IMG000
from .image_special import convert_IMG001
from .image_special import convert_IMG015
from .image_special import convert_IMG018_023
from .image_special import convert_IMG067
from .image_special import convert_IMG068_069
from .image_special import convert_IMG082_084
from .image_special import convert_IMG139
from .image_special import convert_none_background
from .image_special import convert_gray_background
from .image_special import convert_fit_frame
from .image_special import convert_default
from .paths import IMG_LIST


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


def convert_image_parallel(cfg: AppConfig, img_info: list[int, str, str]) -> None:
    """画像の並列変換処理"""

    p_relative_path = img_info[1]
    p_convert_mode = img_info[2]

    nsa_extract_path = (cfg.nsa_extract_dir / Path(p_relative_path))

    p_index = str(img_info[0]).zfill(3)
    temppng_path = (cfg.convert_dir / f'img{p_index}.png')
    tempbin_path = (cfg.convert_dir / f'img{p_index}.img.bin')
    output_path = (cfg.convert_dir / f'img{p_index}.bin')

    # arc_unpackerはbmpをpngでデコードするのでパスもそれに合わせる
    if (nsa_extract_path.suffix == '.bmp'):
        nsa_extract_path = (nsa_extract_path.with_suffix('.png'))

    # PILを使って画像をリサイズ(画像ごとの特殊モードを利用)
    match p_convert_mode:
        case 'special_000':
            convert_IMG000(nsa_extract_path, temppng_path, cfg)
        case 'special_001':
            convert_IMG001(nsa_extract_path, temppng_path, cfg)
        case 'special_015':
            convert_IMG015(nsa_extract_path, temppng_path, cfg)
        case 'special_018_023':
            convert_IMG018_023(nsa_extract_path, temppng_path, cfg)
        case 'special_067':
            convert_IMG067(nsa_extract_path, temppng_path, cfg)
        case 'special_068_069':
            convert_IMG068_069(nsa_extract_path, temppng_path, cfg)
        case 'special_082_084':
            convert_IMG082_084(nsa_extract_path, temppng_path, cfg)
        case 'special_139':
            convert_IMG139(nsa_extract_path, temppng_path, cfg)
        case 'gray_background':
            convert_gray_background(nsa_extract_path, temppng_path, cfg)
        case 'none_background':
            convert_none_background(nsa_extract_path, temppng_path, cfg)
            return
        case 'fit_frame':
            convert_fit_frame(nsa_extract_path, temppng_path, cfg)
        case _:
            convert_default(nsa_extract_path, temppng_path, cfg)

    # grit.exeを使って変換
    run_grit(cfg, temppng_path)

    # 末尾に独自データを追記
    append_footer_data(temppng_path, tempbin_path)

    if (cfg.debug_mode):
        # デバッグ用に中間pngファイルをdebug_dirにコピー
        debug_png_path = cfg.debug_dir / f'img{p_index}.png'
        temppng_path.replace(debug_png_path)
    else:
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