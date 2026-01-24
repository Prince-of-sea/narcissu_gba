#!/usr/bin/env python3
from core.gui_utils import dpg_all_enable_item
from core.gui_utils import message_box
from core.gui_utils import configure_progress_bar
from core.resource_extractor import extract_resources
from core.file_checker import check_files
from core.scenario_converter import convert_scenario
from core.image_converter import convert_images
from core.audio_converter import convert_audio
from core.packer import pack_resources
from core.config import set_gui_config


def convert_main(cfg) -> None:
    """変換メイン処理"""

    # GUI入力無効化
    dpg_all_enable_item(False)

    # GUI設定を反映
    set_gui_config(cfg)
    
    # リソース抽出
    extract_resources(cfg)

    # ファイルチェック
    if check_files(cfg):

        # 各種変換処理
        convert_scenario(cfg)
        convert_images(cfg)
        convert_audio(cfg)
        pack_resources(cfg)
    
    # GUI入力有効化
    dpg_all_enable_item(True)

    # 変換完了メッセージ
    message_box('変換完了', '変換が完了しました')

    # プログレスバー戻す
    configure_progress_bar(cfg.progress_dict["start"])

    return
