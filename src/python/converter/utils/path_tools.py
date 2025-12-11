import os
import sys


def get_base_dir() -> str:
    """exe からの相対パスに対応した base_dir を返す"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)


def join_path(*paths) -> str:
    """安全にパスを結合"""
    return os.path.join(*paths)
