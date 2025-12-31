#!/usr/bin/env python3
from pathlib import Path
import re

from .paths import IMG_LIST, BGM_LIST, FMX_LIST

#####後で消す#####
input_path = Path('D:/132_shuumatsu_gba/0.txt')
temp_dir = Path('D:/132_shuumatsu_gba/gbfs/data/tmp/')
##################

'''
"_r", 1,// キー入力＋改ページ（紙アイコン）
"_t", 1,// キー入力＋改行（指アイコン）
"_m", 1,// テキスト表示
"_n", 1,// 改行
"!g", 1,// 背景
"!b", 1,// 音楽
"!e", 1,// 効果音
"!x", 2,// 立ち絵
"!j", 1,// スクリプトジャンプ
"!t", 1,// タイトル
"!s", 2,// 既読
"#g", 1,// CALL
"#r", 0,// RET
"#l", 0,// ELSE
"#n", 0,// ENDIF
"#i", 3,// IF
"#W", 1,// エフェクト
"#t", 1,// ウェイト
";;", 0,// 選択肢
"[]", 3,// 計算式
'''


# def find_scenario_paths(base_dir: str = "") -> list:
#     """シナリオファイル一覧を返す"""
#     pass


# def decrypt_0x84(data: bytes) -> bytes:
#     """0x84 複合化"""
#     pass


# def split_scenario_into_chapters(data: bytes) -> dict:
#     """章ごとに分割して辞書で返す"""
#     pass


# def convert_general_rules(text: str) -> str:
#     """汎用変換処理"""
#     pass


# def convert_special_rules(text: str) -> str:
#     """内部条件分岐を含む個別特殊変換"""
#     pass


# def join_scenario(chapters: dict) -> bytes:
#     """シナリオを結合してバイナリ化"""
#     pass


# def export_scenario_bin(bin_data: bytes, out_path: str) -> None:
#     """bin ファイル出力"""
#     pass


# def export_debug_text(bin_data: bytes, out_path: str) -> None:
#     """デバッグ用にテキスト形式で出力"""
#     pass


