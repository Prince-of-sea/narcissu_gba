#!/usr/bin/env python3
import shutil

from core.config import AppConfig


def clear_directory(cfg: AppConfig) -> None:
    """不要ディレクトリの中身全部消す"""

    shutil.rmtree(cfg.convert_dir)
    shutil.rmtree(cfg.extract_dir)

    if (cfg.debug_dir).exists():
        shutil.rmtree(cfg.debug_dir)
    
    return