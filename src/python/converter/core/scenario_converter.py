#!/usr/bin/env python3
from pathlib import Path
import math
import re

from core.config import AppConfig
from core.gui_utils import configure_progress_bar
from .paths import IMG_LIST, BGM_LIST, SE_LIST, VOICE_LIST


# 謎コマンドカウンタ(?)管理クラス - コマンドごとにインクリメントされていく数値を16進数で文字列化して返す
# いまいちなんのために使われてるか不明だが、雰囲気だけでも元のエンジンに合わせるために一応実装
class CommandCnt:
    def __init__(self, initial_value=0):
        self._value = initial_value

    def get_str(self):
        """1. 今の数を16進数の文字列で出力"""
        return format(self._value, '04X')

    def add(self, amount):
        """2. 引数分だけ足す"""
        self._value += amount

    def reset(self):
        """3. 0初期化"""
        self._value = 0


# !s命令用カウンタ管理クラス
class StepCnt:
    def __init__(self):
        self.count_a = 0
        self.count_b = 0

    def call(self, val_x):
        """引数を受け取り、カウントアップして [A, B, X] を返す"""
        self.count_b += 1
        
        # 8進法のように、8に達した瞬間に繰り上げ
        if self.count_b >= 8:
            self.count_b = 0
            self.count_a += 1
            
        return [str(val_x), '!s', str(self.count_a), str(self.count_b)]

    def reset(self):
        """カウントを初期化する"""
        self.count_a = 0
        self.count_b = 0


def decrypt_0x84(data: bytes) -> bytes:
    """0x84 複合化(nscript.dat用)"""

    # 復号したバイナリを格納する配列の作成
    bin_list = []

    # 復号 0x84でbitxor
    for b in range(len(data)):
        bin_list.append(bytes.fromhex(
            str((hex(int(data[b]) ^ int(0x84))[2:].zfill(2)))))
        
    # バイト列を文字列に変換
    decode_text = (b''.join(bin_list)).decode('cp932', errors='ignore')

    return decode_text


def extract_concept(text):
    """文字列を抽出する正規表現 - "（"以降は除外"""
    match = re.search(r'(csel )?"　■　(.+?)(（.+)?",\*ns[0-9]{2},', text)
    if match:
        return match.group(2)
    return None


