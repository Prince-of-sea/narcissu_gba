#!/usr/bin/env python3
import binascii
from pathlib import Path

from .paths import FILE_CRC32_LIST
from core.config import AppConfig

def check_files(cfg: AppConfig) -> None:
    """チェックを行う"""

    # 仮 最低限
    r = True

    for f_info in FILE_CRC32_LIST:
        f_path = cfg.input_dir / Path(f_info[1])
        if not f_path.exists():
            r = False
            print(f'必要なファイルが存在しません: {f_path}')
        else:
            # crc32 チェック
            with open(f_path, 'rb') as f:
                data = f.read()
                crc32 = binascii.crc32(data)
                if (crc32 != f_info[0]):
                    r = False
                    print(f'ファイルの整合性が取れません: {f_path} {hex(crc32)} {hex(f_info[0])}')
    
    return r