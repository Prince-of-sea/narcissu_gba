#!/usr/bin/env python3
import concurrent.futures
import subprocess
import shutil
from pathlib import Path

from core.config import AppConfig
from core.gui_utils import configure_progress_bar
from core.converter_utils import subprocess_args
from .paths import BGM_LIST, SE_LIST, VOICE_LIST


def run_sox(cfg: AppConfig, input_path: Path, temp_raw_path: Path, is_bgm: bool, no_music_threshold: float) -> None:
    """sox.exeを使って変換"""

    # 音質設定
    rate = cfg.sound_quality

    # 無音判定の閾値設定
    no_music_threshold_0 = no_music_threshold[0] #前
    no_music_threshold_1 = no_music_threshold[1] #後

    # メイン処理 - コマンド組み立て
    if is_bgm:
        cmd = [cfg.sox_exe, '-D', input_path, '-c1', f'-r{rate}', '-B', '-b8', '-e', 'signed-integer', temp_raw_path,
                'silence', '1', '0.1', f'{no_music_threshold_0}%', 'reverse', 'silence', '1', '0.1', f'{no_music_threshold_1}%', 'reverse',
                'rate', '-v', str(rate),
                'norm', '-1']
    else:
        cmd = [cfg.sox_exe, '-D', input_path, '-c1', f'-r{rate}', '-B', '-b8', '-e', 'signed-integer', temp_raw_path,
                'silence', '1', '0.1', f'{no_music_threshold_0}%', 'reverse', 'silence', '1', '0.1', f'{no_music_threshold_1}%', 'reverse',
                'gain', '-l', '6',
                'rate', '-v', str(rate),
                'norm', '-1']
    
    # メイン処理 - コマンド実行
    subprocess.run(cmd, cwd = cfg.convert_dir, **subprocess_args())

    # デバッグ用
    if cfg.out_temp_file_checkbox:

        # パス設定
        temp_wav_path = temp_raw_path.with_suffix('.wav')

        # テスト用処理 - コマンド組み立て
        if is_bgm:
            cmd = [cfg.sox_exe, '-D', input_path, '-c1', f'-r{rate}', '-b8', temp_wav_path,
                    'silence', '1', '0.1', f'{no_music_threshold_0}%', 'reverse', 'silence', '1', '0.1', f'{no_music_threshold_1}%', 'reverse',
                    'rate', '-v', str(rate),
                    'norm', '-1']
        else:
            cmd = [cfg.sox_exe, '-D', input_path, '-c1', f'-r{rate}', '-b8', temp_wav_path,
                   'silence', '1', '0.1', f'{no_music_threshold_0}%', 'reverse', 'silence', '1', '0.1', f'{no_music_threshold_1}%', 'reverse',
                   'gain', '-l', '6',
                   'rate', '-v', str(rate),
                   'norm', '-1']

        # テスト用処理 - コマンド実行
        subprocess.run(cmd, cwd = cfg.convert_dir, **subprocess_args())
    
    # 無音ファイルコピー
    if ((is_bgm) or (input_path.stem == 'fmx045')):
        shutil.copyfile(
            Path(cfg.convert_dir / 'dummy.raw'),
            Path(cfg.convert_dir / f'{temp_raw_path.stem}_'),
        )

    return


def run_sox_dummy(cfg: AppConfig, dummy_raw_path: Path) -> None:
    """sox.exeを使って無音ファイルを作成"""

    # 音質設定
    rate = cfg.sound_quality

    # 無音ファイル作成(BGM再生後に、「データ上で次にあるファイル」の先頭が一瞬流れるバグがあるのでその解消用)
    # 次が流れてもそれが無音なら気づかれなくて済む、実害無い、とかいう雑な回避策
    cmd = [cfg.sox_exe, '-n', '-c1', f'-r{rate}', '-B', '-b8', '-e', 'signed-integer', dummy_raw_path, 'trim', '0', '1.3']

    # メイン処理 - コマンド実行
    subprocess.run(cmd, cwd = cfg.convert_dir, **subprocess_args())

    return


def convert_audio_parallel(cfg: AppConfig, img_info: list[int, str], is_bgm: bool) -> None:
    """音声の並列変換処理"""

    p_relative_path = img_info[1]
    p_no_music_threshold = img_info[2]

    input_path   = (cfg.nsa_extract_dir / Path(p_relative_path))

    if is_bgm:
        p_index = str(img_info[0]).zfill(2)
        temp_raw_path = (cfg.convert_dir  / f'bgm{p_index}.raw')
        output_path  = (cfg.convert_dir  / f'bgm{p_index}.bin')
    else:
        p_index = str(img_info[0]).zfill(3)
        temp_raw_path = (cfg.convert_dir  / f'fmx{p_index}.raw')
        output_path  = (cfg.convert_dir  / f'fmx{p_index}.bin')

    # 競合するファイルがあれば削除
    if temp_raw_path.exists():
        temp_raw_path.unlink()

    # sox.exeを使って変換
    run_sox(cfg, input_path, temp_raw_path, is_bgm, p_no_music_threshold)

    # デバッグ用にwavファイルをdebug_dirにコピー
    if cfg.out_temp_file_checkbox:
        if is_bgm:
            temp_wav_path = temp_raw_path.with_suffix('.wav')
            debug_wav_path = Path(cfg.debug_dir / 'bgm' / f'bgm{p_index}.wav')
        else:
            temp_wav_path = temp_raw_path.with_suffix('.wav')
            debug_wav_path = Path(cfg.debug_dir / 'fmx' / f'fmx{p_index}.wav')

        temp_wav_path.replace(debug_wav_path)
    
    # 競合するファイルがあれば削除
    if output_path.exists(): 
        output_path.unlink()

    # 変換したrawファイルをrenameして出力パスに移動
    temp_raw_path.replace(output_path)

    return


def convert_audio(cfg: AppConfig) -> None:
    """音源の全変換処理"""

    # ボイス有無で変換リストを作成
    if (cfg.include_voice):
        fmx_list = (SE_LIST + VOICE_LIST)
    else:
        fmx_list = (SE_LIST)

    # プログレスバー計算用  
    prog_img = cfg.progress_dict["convert_images"]
    prog_aud = cfg.progress_dict["convert_audio"]
    all_list_len = len(BGM_LIST + fmx_list)
    
    # 無音ファイルパス
    dummy_raw_path = Path(cfg.convert_dir / f'dummy.raw')

    # 無音ファイル作成
    run_sox_dummy(cfg, dummy_raw_path)

    # 並列ファイル変換
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for img_info in BGM_LIST:
            # 音源の並列変換処理(is_bgm=True)
            futures.append(executor.submit(
                convert_audio_parallel, cfg, img_info, True))
            
        for img_info in fmx_list:
            # 音源の並列変換処理(is_bgm=True)
            futures.append(executor.submit(
                convert_audio_parallel, cfg, img_info, False))

        # 処理待ち&プログレスバー計算更新
        for i, ft in enumerate(concurrent.futures.as_completed(futures)):
            configure_progress_bar(
                prog_img + float(i / all_list_len) * (prog_aud - prog_img))
    
    # 無音ファイル削除
    dummy_raw_path.unlink()

    # プログレスバー更新
    configure_progress_bar(cfg.progress_dict["convert_audio"])

    return
    