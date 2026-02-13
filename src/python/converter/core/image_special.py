#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont

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
        img = img.resize((240, 180), Image.Resampling.LANCZOS)
        
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
        img = img.resize((240, 180), Image.Resampling.LANCZOS)
        
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
def convert_IMG002_009(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """yobi/system.chapter02.bmp～yobi/system.chapter08.bmp 変換"""

    # 拡大率
    SUBTITLE_SCALE = 0.66

    # 背景用の画像パス
    subtitle_bg_path = cfg.nsa_extract_dir / Path('sys') / Path('mini_title.png')  

    # 元画像を読み込み
    with Image.open(subtitle_bg_path) as img:
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
        with Image.open(nsa_extract_path) as img_subtitle:

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
        img = img.resize((240, 180), Image.Resampling.LANCZOS)

        # 上12px、下8pxを捨てる（240x160にクロップ）
        img = img.crop((0, 12, 240, 172))

        # シャープネスを少し上げる
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # PNGで保存
        img.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG017(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/c00.jpg 変換"""

    # 文字ついてない版の画像パス
    sora01_path = nsa_extract_path.parent / Path('sora01.jpg')

    # 文面 直置きは気が引けるので申し訳程度のバイナリ表記
    image_msg = b'\xe2\x80\x95\xe3\x80\x80\xef\xbc\x92\xef\xbc\x90\xef\xbc\x90\xef\xbc\x94\xe5\xb9\xb4\xe3\x80\x80\xe4\xb8\xbb\xe4\xba\xba\xe5\x85\xac\xe3\x80\x80\xe5\x88\x9d\xe5\xa4\x8f\xe3\x80\x80\xe2\x80\x95'.decode('utf-8')

    line_s = 2  # 行間
    edge_color = (128, 128, 128,  64)
    main_color = (255, 255, 255, 255)

    with Image.open(sora01_path) as img:
        img = img.convert("RGB")
        img_new = Image.new("RGB", (240, 160), img.getpixel((0, 0)))
        
        # 縮小画像(240x61)の作成
        img_resized = img.crop((0, 145, 800, 349)).resize((240, 61), Image.Resampling.LANCZOS)

        # 描画準備
        tmp = Image.new('RGBA', img_resized.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(tmp)
        font = ImageFont.truetype(cfg.font_path, 11)

        # 1行目を基準とした中央座標計算
        first_line = image_msg.split('\n')[0]
        bbox = draw.textbbox((0, 0), first_line, font=font)
        x, y = (img_resized.width - (bbox[2]-bbox[0])) // 2, (img_resized.height - (bbox[3]-bbox[1])) // 2

        # 描画（縁4方向 + 本体
        for ox, oy in [(-1,0), (1,0), (0,-1), (0,1)]:
            draw.multiline_text((x+ox, y+oy), image_msg, font=font, fill=edge_color, spacing=line_s, align="center")
        draw.multiline_text((x, y), image_msg, font=font, fill=main_color, spacing=line_s, align="center")

        img_resized.paste(tmp, (0, 0), tmp)
        img_new.paste(img_resized, (0, 32))
        
        # 保存
        img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3)).save(temppng_path, "PNG")
    
    return


###################################################################################################
def convert_IMG018_023(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/c001.jpg、e/c004.jpg 変換"""

    # 画像を読み込み
    with Image.open(nsa_extract_path).convert("RGB") as img:
        
        # 元画像の左上 (0, 0) の色を取得
        bg_color = img.getpixel((0, 0))

        # 元画像の左上の色をもとに240x160の新画像を作成
        img_new = Image.new("RGB", (240, 160), bg_color)

        # 元画像の(160, 196)から(640, 322)までを切り出し
        img_cropped = img.crop((160, 196, 640, 322))

        # 240x61に縮小
        img_cropped = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)

        # 新切り出し画像を新画像の(0, 32)にはりつけ
        img_new.paste(img_cropped, (0, 32))

        # PNGで保存
        img_new.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG019_020(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/c001a.jpg～e/c001b.jpg 変換"""

    # フィルター画像のパス
    filter_image_path = cfg.image_filter_dir / Path('filter_019_1.bin')

    # 画像を読み込み
    with Image.open(nsa_extract_path).convert("RGB") as img:
        
        # 元画像の左上 (0, 0) の色を取得
        bg_color = img.getpixel((0, 0))

        # 元画像の左上の色をもとに240x160の新画像を作成
        img_new = Image.new("RGB", (240, 160), bg_color)

        # 元画像の(160, 196)から(640, 322)までを切り出し
        img_cropped = img.crop((160, 196, 640, 322))

        # 240x61に縮小
        img_cropped = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)

        # 新切り出し画像を新画像の(0, 32)にはりつけ
        img_new.paste(img_cropped, (0, 32))

        # フィルター画像を読み込み
        with Image.open(filter_image_path) as filter_img:
            
            # 画像にフィルターを合成
            img_new = Image.alpha_composite(img_new.convert('RGBA'), filter_img.convert('RGBA'))

        # PNGで保存
        img_new.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG024(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/c005.jpg 変換"""

    # 文字ついてない版の画像パス
    chara_0013b_path = nsa_extract_path.parent / Path('chara_0013b.jpg')

    # 文面 直置きは気が引けるので申し訳程度のバイナリ表記
    image_msg = b'\x73\x74\x61\x67\x65\x2d\x6e\x61\x6e\x61\x0a\x20\x2d\x20\x76\x6f\x6c\x2e\x32\x34\x20\x2d\x20'.decode('utf-8')

    line_s = 2  # 行間
    edge_color = (255, 255, 255, 128)
    main_color = (  0,   0,   0, 255)

    with Image.open(chara_0013b_path) as img:
        img = img.convert("RGB")
        img_new = Image.new("RGB", (240, 160), img.getpixel((0, 0)))
        
        # 縮小画像(240x61)の作成
        img_resized = img.crop((0, 145, 800, 349)).resize((240, 61), Image.Resampling.LANCZOS)

        # 描画準備
        tmp = Image.new('RGBA', img_resized.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(tmp)
        font = ImageFont.truetype(cfg.font_path, 10)

        # 1行目を基準とした中央座標計算
        first_line = image_msg.split('\n')[0]
        bbox = draw.textbbox((0, 0), first_line, font=font)
        x, y = (img_resized.width - (bbox[2]-bbox[0])) // 2, (img_resized.height - (bbox[3]-bbox[1])) // 2

        # 描画（縁4方向 + 本体
        for ox, oy in [(-1,0), (1,0), (0,-1), (0,1)]:
            draw.multiline_text((x+ox, y+oy), image_msg, font=font, fill=edge_color, spacing=line_s, align="center")
        draw.multiline_text((x, y), image_msg, font=font, fill=main_color, spacing=line_s, align="center")

        img_resized.paste(tmp, (0, 0), tmp)
        img_new.paste(img_resized, (0, 32))
        
        # 保存
        img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3)).save(temppng_path, "PNG")
    
    return


###################################################################################################
def convert_IMG025(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/c0052.jpg 変換"""

    # 文字ついてない版の画像パス
    chara_0013_path = nsa_extract_path.parent / Path('chara_0013.jpg')

    # 文面 直置きは気が引けるので申し訳程度のバイナリ表記
    image_msg = b'\x73\x74\x61\x67\x65\x2d\x6e\x61\x6e\x61\x0a\x20\x2d\x20\x76\x6f\x6c\x2e\x32\x34\x20\x2d\x20'.decode('utf-8')

    line_s = 2  # 行間
    edge_color = (255, 255, 255, 128)
    main_color = (  0,   0,   0, 255)

    with Image.open(chara_0013_path) as img:
        img = img.convert("RGB")
        img_new = Image.new("RGB", (240, 160), img.getpixel((0, 0)))
        
        # 縮小画像(240x61)の作成
        img_resized = img.crop((0, 145, 800, 349)).resize((240, 61), Image.Resampling.LANCZOS)

        # 描画準備
        tmp = Image.new('RGBA', img_resized.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(tmp)
        font = ImageFont.truetype(cfg.font_path, 10)

        # 1行目を基準とした中央座標計算
        first_line = image_msg.split('\n')[0]
        bbox = draw.textbbox((0, 0), first_line, font=font)
        x, y = (img_resized.width - (bbox[2]-bbox[0])) // 2, (img_resized.height - (bbox[3]-bbox[1])) // 2

        # 描画（縁4方向 + 本体
        for ox, oy in [(-1,0), (1,0), (0,-1), (0,1)]:
            draw.multiline_text((x+ox, y+oy), image_msg, font=font, fill=edge_color, spacing=line_s, align="center")
        draw.multiline_text((x, y), image_msg, font=font, fill=main_color, spacing=line_s, align="center")

        img_resized.paste(tmp, (0, 0), tmp)
        img_new.paste(img_resized, (0, 32))
        
        # 保存
        img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3)).save(temppng_path, "PNG")
    
    return


###################################################################################################
def convert_IMG026(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/c02.jpg 変換"""

    # 文字ついてない版の画像パス
    sora_ame03_path = nsa_extract_path.parent / Path('sora_ame03.jpg')

    # 文面 直置きは気が引けるので申し訳程度のバイナリ表記
    image_msg = b'\xe2\x80\x95\xe3\x80\x80\xef\xbc\x91\xef\xbc\x99\xef\xbc\x99\xef\xbc\x96\xe5\xb9\xb4\xe3\x80\x80\xe6\x98\xa5\xe3\x80\x80\xe3\x82\xbb\xe3\x83\x84\xe3\x83\x9f\xe3\x80\x80\xe2\x80\x95'.decode('utf-8')

    line_s = 2  # 行間
    edge_color = (128, 128, 128,  64)
    main_color = (255, 255, 255, 255)

    with Image.open(sora_ame03_path) as img:
        img = img.convert("RGB")
        img_new = Image.new("RGB", (240, 160), img.getpixel((0, 0)))
        
        # 縮小画像(240x61)の作成
        img_resized = img.crop((0, 145, 800, 349)).resize((240, 61), Image.Resampling.LANCZOS)

        # 描画準備
        tmp = Image.new('RGBA', img_resized.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(tmp)
        font = ImageFont.truetype(cfg.font_path, 11)

        # 1行目を基準とした中央座標計算
        first_line = image_msg.split('\n')[0]
        bbox = draw.textbbox((0, 0), first_line, font=font)
        x, y = (img_resized.width - (bbox[2]-bbox[0])) // 2, (img_resized.height - (bbox[3]-bbox[1])) // 2

        # 描画（縁4方向 + 本体）
        for ox, oy in [(-1,0), (1,0), (0,-1), (0,1)]:
            draw.multiline_text((x+ox, y+oy), image_msg, font=font, fill=edge_color, spacing=line_s, align="center")
        draw.multiline_text((x, y), image_msg, font=font, fill=main_color, spacing=line_s, align="center")

        img_resized.paste(tmp, (0, 0), tmp)
        img_new.paste(img_resized, (0, 32))
        
        # 保存
        img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3)).save(temppng_path, "PNG")
    
    return


###################################################################################################
def convert_IMG027(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/c03.jpg 変換"""

    # 文字ついてない版の画像パス
    sora07_path = nsa_extract_path.parent / Path('sora07.jpg')

    # 文面 直置きは気が引けるので申し訳程度のバイナリ表記
    image_msg = b'\xe2\x80\x95\xe3\x80\x80\xe4\xb8\xbb\xe4\xba\xba\xe5\x85\xac\xe3\x80\x80\xef\xbc\x92\xef\xbc\x90\xef\xbc\x90\xef\xbc\x94\xe5\xb9\xb4\xe3\x80\x80\xe7\xa7\x8b\xe3\x80\x80\xe2\x80\x95'.decode('utf-8')

    line_s = 2  # 行間
    edge_color = (  0,   0,   0,  64)
    main_color = (255, 255, 255, 255)

    with Image.open(sora07_path) as img:
        img = img.convert("RGB")
        img_new = Image.new("RGB", (240, 160), img.getpixel((0, 0)))
        
        # 縮小画像(240x61)の作成
        img_resized = img.crop((0, 145, 800, 349)).resize((240, 61), Image.Resampling.LANCZOS)

        # 描画準備
        tmp = Image.new('RGBA', img_resized.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(tmp)
        font = ImageFont.truetype(cfg.font_path, 11)

        # 1行目を基準とした中央座標計算
        first_line = image_msg.split('\n')[0]
        bbox = draw.textbbox((0, 0), first_line, font=font)
        x, y = (img_resized.width - (bbox[2]-bbox[0])) // 2, (img_resized.height - (bbox[3]-bbox[1])) // 2

        # 描画（縁4方向 + 本体）
        for ox, oy in [(-1,0), (1,0), (0,-1), (0,1)]:
            draw.multiline_text((x+ox, y+oy), image_msg, font=font, fill=edge_color, spacing=line_s, align="center")
        draw.multiline_text((x, y), image_msg, font=font, fill=main_color, spacing=line_s, align="center")

        img_resized.paste(tmp, (0, 0), tmp)
        img_new.paste(img_resized, (0, 32))
        
        # 保存
        img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3)).save(temppng_path, "PNG")
    
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
            img96 = img96.resize((240, 180), Image.Resampling.LANCZOS)

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
        img = img.resize((240, 180), Image.Resampling.LANCZOS)
        
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
        img_cropped = img_cropped.resize((240, 61), Image.Resampling.LANCZOS)

        # 新切り出し画像を新画像の(0, 32)にはりつけ
        img_new.paste(img_cropped, (0, 32))

        # PNGで保存
        img_new.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG114(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/st01.jpg 変換"""

    # 画像を読み込み
    with Image.open(nsa_extract_path).convert("RGB") as img:

        # 切り出し位置とサイズ
        crop_x = 562
        crop_y = 304
        crop_w = 185
        crop_h = 17

        # 本来の縮小後サイズの何倍のサイズにするか
        scale = 2.3

        # 元画像の左上の色をもとに240x160の新画像(img_new)を作成
        bg_color_topleft = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color_topleft)

        # 元画像の(5,150)の色をもとに240x61の新背景画像(img_bgcolor)を作成
        bg_color_target = img.getpixel((5, 150))
        img_bgcolor = Image.new("RGB", (240, 61), bg_color_target)

        # 元画像から一部を切り出し、縮小した新切り出し画像(img_cropped)を作成
        crop_w_scaled = int(crop_w * 0.3 * scale)
        crop_h_scaled = int(crop_h * 0.3 * scale)
        img_cropped = img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
        img_cropped = img_cropped.resize((crop_w_scaled, crop_h_scaled), Image.Resampling.LANCZOS)

        # 新背景画像を新画像の(0,32)にはりつけ
        img_new.paste(img_bgcolor, (0, 32))

        # 新切り出し画像を新画像にはりつけ
        paste_x = 105
        paste_y = 80
        img_new.paste(img_cropped, (paste_x, paste_y))

        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # PNGで保存
        img_new.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG115(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/st02.jpg 変換"""

    # 画像を読み込み
    with Image.open(nsa_extract_path).convert("RGB") as img:

        # 切り出し位置とサイズ
        crop1 = [561, 215, 214, 14]
        crop2 = [561, 244, 185, 14]
        crop3 = [561, 271, 198, 13]
        crop4 = [561, 297, 202, 15]
        crop5 = [561, 322, 199, 14]

        # 本来の縮小後サイズの何倍のサイズにするか
        scale = 2.3

        # 元画像の左上の色をもとに240x160の新画像(img_new)を作成
        bg_color_topleft = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color_topleft)

        # 元画像の(5,150)の色をもとに240x61の新背景画像(img_bgcolor)を作成
        bg_color_target = img.getpixel((5, 150))
        img_bgcolor = Image.new("RGB", (240, 61), bg_color_target)

        # 元画像から一部を切り出し、縮小した新切り出し画像(img_cropped)を作成
        img_cropped1 = img.crop((crop1[0], crop1[1], crop1[0] + crop1[2], crop1[1] + crop1[3]))
        img_cropped1 = img_cropped1.resize((int(crop1[2] * 0.3 * scale), int(crop1[3] * 0.3 * scale)), Image.Resampling.LANCZOS)
        img_cropped2 = img.crop((crop2[0], crop2[1], crop2[0] + crop2[2], crop2[1] + crop2[3]))
        img_cropped2 = img_cropped2.resize((int(crop2[2] * 0.3 * scale), int(crop2[3] * 0.3 * scale)), Image.Resampling.LANCZOS)
        img_cropped3 = img.crop((crop3[0], crop3[1], crop3[0] + crop3[2], crop3[1] + crop3[3]))
        img_cropped3 = img_cropped3.resize((int(crop3[2] * 0.3 * scale), int(crop3[3] * 0.3 * scale)), Image.Resampling.LANCZOS)
        img_cropped4 = img.crop((crop4[0], crop4[1], crop4[0] + crop4[2], crop4[1] + crop4[3]))
        img_cropped4 = img_cropped4.resize((int(crop4[2] * 0.3 * scale), int(crop4[3] * 0.3 * scale)), Image.Resampling.LANCZOS)
        img_cropped5 = img.crop((crop5[0], crop5[1], crop5[0] + crop5[2], crop5[1] + crop5[3]))
        img_cropped5 = img_cropped5.resize((int(crop5[2] * 0.3 * scale), int(crop5[3] * 0.3 * scale)), Image.Resampling.LANCZOS)

        # 新背景画像を新画像の(0,32)にはりつけ
        img_new.paste(img_bgcolor, (0, 32))

        # 新切り出し画像を新画像にはりつけ
        paste_xy1 = [85, 42]
        img_new.paste(img_cropped1, (paste_xy1[0], paste_xy1[1]))
        paste_xy2 = [paste_xy1[0], 47           + int(crop1[3] * 0.3 * scale)]
        img_new.paste(img_cropped2, (paste_xy2[0], paste_xy2[1]))
        paste_xy3 = [paste_xy1[0], paste_xy2[1] + int(crop2[3] * 0.3 * scale)]
        img_new.paste(img_cropped3, (paste_xy3[0], paste_xy3[1]))
        paste_xy4 = [paste_xy1[0], paste_xy3[1] + int(crop3[3] * 0.3 * scale)]
        img_new.paste(img_cropped4, (paste_xy4[0], paste_xy4[1]))
        paste_xy5 = [paste_xy1[0], paste_xy4[1] + int(crop4[3] * 0.3 * scale)]
        img_new.paste(img_cropped5, (paste_xy5[0], paste_xy5[1]))

        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # PNGで保存
        img_new.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG116(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/st03.jpg 変換"""

    # 画像を読み込み
    with Image.open(nsa_extract_path).convert("RGB") as img:

        # 切り出し位置とサイズ
        crop1 = [560, 192, 220, 13]
        crop2 = [560, 217, 220, 15]
        crop3 = [560, 243, 220, 15]
        crop4 = [560, 271, 220, 12]
        crop5 = [560, 296, 220, 15]
        crop6 = [560, 323, 220, 13]

        # 本来の縮小後サイズの何倍のサイズにするか
        scale = 2.3

        # 元画像の左上の色をもとに240x160の新画像(img_new)を作成
        bg_color_topleft = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color_topleft)

        # 元画像の(5,150)の色をもとに240x61の新背景画像(img_bgcolor)を作成
        bg_color_target = img.getpixel((5, 150))
        img_bgcolor = Image.new("RGB", (240, 61), bg_color_target)

        # 元画像から一部を切り出し、縮小した新切り出し画像(img_cropped)を作成
        img_cropped1 = img.crop((crop1[0], crop1[1], crop1[0] + crop1[2], crop1[1] + crop1[3]))
        img_cropped1 = img_cropped1.resize((int(crop1[2] * 0.3 * scale), int(crop1[3] * 0.3 * scale)), Image.Resampling.LANCZOS)
        img_cropped2 = img.crop((crop2[0], crop2[1], crop2[0] + crop2[2], crop2[1] + crop2[3]))
        img_cropped2 = img_cropped2.resize((int(crop2[2] * 0.3 * scale), int(crop2[3] * 0.3 * scale)), Image.Resampling.LANCZOS)
        img_cropped3 = img.crop((crop3[0], crop3[1], crop3[0] + crop3[2], crop3[1] + crop3[3]))
        img_cropped3 = img_cropped3.resize((int(crop3[2] * 0.3 * scale), int(crop3[3] * 0.3 * scale)), Image.Resampling.LANCZOS)
        img_cropped4 = img.crop((crop4[0], crop4[1], crop4[0] + crop4[2], crop4[1] + crop4[3]))
        img_cropped4 = img_cropped4.resize((int(crop4[2] * 0.3 * scale), int(crop4[3] * 0.3 * scale)), Image.Resampling.LANCZOS)
        img_cropped5 = img.crop((crop5[0], crop5[1], crop5[0] + crop5[2], crop5[1] + crop5[3]))
        img_cropped5 = img_cropped5.resize((int(crop5[2] * 0.3 * scale), int(crop5[3] * 0.3 * scale)), Image.Resampling.LANCZOS)
        img_cropped6 = img.crop((crop6[0], crop6[1], crop6[0] + crop6[2], crop6[1] + crop6[3]))
        img_cropped6 = img_cropped6.resize((int(crop6[2] * 0.3 * scale), int(crop6[3] * 0.3 * scale)), Image.Resampling.LANCZOS)

        # 新背景画像を新画像の(0,32)にはりつけ
        img_new.paste(img_bgcolor, (0, 32))

        # 新切り出し画像を新画像にはりつけ
        paste_xy1 = [85, 38]
        img_new.paste(img_cropped1, (paste_xy1[0], paste_xy1[1]))
        paste_xy2 = [paste_xy1[0], paste_xy1[1] + int(crop1[3] * 0.3 * scale)]
        img_new.paste(img_cropped2, (paste_xy2[0], paste_xy2[1]))
        paste_xy3 = [paste_xy1[0], paste_xy2[1] + int(crop2[3] * 0.3 * scale)]
        img_new.paste(img_cropped3, (paste_xy3[0], paste_xy3[1]))
        paste_xy4 = [paste_xy1[0], paste_xy3[1] + int(crop3[3] * 0.3 * scale)]
        img_new.paste(img_cropped4, (paste_xy4[0], paste_xy4[1]))
        paste_xy5 = [paste_xy1[0], paste_xy4[1] + int(crop4[3] * 0.3 * scale)]
        img_new.paste(img_cropped5, (paste_xy5[0], paste_xy5[1]))
        paste_xy6 = [paste_xy1[0], paste_xy5[1] + int(crop5[3] * 0.3 * scale)]
        img_new.paste(img_cropped6, (paste_xy6[0], paste_xy6[1]))

        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

        # PNGで保存
        img_new.save(temppng_path, "PNG")

    return


###################################################################################################
def convert_IMG117(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """e/st04.jpg 変換"""

    # 画像を読み込み
    with Image.open(nsa_extract_path).convert("RGB") as img:

        # 切り出し位置とサイズ
        crop1 = [617, 242, 152, 16]
        crop2 = [617, 275, 152, 15]
        crop3 = [617, 307, 152, 12]

        # 本来の縮小後サイズの何倍のサイズにするか
        scale = 2.3

        # 元画像の左上の色をもとに240x160の新画像(img_new)を作成
        bg_color_topleft = img.getpixel((0, 0))
        img_new = Image.new("RGB", (240, 160), bg_color_topleft)

        # 元画像の(5,150)の色をもとに240x61の新背景画像(img_bgcolor)を作成
        bg_color_target = img.getpixel((5, 150))
        img_bgcolor = Image.new("RGB", (240, 61), bg_color_target)

        # 元画像から一部を切り出し、縮小した新切り出し画像(img_cropped)を作成
        img_cropped1 = img.crop((crop1[0], crop1[1], crop1[0] + crop1[2], crop1[1] + crop1[3]))
        img_cropped1 = img_cropped1.resize((int(crop1[2] * 0.3 * scale), int(crop1[3] * 0.3 * scale)), Image.Resampling.LANCZOS)
        img_cropped2 = img.crop((crop2[0], crop2[1], crop2[0] + crop2[2], crop2[1] + crop2[3]))
        img_cropped2 = img_cropped2.resize((int(crop2[2] * 0.3 * scale), int(crop2[3] * 0.3 * scale)), Image.Resampling.LANCZOS)
        img_cropped3 = img.crop((crop3[0], crop3[1], crop3[0] + crop3[2], crop3[1] + crop3[3]))
        img_cropped3 = img_cropped3.resize((int(crop3[2] * 0.3 * scale), int(crop3[3] * 0.3 * scale)), Image.Resampling.LANCZOS)

        # 新背景画像を新画像の(0,32)にはりつけ
        img_new.paste(img_bgcolor, (0, 32))

        # 新切り出し画像を新画像にはりつけ
        paste_xy1 = [128, 62]
        img_new.paste(img_cropped1, (paste_xy1[0], paste_xy1[1]))
        paste_xy2 = [paste_xy1[0], paste_xy1[1] + int(crop1[3] * 0.3 * scale)]
        img_new.paste(img_cropped2, (paste_xy2[0], paste_xy2[1]))
        paste_xy3 = [paste_xy1[0], paste_xy2[1] + int(crop2[3] * 0.3 * scale)]
        img_new.paste(img_cropped3, (paste_xy3[0], paste_xy3[1]))

        # シャープネスを少し上げる
        img_new = img_new.filter(ImageFilter.UnsharpMask(radius=2, percent=15, threshold=3))

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
        img = img.resize((240, 180), Image.Resampling.LANCZOS)
        
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
def convert_IMG999(nsa_extract_path: Path, temppng_path: Path, cfg: AppConfig):
    """変換環境表示(仮) 変換"""

    # 変換モード文字列
    if cfg.include_voice:
        voice_mode = 'ボイスON'
    else:
        voice_mode = 'ボイスOFF'
    
    if cfg.ch1subtitle_checkbox:
        ch1_mode = '表示'
    else:
        ch1_mode = '非表示'

    # メッセージ内容
    msg = f"""ROM変換日時
　{cfg.convert_time}
バージョン
　Ver.{cfg.app_version}
音声変換設定
　{voice_mode} / {cfg.sound_quality}Hz
Chapter1タイトル
　{ch1_mode}

本ソフトやコンバータに関する
詳細情報、利用方法はこちら→

https://github.com
/Prince-of-sea/narcissu_gba"""
    
    line_s = 2  # 行間
    edge_color = (128, 128, 128, 64)
    main_color = (255, 255, 255, 255)

    # 画像を読み込み
    with Image.open(nsa_extract_path) as img:

        # 240x180にリサイズ（縮小）
        img = img.resize((240, 180), Image.Resampling.LANCZOS)
        
        # 上下10pxを捨てる（240x160にクロップ）
        img = img.crop((0, 10, 240, 170))

        # シャープネスを少し上げる
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=30, threshold=3))
        
        # フィルター画像のパス
        filter2_image_path = cfg.image_filter_dir / Path('filter_999_2.bin')

        # フィルター画像を読み込み
        with Image.open(filter2_image_path) as filter_img:
            
            # 画像にフィルターを合成
            img = Image.alpha_composite(img.convert('RGBA'), filter_img.convert('RGBA'))

        # メッセージ描画用の透明レイヤー
        tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(tmp)
        font = ImageFont.truetype(cfg.font_path, 10)

        # 文字貼り付け開始位置
        x, y = 9, 9

        # 描画（縁4方向 + 本体）    
        for ox, oy in [(-1,0), (1,0), (0,-1), (0,1)]:
            draw.multiline_text((x+ox, y+oy), msg, font=font, fill=edge_color, spacing=line_s, align="left")
        draw.multiline_text((x, y), msg, font=font, fill=main_color, spacing=line_s, align="left")

        # 文字合成
        img.paste(tmp, (0, 0), tmp)

        # QRコード画像のパス
        filter1_image_path = cfg.image_filter_dir / Path('filter_999_1.bin')

        # QRコード画像を読み込み
        with Image.open(filter1_image_path) as filter_img:

            # QRコード貼り付け
            img.paste(filter_img.convert('RGB'), (157, 77))

        # 保存
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
            raise Exception ("文字が検出されませんでした。")
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
        img_cropped = img_cropped.resize((crop_w_scaled, crop_h_scaled), Image.Resampling.LANCZOS)

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
        img = img.resize((240, 180), Image.Resampling.LANCZOS)
        
        # 上下10pxを捨てる（240x160）にクロップ
        img = img.crop((0, 10, 240, 170))

        # シャープネスを少し上げる
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=30, threshold=3))

        # PNGで保存
        img.save(temppng_path, "PNG")

    return