########## 仮関数 とりあえず適当に動くだけ あとで処理分け&クリーンアップする ###########
def convert_txt_to_gbabin(txt_lines):

    # パターン定義
    BGM_PATTERN            = r'^mp3\s+"(?P<arg1>[^"]*)"'
    BGM_LOOP_PATTERN       = r'^mp3loop\s+"(?P<arg1>[^"]*)"'
    BGM_FADEOUT_PATTERN    = r'^mp3fadeout\s+(?P<arg1>\d+)'
    SE_PATTERN             = r'^dwave\s+(?P<arg1>\d+),\s*"(?P<arg2>[^"]*)"'
    SE_LOOP_PATTERN        = r'^dwaveloop\s+(?P<arg1>\d+),\s*"(?P<arg2>[^"]*)"'
    SE_STOP_PATTERN        = r'^dwavestop\s+(?P<arg1>\d+)'
    STOP_ALL_PATTERN       = r'^stop$'
    BG_PATTERN             = r'^bg\s+"(?P<arg1>[^"]*)",\s*(?P<arg2>\d+)'
    TEXTCLEAR_PATTERN      = r'^textclear$'
    CLICK_PATTERN          = r'^click$'
    WAIT_PATTERN           = r'^wait\s+(?P<arg1>\d+)'
    WAIT_SHORT_PATTERN     = r'^!w(?P<arg1>\d+)'
    PAGE_TEXT_PATTERN      = r'^([^\x01-\x7E]|@)+\\'
    LINE_TEXT_PATTERN      = r'^([^\x01-\x7E]|@)+@'
    TEXT_PATTERN           = r'^([^\x01-\x7E]|@)+'
    TEXT_SPEED_RESET       = r'^!sd$'
    TEXT_SPEED_SET         = r'^!s(?P<arg1>\d+)'
    ERASE_TEXTWINDOW       = r'^erasetextwindow\s+'
    SET_WINDOW             = r'^setwindow\s+'
    MOV_STR_PATTERN        = r'^mov\s+\$(?P<arg1>.*),\s*"(?P<arg2>[^"]*)"'
    MOV_NUM_PATTERN        = r'^mov\s+\%(?P<arg1>.*),\s*(?P<arg2>\d+)'
    LABEL_PATTERN          = r'^\*(?P<arg1>.*)'

    # 正規表現そのものをキーにした辞書
    # キー：正規表現（名前付きグループ）
    # 値　：GBA側にシナリオとして読み込ませるためのバイナリそのもの
    # 追記...ここあとで統合予定　上のやつと被って滅茶苦茶なので
    PATTERNS = {
        # 上から順で読み取らせるので基準が緩いものほど下に

        BGM_PATTERN        : r'^mp3\s+"(?P<arg1>[^"]*)"',                        # bgm
        BGM_LOOP_PATTERN   : r'^mp3loop\s+"(?P<arg1>[^"]*)"',                    # bgmループ(とりあえず単発で実装)
        BGM_FADEOUT_PATTERN: r'^mp3fadeout\s+(?P<arg1>\d+)',                     # bgm止める
        SE_PATTERN         : r'^dwave\s+(?P<arg1>\d+),\s*"(?P<arg2>[^"]*)"',     # 効果音
        SE_LOOP_PATTERN    : r'^dwaveloop\s+(?P<arg1>\d+),\s*"(?P<arg2>[^"]*)"', # 効果音ループ(単発 or BGM扱い 検討中)
        SE_STOP_PATTERN    : r'^dwavestop\s+(?P<arg1>\d+)',                      # 効果音停止
        STOP_ALL_PATTERN   : r'^stop$',                                          # 音声全停止
        
        BG_PATTERN         : r'^bg\s+"(?P<arg1>[^"]*)",\s*(?P<arg2>\d+)',        # 背景
        
        TEXTCLEAR_PATTERN  : r'^textclear$',                                     # テキストクリア(ボイス無しでのみ使用？)
        CLICK_PATTERN      : r'^click$',                                         # クリックして次へ(空文章用意で実装)
        WAIT_PATTERN       : r'^wait\s+(?P<arg1>\d+)',                           # ウェイト
        WAIT_SHORT_PATTERN : r'^!w(?P<arg1>\d+)',                                # ウェイト
        
        PAGE_TEXT_PATTERN  : r'^([^\x01-\x7E]|@)+\\',                            # 改ページ文章
        LINE_TEXT_PATTERN  : r'^([^\x01-\x7E]|@)+@',                             # 改行文章
        TEXT_PATTERN       : r'^([^\x01-\x7E]|@)+',                              # 普通の文章
        
        # 面倒なので場所ごとに個別で潰す可能性の高い命令
        TEXT_SPEED_RESET   : r'^!sd$',                                           # 文字表示速度変更
        TEXT_SPEED_SET     : r'^!s(?P<arg1>\d+)',                                # 文字表示速度設定
        ERASE_TEXTWINDOW   : r'^erasetextwindow\s+',                             # 文字表示window削除
        SET_WINDOW         : r'^setwindow\s+',                                   # 文字表示位置設定
        
        MOV_STR_PATTERN    : r'^mov\s+\$(?P<arg1>.*),\s*"(?P<arg2>[^"]*)"',      # 文字変数代入(主に章のタイトルに利用)
        MOV_NUM_PATTERN    : r'^mov\s+\%(?P<arg1>.*),\s*(?P<arg2>\d+)',          # 数字変数代入(詳細不明)
        
        LABEL_PATTERN      : r'^\*(?P<arg1>.*)',                                 # jump用ラベル
    }

    # 仮
    command_cnt = '0014'

    line_command_list = []

    # 一行ごと読み込み
    for line in txt_lines:

        # 行頭/行末空白削除
        line = line.strip()

        # 行がある(=空白ではない)場合
        if line:

            ismatch = False

            # 正規表現検索
            for ptkey, ptval in PATTERNS.items():

                line_command = []

                # キーのパターンと一致
                if (matched_data := re.match(ptkey, line)):
                    ismatch = True

                    # BGM
                    if (ptkey in [BGM_PATTERN, BGM_LOOP_PATTERN]):
                        for iml in BGM_LIST:
                            if (Path(iml[1]) == Path(matched_data.group('arg1'))):
                                line_command = ['!b', str(iml[0]), str(command_cnt)]
                                break

                    # 効果音・ボイス
                    elif (ptkey in [SE_PATTERN, SE_LOOP_PATTERN]):
                        for iml in FMX_LIST:
                            if (Path(iml[1]) == Path(matched_data.group('arg2'))):
                                line_command = ['!e', str(iml[0]), str(command_cnt)]
                                break

                    # 音消す(SEループ削除は後で実装)
                    elif (ptkey in [BGM_FADEOUT_PATTERN, STOP_ALL_PATTERN]):
                        # DEBUG_LIST.append(matched_data.group('arg2'))
                        line_command = ['!b', str(1), str(command_cnt)]
                        pass
                    
                    # 背景
                    elif (ptkey in [BG_PATTERN]):
                        for iml in IMG_LIST:
                            if (Path(iml[1]) == Path(matched_data.group('arg1'))):
                                line_command = ['!g', str(iml[0]), str(command_cnt)]
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
                                line_command += ['_t', ls, str(command_cnt)]
                            
                            # 改ページ文章
                            elif (ptkey == PAGE_TEXT_PATTERN):
                                line_command += ['_r', ls, str(command_cnt)]
                            
                            # 普通の文章
                            elif (ptkey == TEXT_PATTERN):
                                line_command += ['_m', ls, str(command_cnt)]
                    
                    # 見出し
                    elif (ptkey in [MOV_STR_PATTERN]):
                        val_name = matched_data.group('arg1')
                        midasi = matched_data.group('arg2')

                        if (val_name.lower() == 'sys_midasi'):
                            midasi = midasi.replace(r'　ボイスＶｅｒ', r'')
                            line_command = ['!t', midasi, str(command_cnt)]
                        else:
                            print(f'unknown val_name: {line}')

                    if line_command:
                        line_command_list.append(line_command)
                    break

            if (ismatch == False):
                print(f'no_match: {line}')

    
    # 2→1次元配列へ変換
    scn_list = [item for sublist in line_command_list for item in sublist]
    
    return scn_list


