#!/usr/bin/env python3
import subprocess

from core.config import AppConfig


def extract_resources(cfg: AppConfig) -> None:
    """リソース展開を行う"""

    # arc.nsa
    cmd = [cfg.arc_unpacker_exe, '--dec=nscripter/nsa', f'--out={cfg.extract_dir}', cfg.nsa_path]
    subprocess.run(cmd, cwd = cfg.arc_unpacker_exe.parent)

    pass