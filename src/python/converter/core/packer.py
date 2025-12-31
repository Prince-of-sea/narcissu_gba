from pathlib import Path
import subprocess
import shutil

#####後で消す#####
GBFS_EXE = Path("D:/132_shuumatsu_gba/gbfs/exe/rom/gbfs.exe")
GAME_GBA = Path("D:/132_shuumatsu_gba/src/test.gba")
result_gba = "D:/132_shuumatsu_gba/narci_test.gba"
temp_dir = Path('D:/132_shuumatsu_gba/gbfs/data/tmp/')
gbfs_path = (temp_dir / 'data.gbfs')
##################


def join_binary_files():
    """
    2つのバイナリファイルを明示的に1つに結合する
    """
    out = Path(result_gba)
    src1 = Path(GAME_GBA)
    src2 = Path(gbfs_path)

    if out.is_file():
       out.unlink() 

    with out.open("wb") as outfile:
        # 1つ目のファイルをコピー
        with src1.open("rb") as infile1:
            shutil.copyfileobj(infile1, outfile)
        
        # 2つ目のファイルをコピー
        with src2.open("rb") as infile2:
            shutil.copyfileobj(infile2, outfile)


def run_gbfs() -> None:
    """gbfs.exe を使ってパックする"""

    if gbfs_path.is_file():
       gbfs_path.unlink() 

    cmd = [GBFS_EXE, gbfs_path, f'{temp_dir}/*.*']
    subprocess.run(cmd, cwd = temp_dir)
    pass


def pack_resources() -> None:
    """結合処理全体"""
    run_gbfs()
    join_binary_files()
    pass


if __name__ == '__main__':
    # 結合処理全体
    pack_resources()