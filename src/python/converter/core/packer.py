#!/usr/bin/env python3
from pathlib import Path
import subprocess
import shutil

from core.config import AppConfig

#####後で消す#####
# GBFS_EXE = Path("D:/132_shuumatsu_gba/gbfs/exe/rom/gbfs.exe")
# GAME_GBA = Path("D:/132_shuumatsu_gba/src/test.gba")
# result_gba = "D:/132_shuumatsu_gba/narci_test.gba"
# convert_dir = Path('D:/132_shuumatsu_gba/gbfs/data/tmp/')
# gbfs_path = (convert_dir / 'data.gbfs')
##################


def join_binary_files(cfg: AppConfig):
    """
    2つのバイナリファイルを明示的に1つに結合する
    """
    out = Path(cfg.result_gba)
    src1 = Path(cfg.base_gba)
    src2 = Path(cfg.gbfs_path)

    if out.is_file():
       out.unlink() 

    with out.open("wb") as outfile:
        # 1つ目のファイルをコピー
        with src1.open("rb") as infile1:
            shutil.copyfileobj(infile1, outfile)
        
        # 2つ目のファイルをコピー
        with src2.open("rb") as infile2:
            shutil.copyfileobj(infile2, outfile)


def run_gbfs(cfg: AppConfig) -> None:
    """gbfs.exe を使ってパックする"""

    cmd = [cfg.gbfs_exe, cfg.gbfs_path, f'{cfg.convert_dir}/*.*']
    subprocess.run(cmd, cwd = cfg.convert_dir)
    pass


def pack_resources(cfg: AppConfig) -> None:
    """結合処理全体"""
    run_gbfs(cfg)
    join_binary_files(cfg)
    pass