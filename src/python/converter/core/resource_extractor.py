#!/usr/bin/env python3
import subprocess
from pathlib import Path


#####後で消す#####
ARC_UNPACKER_EXE = Path(r"D:/132_shuumatsu_gba/arc_unpacker/arc_unpacker.exe")
extract_dir = Path(r'D:/132_shuumatsu_gba/__test_ex/')
temp_dir = Path(r'D:/132_shuumatsu_gba/gbfs/data/tmp/')
nsa_path = Path(r'D:/132_shuumatsu_gba/__test_ex/arc.nsa')
##############

def extract_resources(input_path: str = "", output_path: str = "") -> None:
    """リソース展開を行う"""

    # arc.nsa
    cmd = [ARC_UNPACKER_EXE, '--dec=nscripter/nsa', f'--out={extract_dir}', nsa_path]
    subprocess.run(cmd, cwd = ARC_UNPACKER_EXE.parent)


    pass

if __name__ == '__main__':
    # リソース展開を行う
    extract_resources()