def convert_txt_main(cmd_cnt: CommandCnt, s_cnt: StepCnt, txt_lines: list[str], is_product: bool, cfg: AppConfig) -> list[str]:
    """シナリオ変換メイン処理"""

    # パターン定義
    # 上から順で読み取らせるので基準が緩いものほど下に
    BGM_PATTERN            = r'^mp3\s+"(?P<arg1>[^"]*)"'                         # bgm
    BGM_LOOP_PATTERN       = r'^mp3loop\s+"(?P<arg1>[^"]*)"'                     # bgmループ(とりあえず単発で実装)
    BGM_FADEOUT_PATTERN    = r'^mp3fadeout\s+(?P<arg1>\d+)'                      # bgm止める
    SE_PATTERN             = r'^dwave\s+(?P<arg1>\d+),\s*"(?P<arg2>[^"]*)"'      # 効果音
    SE_LOOP_PATTERN        = r'^dwaveloop\s+(?P<arg1>\d+),\s*"(?P<arg2>[^"]*)"'  # 効果音ループ(単発 or BGM扱い 検討中)
    SE_STOP_PATTERN        = r'^dwavestop\s+(?P<arg1>\d+)'                       # 効果音停止
    STOP_ALL_PATTERN       = r'^stop$'                                           # 音声全停止

    BG_PATTERN             = r'^bg\s+"(?P<arg1>[^"]*)",\s*(?P<arg2>\d+)'         # 背景

    TEXTCLEAR_PATTERN      = r'^textclear$'                                      # テキストクリア(ボイス無しでのみ使用？)
    CLICK_PATTERN          = r'^click$'                                          # クリックして次へ(空文章用意で実装)
    WAIT_PATTERN           = r'^wait\s+(?P<arg1>\d+)'                            # ウェイト
    WAIT_SHORT_PATTERN     = r'^!w(?P<arg1>\d+)'                                 # ウェイト

    PAGE_TEXT_PATTERN      = r'^([^\x01-\x7E]|@)+\\'                             # 改ページ文章
    LINE_TEXT_PATTERN      = r'^([^\x01-\x7E]|@)+@'                              # 改行文章
    TEXT_PATTERN           = r'^([^\x01-\x7E]|@)+'                               # 普通の文章
    
    # 面倒なので場所ごとに個別で潰す可能性の高い命令
    TEXT_SPEED_RESET       = r'^!sd$'                                            # 文字表示速度変更
    TEXT_SPEED_SET         = r'^!s(?P<arg1>\d+)'                                 # 文字表示速度設定
    ERASE_TEXTWINDOW       = r'^erasetextwindow\s+'                              # 文字表示window削除
    SET_WINDOW             = r'^setwindow\s+'                                    # 文字表示位置設定

    MOV_STR_PATTERN        = r'^mov\s+\$(?P<arg1>.*),\s*"(?P<arg2>[^"]*)"'       # 文字変数代入(主に章のタイトルに利用)
    MOV_NUM_PATTERN        = r'^mov\s+\%(?P<arg1>.*),\s*(?P<arg2>\d+)'           # 数字変数代入(詳細不明)

    LABEL_PATTERN          = r'^\*(?P<arg1>.*)'                                  # jump用ラベル

    # 正規表現
    PATTERNS = [
        BGM_PATTERN, BGM_LOOP_PATTERN, BGM_FADEOUT_PATTERN, SE_PATTERN, SE_LOOP_PATTERN,
        SE_STOP_PATTERN, STOP_ALL_PATTERN, BG_PATTERN, TEXTCLEAR_PATTERN, CLICK_PATTERN,
        WAIT_PATTERN, WAIT_SHORT_PATTERN, PAGE_TEXT_PATTERN, LINE_TEXT_PATTERN, TEXT_PATTERN,
        TEXT_SPEED_RESET, TEXT_SPEED_SET, ERASE_TEXTWINDOW, SET_WINDOW, MOV_STR_PATTERN,
        MOV_NUM_PATTERN, LABEL_PATTERN, 
    ]

    # 出力用配列
    line_command_list = []

    # エンディング直前フラグ
    ending_flug = False

    # 一行ごと読み込み
    for line in txt_lines:

        # 行頭/行末空白削除
        line = line.strip()

        # Productシナリオの場合の正規表現を使った個別修正
        if is_product:

            # GBA版には無いパスの修正や文字列はみ出し対策など
            # そのままだと不具合や不都合の原因になるので
            line = line.replace('"bgm\\e01.mp3"', '"tui2\\e01.mp3"')
            line = line.replace('こんな↑感じ', 'こんな感じ')
            line = line.replace('れませんが、', 'れませんが、\\')
            line = line.replace('なってしまいました。', 'なってしまいました。\\')
            line = line.replace('したら、', 'したら、\\')

        # 行がある(=空白ではない)場合
        if line:

            ismatch = False

            # 正規表現検索
            for ptkey in PATTERNS:

                line_command = []

                # キーのパターンと一致
                if (matched_data := re.match(ptkey, line)):
                    ismatch = True

                    # BGM
                    if (ptkey in [BGM_PATTERN, BGM_LOOP_PATTERN]):
                        bgm_path = matched_data.group('arg1')

                        for iml in BGM_LIST:
                            if (Path(iml[1]) == Path(bgm_path)):
                                cmd_cnt.add(20)
                                line_command = [cmd_cnt.get_str(), '!b', str(iml[0])]
                                line_command += s_cnt.call(cmd_cnt.get_str())
                                break

                    # 効果音・ボイス
                    elif (ptkey in [SE_PATTERN, SE_LOOP_PATTERN]):
                        se_path = matched_data.group('arg2')

                        for iml in (SE_LIST + VOICE_LIST):
                            if (Path(iml[1]) == Path(se_path)):
                                line_command = [cmd_cnt.get_str(), '!e', str(iml[0])]
                                break

                    # 音消す(SEループ削除は後で実装)
                    elif (ptkey in [BGM_FADEOUT_PATTERN, STOP_ALL_PATTERN]):
                        # DEBUG_LIST.append(matched_data.group('arg2'))
                        line_command = [cmd_cnt.get_str(), '!b', str(1)]
                        pass
                    
                    # 背景
                    elif (ptkey in [BG_PATTERN]):
                        bg_path = matched_data.group('arg1')
                        bg_fadenum_nsc = matched_data.group('arg2')

                        # 0.txt エフェクト定義参照
                        #   effect 2,6,500
                        #   effect 3,10,600
                        #   effect 4,13,3000
                        #   effect 5,10,800
                        #   effect 6,6,500

                        match bg_fadenum_nsc:
                            case '2':
                                wait_time = 5
                            case '3':
                                wait_time = 6
                            case '4':
                                wait_time = 30
                            case '5':
                                wait_time = 8
                            case '6':
                                wait_time = 5
                            case _:
                                wait_time = 1
                        
                        # 原作のエンジンは指定値より若干遅くなるっぽいので補正
                        wait_time += 3

                        # 画像リストでBGに該当するパスを探す
                        for iml in IMG_LIST:

                            # ファイル名が一致
                            if (Path(iml[1]) == Path(bg_path)):
                                iml_0 = iml[0]

                                # 130番は特殊扱い - 129と同じ画像なので129扱い
                                if (iml_0 == 130):
                                    iml_0 = 129
                                
                                cmd_cnt.add(20)
                                line_command = [cmd_cnt.get_str(), '!g', str(iml_0)]

                                # -以下画像切り替えフェード用のウェイト追加-
                                cmd_cnt.add(20)

                                # [特殊]エンディング直前(直前であることをcソース側で検知させるために他と被らない数値で指定)
                                if (ending_flug):
                                    line_command += [cmd_cnt.get_str(), '#t', str(12)]
                                    ending_flug = False
                                
                                # それ以外は通常のウェイト指定
                                else:
                                    line_command += [cmd_cnt.get_str(), '#t', str(wait_time)]

                                line_command += s_cnt.call(cmd_cnt.get_str())

                                # ファイル名が一致したらループ抜ける
                                break

                    # テキスト
                    elif (ptkey in [PAGE_TEXT_PATTERN, LINE_TEXT_PATTERN, TEXT_PATTERN]):

                        # 処理詰まりそうなので修正
                        line = line.replace(r'@/', '@')

                        # 改ページ・改行文章は最後の一文字外す
                        if (ptkey in [PAGE_TEXT_PATTERN, LINE_TEXT_PATTERN]):
                            line = line[:-1]

                        # 途中クリック待ちで分割
                        line_split = line.split('@')

                        # 最後の文字列とそれ以外で処理変えるため取得
                        ls_last_index = len(line_split) - 1

                        # 文章を分割して処理する
                        for i, ls in enumerate(line_split):

                            # 改行文章or表示途中(元々改行だった文章であり、GBA表示時に改行するわけではない)
                            if (ptkey == LINE_TEXT_PATTERN) or (i != ls_last_index):

                                #通常時
                                if (not is_product):
                                    line_command += [cmd_cnt.get_str(), '_t', ls]

                                # Productシナリオ時 - 改ページ扱いに変更
                                else:
                                    line_command += [cmd_cnt.get_str(), '_r', ls]
                            
                            # 改ページ文章
                            elif (ptkey == PAGE_TEXT_PATTERN):
                                line_command += [cmd_cnt.get_str(), '_r', ls]
                            
                            # 普通の文章
                            elif (ptkey == TEXT_PATTERN):
                                line_command += [cmd_cnt.get_str(), '_m', ls]
                            
                            # エンディング手前かどうかチェック
                            if (ls == b'\x81c\x81c\x8ec\x82\xb9\x82\xbd\x89\xb4\x92B\x82\xcc\x8f\xd8\x82\xb5\x81c\x81c'.decode('cp932')):
                                ending_flug = True

                    # 見出し
                    elif (ptkey in [MOV_STR_PATTERN]):
                        val_name = matched_data.group('arg1')
                        midasi = matched_data.group('arg2')

                        if (val_name.lower() == 'sys_midasi'):
                            cmd_cnt.add(20)
                            midasi = midasi.replace(r'　ボイスＶｅｒ', r'')
                            line_command = [cmd_cnt.get_str(), '!t', midasi]
                            line_command += s_cnt.call(cmd_cnt.get_str())
                        else:
                            raise Exception (f'unknown val_name: {line}')
                        
                    # クリック待ち
                    elif (ptkey in [CLICK_PATTERN]):
                        line_command += [cmd_cnt.get_str(), '_r', '　'*68]

                    # ウェイト
                    elif (ptkey in [WAIT_PATTERN, WAIT_SHORT_PATTERN]):
                        wait_time_rawstr = matched_data.group('arg1')
                        wait_time_rawint = int(wait_time_rawstr)
                        wait_time = math.ceil(wait_time_rawint / 100)

                        if (wait_time < 1):
                            wait_time = 1
                        
                        cmd_cnt.add(20)
                        line_command = [cmd_cnt.get_str(), '#t', str(wait_time)]
                        line_command += s_cnt.call(cmd_cnt.get_str())

                    if line_command:
                        line_command_list.append(line_command)
                    break

            if (ismatch == False):
                raise Exception (f'no_match: {line}')

    
    # 2→1次元配列へ変換
    scn_list = [item for sublist in line_command_list for item in sublist]
    
    return scn_list


