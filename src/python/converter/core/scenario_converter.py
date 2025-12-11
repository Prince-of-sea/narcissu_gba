def find_scenario_paths(base_dir: str = "") -> list:
    """シナリオファイル一覧を返す"""
    pass


def decrypt_0x84(data: bytes) -> bytes:
    """0x84 複合化"""
    pass


def split_scenario_into_chapters(data: bytes) -> dict:
    """章ごとに分割して辞書で返す"""
    pass


def convert_general_rules(text: str) -> str:
    """汎用変換処理"""
    pass


def convert_special_rules(text: str) -> str:
    """内部条件分岐を含む個別特殊変換"""
    pass


def join_scenario(chapters: dict) -> bytes:
    """シナリオを結合してバイナリ化"""
    pass


def export_scenario_bin(bin_data: bytes, out_path: str) -> None:
    """bin ファイル出力"""
    pass


def export_debug_text(bin_data: bytes, out_path: str) -> None:
    """デバッグ用にテキスト形式で出力"""
    pass


def convert_scenario(debug: bool = False) -> None:
    """シナリオ変換の全処理"""
    pass
