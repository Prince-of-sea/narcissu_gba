#!/usr/bin/env python3
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    # ===== 入出力 =====
    input_dir: Path
    output_dir: Path

    # ===== 外部ツール（exe）=====
    arc_unpacker_exe: Path
    gbfs_exe: Path
    grit_exe: Path
    sox_exe: Path

    # ===== 作業ディレクトリ =====
    extract_dir: Path
    nsa_extract_dir: Path
    convert_dir: Path
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


def create_config(temp_dir: str, gui_cfg: dict) -> AppConfig:

    temp_dir = Path(temp_dir)

    if getattr(sys, 'frozen', False):
        # .exeとして実行されている時の処理
        cwd = Path.cwd()
    else:
        # 通常のPythonスクリプトとして実行されている時の処理
        cwd = Path.cwd().parent.parent.parent
    
    input_dir_cfg = gui_cfg['input_dir']
    output_dir_cfg = gui_cfg['output_dir']

    cfg = AppConfig(
        input_dir        = Path(input_dir_cfg),
        output_dir       = Path(output_dir_cfg),

        arc_unpacker_exe = Path(cwd / "tools" / "arc_unpacker" / "arc_unpacker.exe"),
        gbfs_exe         = Path(cwd / "tools" / "gbfs" / "gbfs.exe"),
        grit_exe         = Path(cwd / "tools" / "grit" / "grit.exe"),
        sox_exe          = Path(cwd / "tools" / "sox" / "sox.exe"),
        base_gba         = Path(cwd / "core_gba" / "NarcissuGBA.gba"),

        nsdat_path       = Path(input_dir_cfg / "nscript.dat"),
        nsa_path         = Path(input_dir_cfg / "arc.nsa"),

        extract_dir      = Path(temp_dir / "extract"),
        nsa_extract_dir  = Path(temp_dir / "extract" / "arc~.nsa"),
        convert_dir      = Path(temp_dir / "convert"),
        gbfs_path        = Path(temp_dir / "convert" / "data.gbfs"),

        result_gba       = Path(output_dir_cfg / "NarcissuGBA.gba"),

    )

    cfg.extract_dir.mkdir(parents=True, exist_ok=True)
    cfg.convert_dir.mkdir(parents=True, exist_ok=True)

    return cfg