def convert_txt(lines: list[str], cfg: AppConfig) -> dict:
    """シナリオテキスト変換の全処理"""

    # 必要な初期データ準備(共通)
    scn_list = {
        '000': ['0', '0000', '!t', '起動', '0000', '#W', '200', '0000', '#t', '10', '0000', 
                '!g', '0', '0000', '#t', '6', '0000', '!g', '1', '0000', '#t', '6', '0000', '!j', '1', '0000', ';;', ''],
        
        '005': ['0', '0000', '#W',  '0', '0000', '#t',  '1', '0000', '#W', '1'],
        '006': ['0', '0000', '!t', 'プロダクト',   '0000', '#W', '0'],
    }

    # ボイス有りの場合は004追加
    if (cfg.include_voice):
        scn_list['004'] = ['0', '0000', '#W',  '0', '0000', '#t',  '1', '0000', '#W', '1']

    # ボイス無しの場合は自動ジャンプ用003追加
    else:
        scn_list['003'] = ['0', '0000', '!j',  '5', ';;', '']
    

    # 謎コマンドカウンタ管理クラス初期化
    cmd_cnt  = CommandCnt()

    # !s命令用カウンタ管理クラス初期化
    s_cnt = StepCnt()

    # ボイス有り版
    if (cfg.include_voice):
        cmd_cnt.reset()
        cmd_cnt.add(20)
        scn_list['004'] += (convert_txt_main(cmd_cnt, s_cnt, lines[10126:10598], False, cfg))
        if (cfg.ch1_subtitle_checkbox):
            scn_list['004'] += ([cmd_cnt.get_str(), '!g', '2', cmd_cnt.get_str(), '#t', '120'])
        scn_list['004'] += (convert_txt_main(cmd_cnt, s_cnt, lines[10622:11709], False, cfg))
        scn_list['004'] += ([cmd_cnt.get_str(), '!g', '3', cmd_cnt.get_str(), '#t', '120'])
        scn_list['004'] += (convert_txt_main(cmd_cnt, s_cnt, lines[11717:13244], False, cfg))
        scn_list['004'] += ([cmd_cnt.get_str(), '!g', '4', cmd_cnt.get_str(), '#t', '120'])
        scn_list['004'] += (convert_txt_main(cmd_cnt, s_cnt, lines[13247:14528], False, cfg))
        scn_list['004'] += ([cmd_cnt.get_str(), '!g', '5', cmd_cnt.get_str(), '#t', '120'])
        scn_list['004'] += (convert_txt_main(cmd_cnt, s_cnt, lines[14531:15539], False, cfg))
        scn_list['004'] += ([cmd_cnt.get_str(), '!g', '6', cmd_cnt.get_str(), '#t', '120'])
        scn_list['004'] += (convert_txt_main(cmd_cnt, s_cnt, lines[15543:16884], False, cfg))
        scn_list['004'] += ([cmd_cnt.get_str(), '!g', '7', cmd_cnt.get_str(), '#t', '120'])
        scn_list['004'] += (convert_txt_main(cmd_cnt, s_cnt, lines[16889:17897], False, cfg))
        scn_list['004'] += ([cmd_cnt.get_str(), '!g', '8', cmd_cnt.get_str(), '#t', '120'])
        scn_list['004'] += (convert_txt_main(cmd_cnt, s_cnt, lines[17899:19128], False, cfg))
        scn_list['004'] += ([cmd_cnt.get_str(), '!g', '9', cmd_cnt.get_str(), '#t', '120'])
        scn_list['004'] += (convert_txt_main(cmd_cnt, s_cnt, lines[19131:19758], False, cfg))
        scn_list['004'] += ([cmd_cnt.get_str(), '!g', '1', cmd_cnt.get_str(), '#t', '1', cmd_cnt.get_str(), '!j', '1', cmd_cnt.get_str(), ';;', ''])

    # ボイス無し版
    cmd_cnt.reset()
    cmd_cnt.add(20)
    scn_list['005'] += convert_txt_main(cmd_cnt, s_cnt, lines[639:1101], False, cfg)
    if (cfg.ch1_subtitle_checkbox):
        scn_list['005'] += ([cmd_cnt.get_str(), '!g', '2', cmd_cnt.get_str(), '#t', '120'])
    scn_list['005'] += convert_txt_main(cmd_cnt, s_cnt, lines[1105:2184], False, cfg)
    scn_list['005'] += ([cmd_cnt.get_str(), '!g', '3', cmd_cnt.get_str(), '#t', '120'])
    scn_list['005'] += convert_txt_main(cmd_cnt, s_cnt, lines[2188:3690], False, cfg)
    scn_list['005'] += ([cmd_cnt.get_str(), '!g', '4', cmd_cnt.get_str(), '#t', '120'])
    scn_list['005'] += convert_txt_main(cmd_cnt, s_cnt, lines[3693:4945], False, cfg)
    scn_list['005'] += ([cmd_cnt.get_str(), '!g', '5', cmd_cnt.get_str(), '#t', '120'])
    scn_list['005'] += convert_txt_main(cmd_cnt, s_cnt, lines[4948:5926], False, cfg)
    scn_list['005'] += ([cmd_cnt.get_str(), '!g', '6', cmd_cnt.get_str(), '#t', '120'])
    scn_list['005'] += convert_txt_main(cmd_cnt, s_cnt, lines[5930:7258], False, cfg)
    scn_list['005'] += ([cmd_cnt.get_str(), '!g', '7', cmd_cnt.get_str(), '#t', '120'])
    scn_list['005'] += convert_txt_main(cmd_cnt, s_cnt, lines[7263:8255], False, cfg)
    scn_list['005'] += ([cmd_cnt.get_str(), '!g', '8', cmd_cnt.get_str(), '#t', '120'])
    scn_list['005'] += convert_txt_main(cmd_cnt, s_cnt, lines[8257:9471], False, cfg)
    scn_list['005'] += ([cmd_cnt.get_str(), '!g', '9', cmd_cnt.get_str(), '#t', '120'])
    scn_list['005'] += convert_txt_main(cmd_cnt, s_cnt, lines[9474:10120], False, cfg)
    scn_list['005'] += ([cmd_cnt.get_str(), '!g', '1', cmd_cnt.get_str(), '#t', '1', cmd_cnt.get_str(), '!j', '1', cmd_cnt.get_str(), ';;', ''])
    
    # Ｐｒｏｄｕｃｔシナリオ
    cmd_cnt.reset()
    cmd_cnt.add(20)
    s_cnt.reset()
    scn_list['006'] += (convert_txt_main(cmd_cnt, s_cnt, lines[298:319], True, cfg))
    scn_list['006'] += ([cmd_cnt.get_str(), '!t', extract_concept(lines[321])])
    scn_list['006'] += (convert_txt_main(cmd_cnt, s_cnt, lines[327:375], True, cfg))
    scn_list['006'] += ([cmd_cnt.get_str(), '!t', extract_concept(lines[322])])
    scn_list['006'] += (convert_txt_main(cmd_cnt, s_cnt, lines[378:481], True, cfg))
    scn_list['006'] += ([cmd_cnt.get_str(), '!t', extract_concept(lines[323])])
    scn_list['006'] += (convert_txt_main(cmd_cnt, s_cnt, lines[485:525], True, cfg))
    scn_list['006'] += ([cmd_cnt.get_str(), '!t', extract_concept(lines[324])])
    scn_list['006'] += (convert_txt_main(cmd_cnt, s_cnt, lines[528:570], True, cfg))
    scn_list['006'] += ([cmd_cnt.get_str(), '!g', '1', cmd_cnt.get_str(), '#t', '1', cmd_cnt.get_str(), '!j', '1', cmd_cnt.get_str(), ';;', ''])

    return scn_list


