#!/usr/bin/env python3
from dataclasses import dataclass
from pathlib import Path

import dearpygui.dearpygui as dpg


@dataclass
class AppConfig:
    # ===== ツールについて =====
    app_name: str
    app_version: str
    
    # ===== 入出力 =====
    input_exe: Path
    include_voice: bool
    sound_quality: int

    # ===== 外部リソース =====
    image_filter_dir: Path
    license_txt_path: Path
    font_path: Path
    icon_path: Path
    repo_url: str

    # ===== 外部ツール（exe）=====
    arc_unpacker_exe: Path
    gbfs_exe: Path
    grit_exe: Path
    sox_exe: Path

    # ===== 作業ディレクトリ =====
    extract_dir: Path
    exe_extract_dir: Path
    nsa_extract_dir: Path
    convert_dir: Path
    debug_dir: Path
    gbfs_path: Path

    # ===== 入力起点 =====
    nsdat_path: Path
    nsa_path: Path

    # ===== 出力起点 =====
    output_debug_dir: Path
    result_gba: Path
    base_gba: Path

    # ===== 設定関連 =====
    bgm_high_quality: bool = False
    voice_on: bool = True
    debug_mode: bool = False

    # ===== 設定関連 =====
    sound_quality_high: int = 8738
    sound_quality_low: int = 5734
    sound_quality_high_message: str = f"高音質再生モード(声無し・{sound_quality_high}Hz)"
    sound_quality_low_message: str = f"ボイス搭載モード(声アリ・{sound_quality_low}Hz)"

    # ===== プログレスバー進捗割合 =====
    progress_dict: dict = None


def set_gui_config(cfg: AppConfig) -> None:
    """GUIからの設定をAppConfigに反映させる"""
    
    cwd = Path.cwd()

    if (dpg.get_value('conv_mode_radio') == cfg.sound_quality_low_message):
        include_voice_cfg = True
        sound_quality_cfg = cfg.sound_quality_low
        result_gba_name = "NarcissuGBA.gba"

    elif (dpg.get_value('conv_mode_radio') == cfg.sound_quality_high_message):
        include_voice_cfg = False
        sound_quality_cfg = cfg.sound_quality_high
        result_gba_name = "NarcissuGBA (no voice).gba"

    cfg.include_voice    = include_voice_cfg
    cfg.sound_quality    = sound_quality_cfg
    cfg.output_debug_dir = Path(cwd / f"debug_{result_gba_name}")
    cfg.result_gba       = Path(cwd / result_gba_name)
    cfg.base_gba         = Path(cwd / "resources" / "base_gba" / f"base_{sound_quality_cfg}.gba")
    cfg.debug_mode       = bool(dpg.get_value("debug_checkbox"))

    cfg.exe_extract_dir.mkdir(parents=True, exist_ok=True)
    cfg.convert_dir.mkdir(parents=True, exist_ok=True)

    if (cfg.debug_mode):
        Path(cfg.debug_dir / 'img').mkdir(parents=True, exist_ok=True)
        Path(cfg.debug_dir / 'bgm').mkdir(parents=True, exist_ok=True)
        Path(cfg.debug_dir / 'fmx').mkdir(parents=True, exist_ok=True)
        Path(cfg.debug_dir / 'scn').mkdir(parents=True, exist_ok=True)
    
    return


def create_config(temp_dir: Path) -> AppConfig:
    """AppConfigを作成する"""

    cwd = Path.cwd()

    cfg = AppConfig(
        app_name         = "Narcissu GBA Converter",
        app_version      = "0.7.2",
        
        input_exe        = Path(cwd / "resources" / "game_win" / "nana24.exe"),
        include_voice    = bool(),
        sound_quality    = int(),

        image_filter_dir = Path(cwd / "resources" / "image_filters"),
        license_txt_path = Path(cwd / "resources" / "lib_license" / "licenses_py.txt"),
        font_path        = Path(cwd / "resources" / "fonts" / "GenJyuuGothic-Monospace-Bold.ttf"),
        icon_path        = Path(cwd / "resources" / "icon" / "icon.ico"),
        repo_url         = str("https://github.com/Prince-of-sea/narcissu_gba/"),

        arc_unpacker_exe = Path(cwd / "tools" / "arc_unpacker" / "arc_unpacker.exe"),
        gbfs_exe         = Path(cwd / "tools" / "gbfs" / "gbfs.exe"),
        grit_exe         = Path(cwd / "tools" / "grit" / "grit.exe"),
        sox_exe          = Path(cwd / "tools" / "sox" / "sox.exe"),

        nsdat_path       = Path(), # resource_extractor - extract_nana24_exeで設定
        nsa_path         = Path(), # 同様

        extract_dir      = Path(temp_dir / "extract"),
        exe_extract_dir  = Path(temp_dir / "extract" / "nana24"),
        nsa_extract_dir  = Path(temp_dir / "extract" / "arc~.nsa"),
        convert_dir      = Path(temp_dir / "convert"),
        debug_dir        = Path(temp_dir / "debug"),
        gbfs_path        = Path(temp_dir / "convert" / "data.gbfs"),

        output_debug_dir = Path(),
        result_gba       = Path(),
        base_gba         = Path(),

        debug_mode       = bool(),

        progress_dict    = {
            "start": 0,
            "extract_nana24_exe": 10,
            "extract_arc_nsa": 20,
            "convert_scenario": 30,
            "convert_images": 40,
            "convert_audio": 80,
            "run_gbfs": 95,
            "join_binary_files": 100,
        },
    )

    return cfg
