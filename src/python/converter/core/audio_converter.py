#!/usr/bin/env python3
import concurrent.futures
import subprocess
from pathlib import Path

from paths import BGM_LIST, FMX_LIST

#####後で消す#####
SOX_EXE = Path(r"C:/Program Files (x86)/sox-14-4-2/sox.exe")
input_dir = Path(r'D:/132_shuumatsu_gba/__test_ex')
temp_dir = Path(r'D:/132_shuumatsu_gba/__temp_ex')
##############


def run_sox(input_path: Path, tempraw_path: Path) -> None:
    """sox.exeを使って変換"""

    # ここ後でGUI側で編集できるようにする予定
    rate = 5256

    cmd = [SOX_EXE, input_path, '-c1', f'-r{rate}', '-B', '-b8', '-e', 'signed-integer', tempraw_path]
    subprocess.run(cmd, cwd = temp_dir)

    return


def convert_audio_parallel(img_info: list[int, str], is_bgm: bool) -> None:
    """画像の並列変換処理"""

    p_relative_path = img_info[1]
    input_path   = (input_dir / Path(p_relative_path))

    if is_bgm:
        p_index = str(img_info[0]).zfill(2)
        tempraw_path = (temp_dir  / f'bgm{p_index}.raw')
        output_path  = (temp_dir  / f'bgm{p_index}.bin')
    else:
        p_index = str(img_info[0]).zfill(3)
        tempraw_path = (temp_dir  / f'fmx{p_index}.raw')
        output_path  = (temp_dir  / f'fmx{p_index}.bin')

    # 競合するファイルがあれば削除
    if tempraw_path.exists():
        tempraw_path.unlink()

    # sox.exeを使って変換
    run_sox(input_path, tempraw_path)

    # 競合するファイルがあれば削除
    if output_path.exists(): 
        output_path.unlink()

    # 変換したrawファイルをrenameして出力パスに移動
    tempraw_path.rename(output_path)

    return


def convert_audio() -> None:
    """音源の全変換処理"""

    # 並列ファイル変換
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for img_info in BGM_LIST:
            # 音源の並列変換処理(is_bgm=True)
            futures.append(executor.submit(
                convert_audio_parallel, img_info, True))
            
        for img_info in FMX_LIST:
            # 音源の並列変換処理(is_bgm=True)
            futures.append(executor.submit(
                convert_audio_parallel, img_info, False))

        # gui対応時にはプログレスバー用に改良予定
        concurrent.futures.as_completed(futures)

    return


if __name__ == '__main__':
    # 音源の全変換処理
    convert_audio()