def create_scenario_files(scn_list: dict, cfg: AppConfig) -> None:
    """シナリオファイル作成"""

    # シナリオごとにbinファイル作成
    for scn_key, scn_val in scn_list.items():

        output_bin_path = cfg.convert_dir / f'SCN{scn_key}.bin'
        scn_temp = [s.encode('cp932') for s in scn_val]
        scn_bin = b"\x00".join(scn_temp)
        
        with open(output_bin_path, "wb") as f:
            f.write(scn_bin)

        # デバッグ用テキスト出力
        if (cfg.out_temp_file_checkbox):
            output_txt_path = Path(cfg.debug_dir / 'scn' / f'SCN{scn_key}.txt')
            debug_txt = "\n".join(scn_val)
            
            with open(output_txt_path, "w", encoding="cp932") as f:
                f.write(debug_txt)
    
    return


def convert_txt_select_main(d: dict) -> bytes:
    """選択肢シナリオ変換メイン処理"""
    data = bytearray()
    data_add_list = []
    
    # 選択肢の数を追加
    data += str(len(d.items())).encode("shift_jis")

    # 区切りのためのNULLバイト
    data += b"\x00"

    for key in d.keys():
        # キーをShift_JISでエンコードして追加
        data += key.encode("shift_jis")

        # 区切りのためのNULLバイト
        data += b"\x00"

        # データの追加位置を記録
        data_add_list.append(len(data))

        # 仮
        data += b"\xFF\xFF"

        # 区切りのためのNULLバイト
        data += b"\x00\x00\x00"

    # 区切りのためのNULLバイト
    data += b"\x00"

    # エラー時終了用区切り？
    data += ';;'.encode("shift_jis")

    # 区切りのためのNULLバイト
    data += b"\x00"

    for i, value in enumerate(d.values()):

        # data_add_list[i]の位置からdata_add_list[i]+1の場所に、現在のdataの長さを2バイトで上書きする
        # 但し逆に(10A0の場合はA0 10の順で上書きする)
        data[data_add_list[i]:data_add_list[i]+2] = len(data).to_bytes(2, byteorder='little')

        # 既読管理(仮)
        data += '0000'.encode("shift_jis")

        # 区切りのためのNULLバイト
        data += b"\x00"

        # ジャンプ
        data += '!j'.encode("shift_jis")

        # 区切りのためのNULLバイト
        data += b"\x00"

        # 飛び先の値
        data += str(value).encode("shift_jis")

        # 区切りのためのNULLバイト
        data += b"\x00"

        # 既読管理(仮)
        data += '0000'.encode("shift_jis")

        # 区切りのためのNULLバイト
        data += b"\x00"

        # エラー時終了用区切り？
        data += ';;'.encode("shift_jis")

        # 区切りのためのNULLバイト
        data += b"\x00"

    return bytes(data)


