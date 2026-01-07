#!/usr/bin/env python3
from pathlib import Path
from PIL import Image


def convert_default(nsa_extract_path: Path, temppng_path: Path):
    """デフォルト変換"""

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

    return