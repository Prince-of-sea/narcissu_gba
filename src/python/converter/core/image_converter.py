def list_image_paths(base_dir: str = "") -> list:
    """画像パス一覧を取得"""
    pass


def compress_image(img):
    """圧縮処理"""
    pass


def crop_image(img):
    """クロップ処理"""
    pass


def apply_common_effects(img):
    """汎用特殊効果 (アンシャープマスク等)"""
    pass


def apply_special_effects(img):
    """個別特殊効果 (黒塗り等)"""
    pass


def reduce_color(img):
    """減色処理"""
    pass


def export_temp_file(img, out_path: str):
    """一時ファイルとして保存"""
    pass


def run_grit(in_path: str, out_path: str) -> None:
    """grit.exe を使って変換"""
    pass


def append_footer_data(filepath: str) -> None:
    """末尾に独自データを追記"""
    pass


def convert_images() -> None:
    """画像の全変換処理"""
    pass