def create_scenario_select_files(cfg: AppConfig) -> None:
    """選択肢シナリオ変換の全処理"""

    # ボイス有無選択肢 - ボイス有りの時のみ実装
    if (cfg.include_voice):

        # 選択肢シナリオ変換(今回はとりあえず1つだけ実装)
        d = {"ボイス有り": 4, "ボイス無し": 5}
        select_bin = convert_txt_select_main(d)

        # 保存
        with open(cfg.convert_dir / 'SCN003.bin', 'wb') as f:
            f.write(select_bin)
    
    return


def create_savid(cfg: AppConfig) -> None:
    """savid 作成"""
    
    # byte列として変数に格納
    # 終末GBAと同一内容のものをもってきただけなので詳細不明
    savid_hex = bytes.fromhex('53 52 41 4D 5F 56 6E 6E 6E 00 00 00 00 00 00 00')

    # ファイル「savid.bin」として保存
    with open(cfg.convert_dir / 'savid.bin', 'wb') as f:
        f.write(savid_hex)


def convert_scenario(cfg: AppConfig) -> None:
    """シナリオ変換の全処理"""

    # nscript.dat 読み込み
    nsdat_data = open(cfg.nsdat_path, 'rb').read()

    # 複合化
    lines = decrypt_0x84(nsdat_data).splitlines()

    # 改行文字を削除
    lines = [line.strip() for line in lines]

    # シナリオ変換
    scn_list = convert_txt(lines, cfg)

    # シナリオ書き出し
    create_scenario_files(scn_list, cfg)

    # 選択肢シナリオ変換&書き出し
    create_scenario_select_files(cfg)
    
    # savid作成
    create_savid(cfg)

    # プログレスバー更新
    configure_progress_bar(cfg.progress_dict["convert_scenario"], True)

        
    return