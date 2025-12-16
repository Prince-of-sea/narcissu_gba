from pathlib import Path
import re



# from paths import SOX


def list_in_audio_paths(base_dir: Path = "") -> list:
    """音源パス一覧を取得（base_dirからの相対パス）"""
    
    # base_dirを絶対パスに解決しておくと、relative_toで扱いやすい
    base_path = Path(base_dir).resolve()
    
    # 検索対象のサブディレクトリと拡張子
    sub_dirs = ['bgm', 'se', 'w']
    extensions = ['*.wav', '*.mp3', '*.ogg']
    
    absolute_paths = []
    
    for sub_dir in sub_dirs:
        current_dir = base_path / sub_dir
        # ディレクトリが存在する場合のみ検索を実行
        if current_dir.is_dir():
            # rglobで見つかった絶対パスをリストに追加
            all_files_in_dir = [
                p.resolve() 
                for ext in extensions 
                for p in current_dir.rglob(ext)
            ]
            absolute_paths.extend(all_files_in_dir)

    # 見つかった絶対パスのリストを、base_path起点の相対パスに変換する
    in_audio_paths = [p.relative_to(base_path) for p in absolute_paths]
    
    return in_audio_paths


def list_out_audio_paths(in_audio_paths: list[Path]) -> list[Path]:
    """出力用音源パス一覧を作成 (親ディレクトリ名で判別)"""

    # === 事前に定義するID固定割り当て辞書 ===
    # キーは、ルートディレクトリを想定した相対パスの文字列
    # 値は、使用する連番の数値
    FIXED_ASSIGNMENTS: dict[Path, int] = {
        # .cソース側で音源ID直打ちが必要なとき(例:タイトル画面のbgm)とかは、
        # こっちで宣言させてその番号を利用します
        # 自動採番のIDと競合するので下記CNT_INIT_NUM以上の数値は書かないこと
        Path('bgm/3_1.mp3'): 7,
    }
    
    # 宣言
    out_audio_paths: list[str] = []
    
    # カウンタ初期化時定数(この数未満はID固定で利用)
    CNT_INIT_NUM = 10

    # SE最大値(これを超えるとボイスと競合する)
    SE_MAX = 100

    # カテゴリーごとのカウンターを初期化
    counters = {'bgm': CNT_INIT_NUM, 
                'se': CNT_INIT_NUM, 
                'voice': CNT_INIT_NUM
                }
    
    for path in in_audio_paths:
        # FIXED_ASSIGNMENTS 内に現在のパス (キー) が存在するかチェック
        if path in FIXED_ASSIGNMENTS:
            fixed_value = FIXED_ASSIGNMENTS[path]
            parent_dir_name = path.parent.name.lower()

            if parent_dir_name == 'bgm':
                # BGM の形式で固定値を適用
                new_filename = f"BGM{fixed_value:02d}"
            elif parent_dir_name == 'se' or parent_dir_name == 'voice':
                # SE または W の形式で固定値を適用
                new_filename = f"FMX{fixed_value:03d}"
            else:
                # FIXED_ASSIGNMENTS にあるが、親ディレクトリ名が想定外の場合
                print(f"Skipping fixed assignment for {path} due to unexpected parent directory name: {parent_dir_name}")
                continue # 次のファイルへスキップ
            
            out_audio_paths.append(new_filename)
            # print(f"Applied fixed assignment for {path}: {new_filename}")
            continue # このファイルは処理済みのため、次のループへ進む

        # === ここから自動連番処理 ===
        parent_dir_name = path.parent.name.lower()
        
        category = None

        if parent_dir_name == 'bgm':
            category = 'bgm'
        elif parent_dir_name == 'se':
            category = 'se'
        elif parent_dir_name == 'w': 
            category = 'voice'
        
        if category:
            # === 競合チェック ===
            if category == 'se' and counters['se'] >= (SE_MAX + counters['voice']):
                raise ValueError(f"連番競合エラー: 'se' の連番が 上限に到達しました。'voice' の連番と競合します。ファイル: {path.name}, 親ディレクトリ: {parent_dir_name}")
            
            # カテゴリーに基づいて新しいファイル名を生成
            if category == 'bgm':
                new_filename = f"BGM{counters[category]:02d}"
            elif category == 'se':
                new_filename = f"FMX{counters[category]:03d}"
            elif category == 'voice':
                new_filename = f"FMX{SE_MAX + counters[category]:03d}"
            
            # 新しいファイル名を配列に
            out_audio_paths.append(new_filename)
            
            # カウンターをインクリメント
            counters[category] += 1

        else:
            print(f"Skipping file as category not found in parent directory name: {parent_dir_name}, File: {path.name}")
            
    return out_audio_paths


def convert_with_sox(in_path: Path, out_path: Path) -> None:
    """sox での変換"""
    
    # 引数を受け取ってprintする処理(仮)
    print("-" * 20)
    print(f"入力パス (in_path): {in_path}")
    print(f"出力パス (out_path): {out_path}")

    return None


def convert_audio() -> None:
    """音源変換全処理"""
    base_dir = Path("D:/132_shuumatsu_gba/__test_ex/")
    temp_dir = Path("D:/132_shuumatsu_gba/__temp_ex/")
    
    in_audio_paths = list_in_audio_paths(base_dir)
    out_audio_paths = list_out_audio_paths(in_audio_paths)

    for in_path_rel, out_path_name in zip(in_audio_paths, out_audio_paths):

        # 入力パスをbase_dirを付けて絶対パスに変換
        in_path_abs = base_dir / in_path_rel
        
        # 出力パスをtemp_dirを付けて拡張子.WAV付きの絶対パスに変換
        out_path_abs = temp_dir / f"{out_path_name}.WAV"
        
        # convert_with_sox関数を呼び出す
        convert_with_sox(in_path_abs, out_path_abs)
        
    pass

#test
if __name__ == '__main__':
    convert_audio()