#!/usr/bin/env python3
import subprocess
import shutil
import os

from core.config import AppConfig


def subprocess_args(include_stdout=True):
    """subprocessがexe化時正常に動かないときの対策"""

    if hasattr(subprocess, 'STARTUPINFO'):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        env = os.environ
    else:
        si = None
        env = None

    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}

    ret.update({'stdin': subprocess.PIPE, 'stderr': subprocess.PIPE,
               'startupinfo': si, 'env': env})
    return ret


def clear_directory(cfg: AppConfig) -> None:
    """不要ディレクトリの中身全部消す"""

    shutil.rmtree(cfg.convert_dir)
    shutil.rmtree(cfg.extract_dir)

    if (cfg.debug_dir).exists():
        shutil.rmtree(cfg.debug_dir)
    
    return