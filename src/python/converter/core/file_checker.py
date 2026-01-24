#!/usr/bin/env python3
import binascii
from pathlib import Path

from .paths import FILE_CRC32_LIST
from core.config import AppConfig

def check_files(cfg: AppConfig) -> None:
    """チェックを行う"""

    # 仮 最低限...の予定だったけどexe内蔵するならこの出来で良いかも
    r = True

    for f_info in FILE_CRC32_LIST:
        f_path = cfg.exe_extract_dir / Path(f_info[2])
        if not f_path.exists():
            r = False
            raise Exception (f'必要なファイルが存在しません: {f_path}')
        else:
            file_size_bytes = Path(f_path).stat().st_size

            # 容量チェック
            if (file_size_bytes != f_info[1]):
                r = False
                raise Exception (f'ファイルの容量が異なります: {f_path} 計算容量:{file_size_bytes} 想定容量:{f_info[1]}')

            # crc32 チェック
            with open(f_path, 'rb') as f:
                data = f.read()
                
                crc32 = binascii.crc32(data)
                if (crc32 != f_info[0]):
                    r = False
                    raise Exception (f'ファイルの整合性が取れません: {f_path} 計算CRC:{hex(crc32)} 想定CRC:{hex(f_info[0])}')
    
    return r