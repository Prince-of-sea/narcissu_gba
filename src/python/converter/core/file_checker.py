#!/usr/bin/env python3
from pathlib import Path

from core.config import AppConfig
# def calc_crc32(filepath: str) -> int:
#     """ファイルの CRC32 を返す"""
#     pass


def check_files(cfg: AppConfig) -> None:
    """チェックを行う"""

    # 仮 最低限
    r = True

    if not cfg.nsdat_path.exists(): r = False
    if not cfg.nsa_path.exists(): r = False

    return r
