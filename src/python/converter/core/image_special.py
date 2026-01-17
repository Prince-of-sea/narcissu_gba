#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps

from core.config import AppConfig

###################################################################################################
# 画像ごとの特殊変換処理
# 引数工夫すればもっと汎用化できそうではあるが、可読性や保守性を優先して個別実装とする
###################################################################################################
def convert_IMG000(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/title_off2.jpg 変換"""

    # フィルター画像のパス
    filter_image_path = cfg.image_filter_dir / Path('filter_000_1.bin')

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
    filter_image_path = cfg.image_filter_dir / Path('filter_001_1.bin')

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
def convert_IMG003(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """sys/mini_title.bmp 変換(2章)"""

    # 拡大率
    SUBTITLE_SCALE = 0.66

    # 字幕用の画像パス
    subtitle_image_path = cfg.nsa_extract_dir / Path('yobi') / Path('system') / Path('chapter02.png')

    # 元画像を読み込み
    with Image.open(nsa_extract_path) as img:
        img = img.convert("RGB")
        
        # 元画像の左上の色をもとに240x160の新画像を作成
        bg_color = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color)
        
        # 元画像の(0,145)から(800,349)を切り出し
        img_cropped = img.crop((0, 145, 800, 349))
        
        # 240x61に縮小
        img_resized = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)
        
        # 新画像の(0,32)にはりつけ
        img_new.paste(img_resized, (0, 32))
        
        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # 字幕用の画像を読み込んで処理
        with Image.open(subtitle_image_path) as img_subtitle:

            # 3枚目（本体）と4枚目（マスク）を直値で切り出し
            img_subtitle_body = img_subtitle.crop((498, 0, 747, 23)).convert("RGBA")
            img_subtitle_mask = img_subtitle.crop((747, 0, 996, 23)).convert("L")

            # マスクの白黒を反転させる
            img_subtitle_mask = ImageOps.invert(img_subtitle_mask)

            # マスクを適用
            img_subtitle_body.putalpha(img_subtitle_mask)

            # その場のサイズ（.width / .height）にSUBTITLE_SCALEを掛けてリサイズ
            subtitle_new_size = (int(img_subtitle_body.width * SUBTITLE_SCALE), int(img_subtitle_body.height * SUBTITLE_SCALE))
            img_subtitle_resized = img_subtitle_body.resize(subtitle_new_size, Image.Resampling.LANCZOS)

            # img_newの(75, 55)に貼り付け
            # 第3引数に自身を指定して透過を有効にする
            img_new.paste(img_subtitle_resized, (75, 55), img_subtitle_resized)

        # 保存
        img_new.save(temppng_path, "PNG")
    
    return


###################################################################################################
def convert_IMG004(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """sys/mini_title.bmp 変換(3章)"""

    # 拡大率
    SUBTITLE_SCALE = 0.66

    # 字幕用の画像パス
    subtitle_image_path = cfg.nsa_extract_dir / Path('yobi') / Path('system') / Path('chapter03.png')

    # 元画像を読み込み
    with Image.open(nsa_extract_path) as img:
        img = img.convert("RGB")
        
        # 元画像の左上の色をもとに240x160の新画像を作成
        bg_color = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color)
        
        # 元画像の(0,145)から(800,349)を切り出し
        img_cropped = img.crop((0, 145, 800, 349))
        
        # 240x61に縮小
        img_resized = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)
        
        # 新画像の(0,32)にはりつけ
        img_new.paste(img_resized, (0, 32))
        
        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # 字幕用の画像を読み込んで処理
        with Image.open(subtitle_image_path) as img_subtitle:

            # 3枚目（本体）と4枚目（マスク）を直値で切り出し
            img_subtitle_body = img_subtitle.crop((498, 0, 747, 23)).convert("RGBA")
            img_subtitle_mask = img_subtitle.crop((747, 0, 996, 23)).convert("L")

            # マスクの白黒を反転させる
            img_subtitle_mask = ImageOps.invert(img_subtitle_mask)

            # マスクを適用
            img_subtitle_body.putalpha(img_subtitle_mask)

            # その場のサイズ（.width / .height）にSUBTITLE_SCALEを掛けてリサイズ
            subtitle_new_size = (int(img_subtitle_body.width * SUBTITLE_SCALE), int(img_subtitle_body.height * SUBTITLE_SCALE))
            img_subtitle_resized = img_subtitle_body.resize(subtitle_new_size, Image.Resampling.LANCZOS)

            # img_newの(75, 55)に貼り付け
            # 第3引数に自身を指定して透過を有効にする
            img_new.paste(img_subtitle_resized, (75, 55), img_subtitle_resized)

        # 保存
        img_new.save(temppng_path, "PNG")
    
    return

###################################################################################################
def convert_IMG005(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """sys/mini_title.bmp 変換(4章)"""

    # 拡大率
    SUBTITLE_SCALE = 0.66

    # 字幕用の画像パス
    subtitle_image_path = cfg.nsa_extract_dir / Path('yobi') / Path('system') / Path('chapter04.png')

    # 元画像を読み込み
    with Image.open(nsa_extract_path) as img:
        img = img.convert("RGB")
        
        # 元画像の左上の色をもとに240x160の新画像を作成
        bg_color = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color)
        
        # 元画像の(0,145)から(800,349)を切り出し
        img_cropped = img.crop((0, 145, 800, 349))
        
        # 240x61に縮小
        img_resized = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)
        
        # 新画像の(0,32)にはりつけ
        img_new.paste(img_resized, (0, 32))
        
        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # 字幕用の画像を読み込んで処理
        with Image.open(subtitle_image_path) as img_subtitle:

            # 3枚目（本体）と4枚目（マスク）を直値で切り出し
            img_subtitle_body = img_subtitle.crop((498, 0, 747, 23)).convert("RGBA")
            img_subtitle_mask = img_subtitle.crop((747, 0, 996, 23)).convert("L")

            # マスクの白黒を反転させる
            img_subtitle_mask = ImageOps.invert(img_subtitle_mask)

            # マスクを適用
            img_subtitle_body.putalpha(img_subtitle_mask)

            # その場のサイズ（.width / .height）にSUBTITLE_SCALEを掛けてリサイズ
            subtitle_new_size = (int(img_subtitle_body.width * SUBTITLE_SCALE), int(img_subtitle_body.height * SUBTITLE_SCALE))
            img_subtitle_resized = img_subtitle_body.resize(subtitle_new_size, Image.Resampling.LANCZOS)

            # img_newの(75, 55)に貼り付け
            # 第3引数に自身を指定して透過を有効にする
            img_new.paste(img_subtitle_resized, (75, 55), img_subtitle_resized)

        # 保存
        img_new.save(temppng_path, "PNG")
    
    return


###################################################################################################
def convert_IMG006(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """sys/mini_title.bmp 変換(5章)"""

    # 拡大率
    SUBTITLE_SCALE = 0.66

    # 字幕用の画像パス
    subtitle_image_path = cfg.nsa_extract_dir / Path('yobi') / Path('system') / Path('chapter05.png')

    # 元画像を読み込み
    with Image.open(nsa_extract_path) as img:
        img = img.convert("RGB")
        
        # 元画像の左上の色をもとに240x160の新画像を作成
        bg_color = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color)
        
        # 元画像の(0,145)から(800,349)を切り出し
        img_cropped = img.crop((0, 145, 800, 349))
        
        # 240x61に縮小
        img_resized = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)
        
        # 新画像の(0,32)にはりつけ
        img_new.paste(img_resized, (0, 32))
        
        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # 字幕用の画像を読み込んで処理
        with Image.open(subtitle_image_path) as img_subtitle:

            # 3枚目（本体）と4枚目（マスク）を直値で切り出し
            img_subtitle_body = img_subtitle.crop((498, 0, 747, 23)).convert("RGBA")
            img_subtitle_mask = img_subtitle.crop((747, 0, 996, 23)).convert("L")

            # マスクの白黒を反転させる
            img_subtitle_mask = ImageOps.invert(img_subtitle_mask)

            # マスクを適用
            img_subtitle_body.putalpha(img_subtitle_mask)

            # その場のサイズ（.width / .height）にSUBTITLE_SCALEを掛けてリサイズ
            subtitle_new_size = (int(img_subtitle_body.width * SUBTITLE_SCALE), int(img_subtitle_body.height * SUBTITLE_SCALE))
            img_subtitle_resized = img_subtitle_body.resize(subtitle_new_size, Image.Resampling.LANCZOS)

            # img_newの(75, 55)に貼り付け
            # 第3引数に自身を指定して透過を有効にする
            img_new.paste(img_subtitle_resized, (75, 55), img_subtitle_resized)

        # 保存
        img_new.save(temppng_path, "PNG")
    
    return


###################################################################################################
def convert_IMG007(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """sys/mini_title.bmp 変換(6章)"""

    # 拡大率
    SUBTITLE_SCALE = 0.66

    # 字幕用の画像パス
    subtitle_image_path = cfg.nsa_extract_dir / Path('yobi') / Path('system') / Path('chapter06.png')

    # 元画像を読み込み
    with Image.open(nsa_extract_path) as img:
        img = img.convert("RGB")
        
        # 元画像の左上の色をもとに240x160の新画像を作成
        bg_color = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color)
        
        # 元画像の(0,145)から(800,349)を切り出し
        img_cropped = img.crop((0, 145, 800, 349))
        
        # 240x61に縮小
        img_resized = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)
        
        # 新画像の(0,32)にはりつけ
        img_new.paste(img_resized, (0, 32))
        
        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # 字幕用の画像を読み込んで処理
        with Image.open(subtitle_image_path) as img_subtitle:

            # 3枚目（本体）と4枚目（マスク）を直値で切り出し
            img_subtitle_body = img_subtitle.crop((498, 0, 747, 23)).convert("RGBA")
            img_subtitle_mask = img_subtitle.crop((747, 0, 996, 23)).convert("L")

            # マスクの白黒を反転させる
            img_subtitle_mask = ImageOps.invert(img_subtitle_mask)

            # マスクを適用
            img_subtitle_body.putalpha(img_subtitle_mask)

            # その場のサイズ（.width / .height）にSUBTITLE_SCALEを掛けてリサイズ
            subtitle_new_size = (int(img_subtitle_body.width * SUBTITLE_SCALE), int(img_subtitle_body.height * SUBTITLE_SCALE))
            img_subtitle_resized = img_subtitle_body.resize(subtitle_new_size, Image.Resampling.LANCZOS)

            # img_newの(75, 55)に貼り付け
            # 第3引数に自身を指定して透過を有効にする
            img_new.paste(img_subtitle_resized, (75, 55), img_subtitle_resized)

        # 保存
        img_new.save(temppng_path, "PNG")
    
    return


###################################################################################################
def convert_IMG008(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """sys/mini_title.bmp 変換(7章)"""

    # 拡大率
    SUBTITLE_SCALE = 0.66

    # 字幕用の画像パス
    subtitle_image_path = cfg.nsa_extract_dir / Path('yobi') / Path('system') / Path('chapter07.png')

    # 元画像を読み込み
    with Image.open(nsa_extract_path) as img:
        img = img.convert("RGB")
        
        # 元画像の左上の色をもとに240x160の新画像を作成
        bg_color = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color)
        
        # 元画像の(0,145)から(800,349)を切り出し
        img_cropped = img.crop((0, 145, 800, 349))
        
        # 240x61に縮小
        img_resized = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)
        
        # 新画像の(0,32)にはりつけ
        img_new.paste(img_resized, (0, 32))
        
        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # 字幕用の画像を読み込んで処理
        with Image.open(subtitle_image_path) as img_subtitle:

            # 3枚目（本体）と4枚目（マスク）を直値で切り出し
            img_subtitle_body = img_subtitle.crop((498, 0, 747, 23)).convert("RGBA")
            img_subtitle_mask = img_subtitle.crop((747, 0, 996, 23)).convert("L")

            # マスクの白黒を反転させる
            img_subtitle_mask = ImageOps.invert(img_subtitle_mask)

            # マスクを適用
            img_subtitle_body.putalpha(img_subtitle_mask)

            # その場のサイズ（.width / .height）にSUBTITLE_SCALEを掛けてリサイズ
            subtitle_new_size = (int(img_subtitle_body.width * SUBTITLE_SCALE), int(img_subtitle_body.height * SUBTITLE_SCALE))
            img_subtitle_resized = img_subtitle_body.resize(subtitle_new_size, Image.Resampling.LANCZOS)

            # img_newの(75, 55)に貼り付け
            # 第3引数に自身を指定して透過を有効にする
            img_new.paste(img_subtitle_resized, (75, 55), img_subtitle_resized)

        # 保存
        img_new.save(temppng_path, "PNG")
    
    return


###################################################################################################
def convert_IMG009(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """sys/mini_title.bmp 変換(8章)"""

    # 拡大率
    SUBTITLE_SCALE = 0.66

    # 字幕用の画像パス
    subtitle_image_path = cfg.nsa_extract_dir / Path('yobi') / Path('system') / Path('chapter08.png')

    # 元画像を読み込み
    with Image.open(nsa_extract_path) as img:
        img = img.convert("RGB")
        
        # 元画像の左上の色をもとに240x160の新画像を作成
        bg_color = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color)
        
        # 元画像の(0,145)から(800,349)を切り出し
        img_cropped = img.crop((0, 145, 800, 349))
        
        # 240x61に縮小
        img_resized = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)
        
        # 新画像の(0,32)にはりつけ
        img_new.paste(img_resized, (0, 32))
        
        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # 字幕用の画像を読み込んで処理
        with Image.open(subtitle_image_path) as img_subtitle:

            # 3枚目（本体）と4枚目（マスク）を直値で切り出し
            img_subtitle_body = img_subtitle.crop((498, 0, 747, 23)).convert("RGBA")
            img_subtitle_mask = img_subtitle.crop((747, 0, 996, 23)).convert("L")

            # マスクの白黒を反転させる
            img_subtitle_mask = ImageOps.invert(img_subtitle_mask)

            # マスクを適用
            img_subtitle_body.putalpha(img_subtitle_mask)

            # その場のサイズ（.width / .height）にSUBTITLE_SCALEを掛けてリサイズ
            subtitle_new_size = (int(img_subtitle_body.width * SUBTITLE_SCALE), int(img_subtitle_body.height * SUBTITLE_SCALE))
            img_subtitle_resized = img_subtitle_body.resize(subtitle_new_size, Image.Resampling.LANCZOS)

            # img_newの(75, 55)に貼り付け
            # 第3引数に自身を指定して透過を有効にする
            img_new.paste(img_subtitle_resized, (75, 55), img_subtitle_resized)

        # 保存
        img_new.save(temppng_path, "PNG")
    
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
def convert_IMG018_023(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/c001.jpg～e/c004.jpg 変換"""

    # 画像を読み込み
    with Image.open(nsa_extract_path).convert("RGB") as img:
        
        # 元画像の左上 (0, 0) の色を取得
        bg_color = img.getpixel((0, 0))

        # 元画像の左上の色をもとに240x160の新画像を作成
        img_new = Image.new("RGB", (240, 160), bg_color)

        # 元画像の(160, 196)から(640, 322)までを切り出し
        img_cropped = img.crop((160, 196, 640, 322))

        # 240x61に縮小
        img_cropped = img_cropped.resize((240, 61), Image.LANCZOS)

        # 新切り出し画像を新画像の(0, 32)にはりつけ
        img_new.paste(img_cropped, (0, 32))

        # PNGで保存
        img_new.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG067(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/imege95.jpg 変換"""

    # 画像を読み込み
    with Image.open(nsa_extract_path).convert("RGB") as img:
        img = img.convert("RGB")
        
        # 元画像の左上の色をもとに240x160の新画像を作成
        bg_color = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color)
        
        # image96.jpg(95の黒帯ついてない版)を読み込み
        img96_path = nsa_extract_path.parent / Path('imege96.jpg')
        with Image.open(img96_path) as img96:

            # 240x180にリサイズ（縮小）
            img96 = img96.resize((240, 180), Image.LANCZOS)

            # 切り出し部分のみ（240x61）にクロップ
            img96 = img96.crop((0, 42, 240, (42 + 61)))
            
            # 新画像の(0,32)にはりつけ
            img_new.paste(img96, (0, 32))
        
        # 保存
        img_new.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG068_069(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/imege96.jpg～e/imege97.jpg 変換"""

    # 画像を読み込み
    with Image.open(nsa_extract_path) as img:

        # 240x180にリサイズ（縮小）
        img = img.resize((240, 180), Image.LANCZOS)
        
        # 上下10pxを捨てる（240x160）にクロップ
        img = img.crop((0, 10, 240, 170))

        # シャープネスを少し上げる
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # PNGで保存
        img.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG082_084(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/nar01.jpg～e/nar01d.jpg 変換"""

    # 画像を読み込み
    with Image.open(nsa_extract_path).convert("RGB") as img:
        
        # 元画像の左上 (0, 0) の色を取得
        bg_color = img.getpixel((0, 0))

        # 元画像の左上の色をもとに240x160の新画像を作成
        img_new = Image.new("RGB", (240, 160), bg_color)

        # 元画像の(185, 196)から(585, 298)までを切り出し
        img_cropped = img.crop((188, 196, 588, 298))

        # 240x61に縮小
        img_cropped = img_cropped.resize((240, 61), Image.LANCZOS)

        # 新切り出し画像を新画像の(0, 32)にはりつけ
        img_new.paste(img_cropped, (0, 32))

        # PNGで保存
        img_new.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG139(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """tui/imege98.bmp 変換"""

    # フィルター画像のパス
    filter_image_path = cfg.image_filter_dir / Path('filter_139_1.bin')

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
def convert_none_background(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """何もしない背景CG変換(汎用)"""
    return


###################################################################################################
def convert_gray_background(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """グレー背景CG変換(汎用)"""

    # 画像を読み込み
    with Image.open(nsa_extract_path).convert("RGB") as img:
        
        # グレースケールに変換して、文字部分を判別しやすくする
        # 背景がグレー、文字が白（明るい）前提なので、一定以上の明るさを文字とみなす
        gray_img = img.convert("L")
        
        # 文字部分（白に近い部分）のバウンディングボックスを取得
        # getbboxは「0（黒）」以外の領域を探すため、pointで二値化する
        # 閾値（128）は画像のグレーの濃さに合わせて調整してください
        binary_mask = gray_img.point(lambda x: 255 if x > 128 else 0)
        bbox = binary_mask.getbbox()

        if not bbox:
            print("文字が検出されませんでした。")
            return

        # bboxは (left, top, right, bottom)
        left, top, right, bottom = bbox

        # 切り出し位置とサイズ
        crop_x = left
        crop_y = top
        crop_w = right - left
        crop_h = bottom - top

        # 元画像の左上の色をもとに240x160の新画像(img_new)を作成
        bg_color_topleft = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color_topleft)

        # 元画像の(5,150)の色をもとに240x61の新背景画像(img_bgcolor)を作成
        bg_color_target = img.getpixel((5, 150))
        img_bgcolor = Image.new("RGB", (240, 61), bg_color_target)

        # 元画像から一部を切り出し、縮小した新切り出し画像(img_cropped)を作成
        crop_h_scaled = 9
        crop_w_scaled = int(crop_w * (crop_h_scaled / crop_h))
        img_cropped = img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
        img_cropped = img_cropped.resize((crop_w_scaled, crop_h_scaled), Image.LANCZOS)

        # 新背景画像を新画像の(0,32)にはりつけ
        img_new.paste(img_bgcolor, (0, 32))

        # 新切り出し画像を新画像にはりつけ
        paste_x = 120 - crop_w_scaled // 2
        paste_y = 32 + (61 - crop_h_scaled) // 2
        img_new.paste(img_cropped, (paste_x, paste_y))

        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # PNGで保存
        img_new.save(temppng_path, "PNG")

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
        
        # 元画像の(0,145)から(800,349)を切り出し
        img_cropped = img.crop((0, 145, 800, 349))
        
        # 240x61に縮小
        img_resized = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)
        
        # 新画像の(0,32)にはりつけ
        img_new.paste(img_resized, (0, 32))
        
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
        
        # 上下10pxを捨てる（240x160）にクロップ
        img = img.crop((0, 10, 240, 170))

        # シャープネスを少し上げる
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=30, threshold=3))

        # PNGで保存
        img.save(temppng_path, "PNG")

    return