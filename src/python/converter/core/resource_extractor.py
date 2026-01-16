#!/usr/bin/env python3
from pathlib import Path
import subprocess
import zipfile

from core.config import AppConfig


def extract_nana24_exe(cfg: AppConfig) -> None:
    """nana24.exeの展開を行う"""

    # zipfileで展開
    with zipfile.ZipFile(cfg.input_exe, 'r') as zip_ref:
        zip_ref.extractall(cfg.exe_extract_dir)
    
    # 文字化け対策のため、globで探してからexe_extract_dir直下に移動
    for p in cfg.exe_extract_dir.glob('**/nscript.dat'):
        p_rename = Path(cfg.exe_extract_dir / 'nscript.dat')
        p.rename(p_rename)
        cfg.nsdat_path = p_rename

    for p in cfg.exe_extract_dir.glob('**/arc.nsa'):
        p_rename = Path(cfg.exe_extract_dir / 'arc.nsa')
        p.rename(p_rename)
        cfg.nsa_path = p_rename

    return


def extract_arc_nsa(cfg: AppConfig) -> None:
    """arc.nsaの展開を行う"""

    cmd = [cfg.arc_unpacker_exe, '--dec=nscripter/nsa', f'--out={cfg.extract_dir}', cfg.nsa_path]
    subprocess.run(cmd, cwd = cfg.arc_unpacker_exe.parent)

    return


def extract_resources(cfg: AppConfig) -> None:
    """リソース展開を行う"""

    # まずはnana24.exe
    extract_nana24_exe(cfg)

    # arc.nsa
    extract_arc_nsa(cfg)

    return
