#!/usr/bin/env python3
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    # ===== 入出力 =====
    input_dir: Path
    output_dir: Path
    include_voice: bool
    sound_quality: int

    # ===== 外部リソース =====
    image_filter_dir: Path

    # ===== 外部ツール（exe）=====
    arc_unpacker_exe: Path
    gbfs_exe: Path
    grit_exe: Path
    sox_exe: Path

    # ===== 作業ディレクトリ =====
    extract_dir: Path
    nsa_extract_dir: Path
    convert_dir: Path
    debug_dir: Path
    gbfs_path: Path

    # ===== 入力起点 =====
    nsdat_path: Path
    nsa_path: Path

    # ===== 出力起点 =====
    result_gba: Path
    base_gba: Path

    # ===== 設定関連(仮) =====
    bgm_high_quality: bool = False
    voice_on: bool = True
    debug_mode: bool = False


def create_config(temp_dir: str, gui_cfg: dict) -> AppConfig:

    temp_dir = Path(temp_dir)
    cwd = Path.cwd()
    
    input_dir_cfg = gui_cfg['input_dir']
    output_dir_cfg = gui_cfg['output_dir']
    include_voice_cfg = gui_cfg['include_voice']
    sound_quality_cfg = gui_cfg['sound_quality']

    cfg = AppConfig(
        input_dir        = Path(input_dir_cfg),
        output_dir       = Path(output_dir_cfg),
        include_voice    = bool(include_voice_cfg),
        sound_quality    = int(sound_quality_cfg),

        image_filter_dir = Path(cwd / "resources" / "image_filters"),

        arc_unpacker_exe = Path(cwd / "tools" / "arc_unpacker" / "arc_unpacker.exe"),
        gbfs_exe         = Path(cwd / "tools" / "gbfs" / "gbfs.exe"),
        grit_exe         = Path(cwd / "tools" / "grit" / "grit.exe"),
        sox_exe          = Path(cwd / "tools" / "sox" / "sox.exe"),

        nsdat_path       = Path(input_dir_cfg / "nscript.dat"),
        nsa_path         = Path(input_dir_cfg / "arc.nsa"),

        extract_dir      = Path(temp_dir / "extract"),
        nsa_extract_dir  = Path(temp_dir / "extract" / "arc~.nsa"),
        convert_dir      = Path(temp_dir / "convert"),
        debug_dir        = Path(temp_dir / "debug"),
        gbfs_path        = Path(temp_dir / "convert" / "data.gbfs"),

        result_gba       = Path(output_dir_cfg / "NarcissuGBA.gba"),
        base_gba         = Path(cwd / "core_gba" / f"base_{sound_quality_cfg}.gba"),

        debug_mode       = bool(Path(cwd / ".debug").exists()),
    )

    cfg.extract_dir.mkdir(parents=True, exist_ok=True)
    cfg.convert_dir.mkdir(parents=True, exist_ok=True)

    if (cfg.debug_mode):
        Path(cfg.debug_dir / 'img').mkdir(parents=True, exist_ok=True)
        Path(cfg.debug_dir / 'bgm').mkdir(parents=True, exist_ok=True)
        Path(cfg.debug_dir / 'fmx').mkdir(parents=True, exist_ok=True)
        Path(cfg.debug_dir / 'scn').mkdir(parents=True, exist_ok=True)

    return cfg
