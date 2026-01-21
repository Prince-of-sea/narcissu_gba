#!/usr/bin/env python3
from core.resource_extractor import extract_resources
from core.file_checker import check_files
from core.scenario_converter import convert_scenario
from core.image_converter import convert_images
from core.audio_converter import convert_audio
from core.packer import pack_resources
from core.config import set_gui_config


def convert_main(cfg, gui_cfg):
    """変換メイン処理"""

    # GUI設定を反映
    set_gui_config(cfg, gui_cfg)
    
    # リソース抽出
    extract_resources(cfg)

    # ファイルチェック
    if check_files(cfg):

        # 各種変換処理
        convert_scenario(cfg)
        convert_images(cfg)
        convert_audio(cfg)
        pack_resources(cfg)

    return
