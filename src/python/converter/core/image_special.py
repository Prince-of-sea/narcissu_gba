#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageFilter

from core.config import AppConfig

###################################################################################################
# 画像ごとの特殊変換処理
# 引数工夫すればもっと汎用化できそうではあるが、可読性や保守性を優先して個別実装とする
###################################################################################################
def convert_IMG000(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/title_off2.jpg 変換"""

    # フィルター画像のパス
    filter_image_path = cfg.res_dir / Path('filter_000_1.png')

    # 画像を読み込み
    with Image.open(nsa_extract_path) as img:

        # 240x180にリサイズ（縮小）
        img = img.resize((240, 180), Image.LANCZOS)
        
        # 上下10pxを捨てる（240x160にクロップ）
        img = img.crop((0, 10, 240, 170))

        # シャープネスを少し上げる
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=30, threshold=3))

        # フィルター画像を読み込み
        with Image.open(filter_image_path) as filter_img:
            
            # 画像にフィルターを合成
            img = Image.alpha_composite(img.convert('RGBA'), filter_img.convert('RGBA'))

        # PNGで保存
        img.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG001(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """tui/title_off.bmp 変換"""

    # フィルター画像のパス
    filter_image_path = cfg.res_dir / Path('filter_001_1.png')

    # 画像を読み込み
    with Image.open(nsa_extract_path) as img:

        # 240x180にリサイズ（縮小）
        img = img.resize((240, 180), Image.LANCZOS)
        
        # 上下10pxを捨てる（240x160にクロップ）
        img = img.crop((0, 10, 240, 170))

        # シャープネスを少し上げる
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=30, threshold=3))

        # フィルター画像を読み込み
        with Image.open(filter_image_path) as filter_img:
            
            # 画像にフィルターを合成
            img = Image.alpha_composite(img.convert('RGBA'), filter_img.convert('RGBA'))

        # PNGで保存
        img.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG015(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/byoin_heya_yu2.jpg 変換"""

    # 画像を読み込み
    with Image.open(nsa_extract_path) as img:

        # 240x180にリサイズ（縮小）
        img = img.resize((240, 180), Image.LANCZOS)

        # 上12px、下8pxを捨てる（240x160にクロップ）
        img = img.crop((0, 12, 240, 172))

        # シャープネスを少し上げる
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # PNGで保存
        img.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_fit_frame(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """フレームに合わせてリサイズ変換(汎用)"""

    # 元画像を読み込み
    with Image.open(nsa_extract_path) as img:
        img = img.convert("RGB")
        
        # 元画像の左上の色をもとに240x160の新画像を作成
        bg_color = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color)
        
        # 元画像の(1,145)から(800,349)を切り出し
        img_cropped = img.crop((1, 145, 800, 349))
        
        # 240x60に縮小
        img_resized = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)
        
        # 新画像の(1,32)にはりつけ
        img_new.paste(img_resized, (1, 32))
        
        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # 保存
        img_new.save(temppng_path, "PNG")
    
    return


###################################################################################################
def convert_default(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """デフォルト変換"""

    # 画像を読み込み
    with Image.open(nsa_extract_path) as img:

        # 240x180にリサイズ（縮小）
        img = img.resize((240, 180), Image.LANCZOS)
        
        # 上下10pxを捨てる（240x160にクロップ
        img = img.crop((0, 10, 240, 170))

        # シャープネスを少し上げる
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=30, threshold=3))

        # PNGで保存
        img.save(temppng_path, "PNG")

    return