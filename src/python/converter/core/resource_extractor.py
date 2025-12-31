#!/usr/bin/env python3
import subprocess
import shutil
from pathlib import Path


#####後で消す#####
ARC_UNPACKER_EXE = Path(r"D:/132_shuumatsu_gba/arc_unpacker/arc_unpacker.exe")
extract_dir = Path(r'D:/132_shuumatsu_gba/__test_ex/')
temp_dir = Path('D:/132_shuumatsu_gba/gbfs/data/tmp/')

# arc_unpacker.exe --dec=nscripter/nsa --out="D:\132_shuumatsu_gba\__temp_ex" C:\Users\xxxxx\Desktop\nana24\ナルキッソス\arc.nsa


def extract_resources(input_path: str = "", output_path: str = "") -> None:
    """リソース展開を行う"""




    pass
