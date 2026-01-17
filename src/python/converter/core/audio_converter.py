#!/usr/bin/env python3
import concurrent.futures
import subprocess
import shutil
from pathlib import Path

from core.config import AppConfig
from .paths import BGM_LIST, SE_LIST, VOICE_LIST


def run_sox(cfg: AppConfig, input_path: Path, tempraw_path: Path, is_bgm: bool) -> None:
    """sox.exeを使って変換"""

    # 音質設定
    rate = cfg.sound_quality

    # メイン処理 - コマンド組み立て
    if is_bgm:
        cmd = [cfg.sox_exe, input_path, '-c1', f'-r{rate}', '-B', '-b8', '-e', 'signed-integer', tempraw_path,
               'silence', '1', '0.1', '1%', 'reverse', 'silence', '1', '0.1', '1%', 'reverse']
    else:
        cmd = [cfg.sox_exe, input_path, '-c1', f'-r{rate}', '-B', '-b8', '-e', 'signed-integer', tempraw_path, 'gain', '-l', '6',
               'silence', '1', '0.1', '1%', 'reverse', 'silence', '1', '0.1', '1%', 'reverse']

    # メイン処理 - コマンド実行
    subprocess.run(cmd, cwd = cfg.convert_dir)

    # デバッグ用
    if cfg.debug_mode:

        # パス設定
        tempwav_path = tempraw_path.with_suffix('.wav')

        # テスト用処理 - コマンド組み立て
        if is_bgm:
            cmd = [cfg.sox_exe, input_path, '-c1', f'-r{rate}', '-b8', tempwav_path, 
                    'silence', '1', '0.1', '1%', 'reverse', 'silence', '1', '0.1', '1%', 'reverse']
        else:
            cmd = [cfg.sox_exe, input_path, '-c1', f'-r{rate}', '-b8', tempwav_path, 'gain', '-l', '6',
                    'silence', '1', '0.1', '1%', 'reverse', 'silence', '1', '0.1', '1%', 'reverse']

        # テスト用処理 - コマンド実行
        subprocess.run(cmd, cwd = cfg.convert_dir)
    
    # 無音ファイルコピー
    shutil.copyfile(
        Path(cfg.convert_dir / 'dummy.raw'),
        Path(cfg.convert_dir / f'{tempraw_path.stem}_'),
    )

    return


def run_sox_dummy(cfg: AppConfig, dummyraw_path: Path) -> None:
    """sox.exeを使って無音ファイルを作成"""

    # 音質設定
    rate = cfg.sound_quality

    # 無音ファイル作成(音声再生後に、「データ上で次にあるファイル」の先頭が一瞬流れるバグがあるのでその解消用)
    # 次が流れてもそれが無音なら気づかれなくて済む、実害無い、とかいう雑な回避策
    cmd = [cfg.sox_exe, '-n', '-c1', f'-r{rate}', '-B', '-b8', '-e', 'signed-integer', dummyraw_path, 'trim', '0', '0.7']

    # メイン処理 - コマンド実行
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

    # デバッグ用にwavファイルをdebug_dirにコピー
    if cfg.debug_mode:
        if is_bgm:
            tempwavpath = tempraw_path.with_suffix('.wav')
            debugwavpath = Path(cfg.debug_dir / 'bgm' / f'bgm{p_index}.wav')
        else:
            tempwavpath = tempraw_path.with_suffix('.wav')
            debugwavpath = Path(cfg.debug_dir / 'fmx' / f'fmx{p_index}.wav')

        tempwavpath.replace(debugwavpath)
    
    # 競合するファイルがあれば削除
    if output_path.exists(): 
        output_path.unlink()

    # 変換したrawファイルをrenameして出力パスに移動
    tempraw_path.replace(output_path)

    return


def convert_audio(cfg: AppConfig) -> None:
    """音源の全変換処理"""

    # 無音ファイルパス
    dummyraw_path = Path(cfg.convert_dir / f'dummy.raw')

    # 無音ファイル作成
    run_sox_dummy(cfg, dummyraw_path)

    # 並列ファイル変換
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        if cfg.include_voice:
            fmx_list = (SE_LIST + VOICE_LIST)
        else:
            fmx_list = (SE_LIST)

        for img_info in BGM_LIST:
            # 音源の並列変換処理(is_bgm=True)
            futures.append(executor.submit(
                convert_audio_parallel, cfg, img_info, True))
            
        for img_info in fmx_list:
            # 音源の並列変換処理(is_bgm=True)
            futures.append(executor.submit(
                convert_audio_parallel, cfg, img_info, False))

        # gui対応時にはプログレスバー用に改良予定
        concurrent.futures.as_completed(futures)
    
    # 無音ファイル削除
    dummyraw_path.unlink()

    return
