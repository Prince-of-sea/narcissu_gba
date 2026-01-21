#!/usr/bin/env python3
from pathlib import Path
import tempfile

from core.config import create_config
from core.gui import gui_main

def main():
    """メイン処理"""

    # 一時ディレクトリを作成してから処理を行う
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)

        # 初期設定だけとりあえず作成
        cfg = create_config(temp_dir)

        # GUI本処理
        gui_main(cfg)


if __name__ == "__main__":
    main()