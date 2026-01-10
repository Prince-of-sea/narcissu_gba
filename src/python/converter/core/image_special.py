#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageFilter


def convert_default(nsa_extract_path: Path, temppng_path: Path):
    """デフォルト変換"""

    # 1. 画像を読み込み
    with Image.open(nsa_extract_path) as img:

        # 2. 240x180にリサイズ（縮小）
        img = img.resize((240, 180), Image.LANCZOS)
        
        # 3. 上下10pxを捨てる（240x160にクロップ）
        # cropの引数は (左, 上, 右, 下)
        img = img.crop((0, 10, 240, 170))

        # 3.5. シャープネスを少し上げる
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=30, threshold=3))

        # 4. PNGで保存
        img.save(temppng_path, "PNG")

    return