def convert_scenario(debug: bool = False) -> None:
    """シナリオ変換の全処理"""

    scn_list = {
        '000': ['0', '0000', '!t', '起動処理', '0000', '#W', '200', '0000', '!g', '0', '0000', '#t', '1', '0000', '#W', '1', '0000', '!g', '1', '0000', '#t', '10', '0000', '!j', '1', '0000', ';;', ''],
        '003': ['0', '0000', '!t', '選択画面', '0000', '#W', '0', '0000', '!j', '5', '0014', ';;', ''], # 最終的にはここに選択肢入れてボイス有無選べるように
        '004': ['0', '0000', '!t', '起動ーボイスなし', '0000', '#W', '0', '0000'],
        '005': ['0', '0000', '!t', '起動ーボイスあり', '0000', '#W', '0', '0000'],
    }

    # 0.txtを読み取り
    with open(input_path, 'r', encoding='cp932') as file:
        lines = file.readlines()

    # 改行文字を削除
    lines = [line.strip() for line in lines]

    # 結果を表示
    scn_list['004'] += convert_txt_to_gbabin(lines[639:1101])# *image	    "プロローグ"
    scn_list['004'] += convert_txt_to_gbabin(lines[1105:2184])# *honpen2	"７階"
    scn_list['004'] += convert_txt_to_gbabin(lines[2188:3690])# *honpen3	"銀のクーペ"
    scn_list['004'] += convert_txt_to_gbabin(lines[3693:4945])# *honpen4	"地図"
    scn_list['004'] += convert_txt_to_gbabin(lines[4948:5926])# *honpen5	"エメラルドの海"
    scn_list['004'] += convert_txt_to_gbabin(lines[5930:7258])# *honpen6	"一号線"
    scn_list['004'] += convert_txt_to_gbabin(lines[7263:8255])# *honpen7	"エコー"
    scn_list['004'] += convert_txt_to_gbabin(lines[8257:9471])# *honpen8	"ナルキッソス"
    scn_list['004'] += convert_txt_to_gbabin(lines[9474:10120])# *honpen9	"白石工務店"
    scn_list['004'] += (['!j', '1', '0014', ';;', ''])

    scn_list['005'] += (convert_txt_to_gbabin(lines[10126:10598]))# *image_voice	"プロローグ　ボイスＶｅｒ  "		10126	10598
    scn_list['005'] += (convert_txt_to_gbabin(lines[10622:11709]))# *honpen2_voice	"７階　ボイスＶｅｒ"			10622	11709
    scn_list['005'] += (convert_txt_to_gbabin(lines[11717:13244]))# *honpen3_voice	"銀のクーペ　ボイスＶｅｒ"		11717	13244
    scn_list['005'] += (convert_txt_to_gbabin(lines[13247:14528]))# *honpen4_voice	"地図　ボイスＶｅｒ"			13247	14528
    scn_list['005'] += (convert_txt_to_gbabin(lines[14531:15539]))# *honpen5_voice	"エメラルドの海　ボイスＶｅｒ"	14531	15539
    scn_list['005'] += (convert_txt_to_gbabin(lines[15543:16884]))# *honpen6_voice	"一号線　ボイスＶｅｒ"			15543	16884
    scn_list['005'] += (convert_txt_to_gbabin(lines[16889:17897]))# *honpen7_voice	"エコー　ボイスＶｅｒ"			16889	17897
    scn_list['005'] += (convert_txt_to_gbabin(lines[17899:19128]))# *honpen8_voice	"ナルキッソス　ボイスＶｅｒ"	17899	19128
    scn_list['005'] += (convert_txt_to_gbabin(lines[19131:19758]))# *honpen9_voice	"白石工務店　ボイスＶｅｒ"		19131	19758
    scn_list['005'] += (['!j', '1', '0014', ';;', ''])

    for scn_key, scn_val in scn_list.items():

        output_path = temp_dir / f'SCN{scn_key}.bin'

        scn_temp = [s.encode('cp932') for s in scn_val]
        scn_bin = b"\x00".join(scn_temp)
        
        with open(output_path, "wb") as f:
            f.write(scn_bin)
        
    pass


if __name__ == '__main__':
    # シナリオの全変換処理
    convert_scenario()