#!/usr/bin/env python3
from pathlib import Path
import subprocess
import shutil

from core.config import AppConfig
from core.gui_utils import configure_progress_bar


def join_binary_files(cfg: AppConfig):
    """
    2つのバイナリファイルを明示的に1つに結合する
    """
    out = Path(cfg.result_gba)
    src1 = Path(cfg.base_gba)
    src2 = Path(cfg.gbfs_path)

    if out.is_file():
       out.unlink() 

    with out.open("wb") as outfile:
        # 1つ目のファイルをコピー
        with src1.open("rb") as infile1:
            shutil.copyfileobj(infile1, outfile)
        
        # 2つ目のファイルをコピー
        with src2.open("rb") as infile2:
            shutil.copyfileobj(infile2, outfile)
    
    # プログレスバー更新
    configure_progress_bar(cfg.progress_dict["join_binary_files"], True)

    return


def run_gbfs(cfg: AppConfig) -> None:
    """gbfs.exe を使ってパックする"""

    cmd = [cfg.gbfs_exe, cfg.gbfs_path, f'{cfg.convert_dir}/*.*']
    result = subprocess.run(cmd, cwd = cfg.convert_dir, stdout=subprocess.PIPE, text=True)

    # デバッグモード時
    if cfg.debug_mode:

        # ログを保存
        log_path = Path(cfg.debug_dir / "gbfs_log.txt")
        with log_path.open('w', encoding='utf-8') as log_file:
            log_file.write(result.stdout)

        # _binフォルダに中間生成物を保存
        debug_bin_dir = Path(cfg.debug_dir / '_bin')
        debug_bin_dir.mkdir(exist_ok=True)
        for p in cfg.convert_dir.glob('*'):
            if (p.is_file() and cfg.gbfs_path.name not in p.name):
                p.replace(debug_bin_dir / p.name)
    
    # プログレスバー更新
    configure_progress_bar(cfg.progress_dict["run_gbfs"], True)
    
    return


def clear_directory(cfg: AppConfig) -> None:
    """不要ディレクトリの中身全部消す"""

    shutil.rmtree(cfg.convert_dir)
    shutil.rmtree(cfg.extract_dir)

    if (cfg.debug_dir).exists():
        shutil.rmtree(cfg.debug_dir)
    
    return


def pack_resources(cfg: AppConfig) -> None:
    """結合処理全体"""
    run_gbfs(cfg)
    join_binary_files(cfg)

    # デバッグモード時はdebug_dir内の中間生成物を保存
    if (cfg.debug_mode):
        # debug_dirをoutput_dir以下にコピー
        if cfg.output_debug_dir.exists():
            shutil.rmtree(cfg.output_debug_dir)

        shutil.copytree(cfg.debug_dir, cfg.output_debug_dir)
    
    # 最後に全部消す
    clear_directory(cfg)

    return