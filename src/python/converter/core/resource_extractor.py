#!/usr/bin/env python3
import subprocess

from core.config import AppConfig

#####後で消す#####
# ARC_UNPACKER_EXE = Path(r"D:/132_shuumatsu_gba/arc_unpacker/arc_unpacker.exe")
# extract_dir = Path(r'D:/132_shuumatsu_gba/__test_ex/')
# nsa_path = Path(r'D:/132_shuumatsu_gba/__test_ex/arc.nsa')
##############

def extract_resources(cfg: AppConfig) -> None:
    """リソース展開を行う"""

    # arc.nsa
    cmd = [cfg.arc_unpacker_exe, '--dec=nscripter/nsa', f'--out={cfg.extract_dir}', cfg.nsa_path]
    subprocess.run(cmd, cwd = cfg.arc_unpacker_exe.parent)

    pass