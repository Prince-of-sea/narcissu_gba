from pathlib import Path
import sys


# ===== 基準ディレクトリ =====
def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parents[2]


BASE_DIR = get_base_dir()


# ===== 外部ツール =====
GAR_BRO = BASE_DIR / "tools/garbro/GARBro.Console.exe"  #仮 できれば消したいよね
SOX     = BASE_DIR / "tools/sox/sox.exe"
GRIT    = BASE_DIR / "tools/grit/grit.exe"
GBFS    = BASE_DIR / "tools/gbfs/gbfs.exe"


# ===== データディレクトリ =====
DATA_RAW  = BASE_DIR / "data/raw"
DATA_WORK = BASE_DIR / "data/work"
DATA_OUT  = BASE_DIR / "data/out"


# ===== ユーティリティ =====
def abs_path(p: Path) -> Path:
    """
    subprocess 用：絶対パスに解決
    """
    return p.expanduser().resolve()
