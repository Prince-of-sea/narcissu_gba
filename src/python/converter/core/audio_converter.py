#!/usr/bin/env python3
import concurrent.futures
import subprocess
from pathlib import Path

from core.config import AppConfig
from .paths import BGM_LIST, FMX_LIST


def run_sox(cfg: AppConfig, input_path: Path, tempraw_path: Path, is_bgm: bool) -> None:
    """sox.exeを使って変換"""

    # ここ後でGUI側で編集できるようにする予定
    rate = 5256

    if is_bgm:
        cmd = [cfg.sox_exe, input_path, '-c1', f'-r{rate}', '-B', '-b8', '-e', 'signed-integer', tempraw_path]
    else:
        cmd = [cfg.sox_exe, input_path, '-c1', f'-r{rate}', '-B', '-b8', '-e', 'signed-integer', tempraw_path, 'gain', '-l', '6']
    
    subprocess.run(cmd, cwd = cfg.convert_dir)

    # 無音ファイル作成(音声再生後に、「データ上で次にあるファイル」の先頭が一瞬流れるバグがあるのでその解消用)
    # 次が流れてもそれが無音なら気づかれなくて済む、実害無い、とかいう雑な回避策
    tempraw_none_path = tempraw_path.with_stem(f"{tempraw_path.stem}_")
    cmd = [cfg.sox_exe, '-n', '-c1', f'-r{rate}', '-B', '-b8', '-e', 'signed-integer', tempraw_none_path, 'trim', '0', '0.7']

    subprocess.run(cmd, cwd = cfg.convert_dir)

    return


def convert_audio_parallel(cfg: AppConfig, img_info: list[int, str], is_bgm: bool) -> None:
    """音声の並列変換処理"""

    p_relative_path = img_info[1]
    input_path   = (cfg.nsa_extract_dir / Path(p_relative_path))

    if is_bgm:
        p_index = str(img_info[0]).zfill(2)
        tempraw_path = (cfg.convert_dir  / f'bgm{p_index}.raw')
        output_path  = (cfg.convert_dir  / f'bgm{p_index}.bin')
    else:
        p_index = str(img_info[0]).zfill(3)
        tempraw_path = (cfg.convert_dir  / f'fmx{p_index}.raw')
        output_path  = (cfg.convert_dir  / f'fmx{p_index}.bin')

    # 競合するファイルがあれば削除
    if tempraw_path.exists():
        tempraw_path.unlink()

    # sox.exeを使って変換
    run_sox(cfg, input_path, tempraw_path, is_bgm)

    # 競合するファイルがあれば削除
    if output_path.exists(): 
        output_path.unlink()

    # 変換したrawファイルをrenameして出力パスに移動
    tempraw_path.rename(output_path)

    return


def convert_audio(cfg: AppConfig) -> None:
    """音源の全変換処理"""

    # 並列ファイル変換
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for img_info in BGM_LIST:
            # 音源の並列変換処理(is_bgm=True)
            futures.append(executor.submit(
                convert_audio_parallel, cfg, img_info, True))
            
        for img_info in FMX_LIST:
            # 音源の並列変換処理(is_bgm=True)
            futures.append(executor.submit(
                convert_audio_parallel, cfg, img_info, False))

        # gui対応時にはプログレスバー用に改良予定
        concurrent.futures.as_completed(futures)

    return
