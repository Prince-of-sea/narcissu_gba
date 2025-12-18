from pathlib import Path
import re
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

起点を「1行」とした記録
つまり配列に入れるときは -1 しようね
開始地点は*表記から
終了はgoto行

*image_voice	"プロローグ　ボイスＶｅｒ  "		10126	10598
*honpen2_voice	"７階　ボイスＶｅｒ"			10622	11709
*honpen3_voice	"銀のクーペ　ボイスＶｅｒ"		11717	13244
*honpen4_voice	"地図　ボイスＶｅｒ"			13247	14528
*honpen5_voice	"エメラルドの海　ボイスＶｅｒ"	14531	15539
*honpen6_voice	"一号線　ボイスＶｅｒ"			15543	16884
*honpen7_voice	"エコー　ボイスＶｅｒ"			16889	17897
*honpen8_voice	"ナルキッソス　ボイスＶｅｒ"	17899	19128
*honpen9_voice	"白石工務店　ボイスＶｅｒ"		19131	19758
'''


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
    PATTERNS = {
        # 上から順で読み取らせるので基準が緩いものほど下に

        BGM_PATTERN:         (f"DUMMY{0x00}"),  # bgm
        BGM_LOOP_PATTERN:    (f"DUMMY{0x00}"),  # bgmループ(とりあえず単発で実装)
        BGM_FADEOUT_PATTERN: (f"DUMMY{0x00}"),  # bgm止める
        SE_PATTERN:          (f"DUMMY{0x00}"),  # 効果音
        SE_LOOP_PATTERN:     (f"DUMMY{0x00}"),  # 効果音ループ(単発 or BGM扱い 検討中)
        SE_STOP_PATTERN:     (f"DUMMY{0x00}"),  # 効果音停止
        STOP_ALL_PATTERN:    (f"DUMMY{0x00}"),  # 音声全停止

        BG_PATTERN:          (f"DUMMY{0x00}"),  # 背景

        CLICK_PATTERN:       (f"DUMMY{0x00}"),  # クリックして次へ(空文章用意で実装)
        WAIT_PATTERN:        (f"DUMMY{0x00}"),  # ウェイト
        WAIT_SHORT_PATTERN:  (f"DUMMY{0x00}"),  # ウェイト

        PAGE_TEXT_PATTERN:   (f"DUMMY{0x00}"),  # 改ページ文章
        LINE_TEXT_PATTERN:   (f"DUMMY{0x00}"),  # 改行文章
        TEXT_PATTERN:        (f"DUMMY{0x00}"),  # 普通の文章

        # 面倒なので場所ごとに個別で潰す可能性の高い命令
        TEXT_SPEED_RESET:    (f"DUMMY{0x00}"),  # 文字表示速度変更
        TEXT_SPEED_SET:      (f"DUMMY{0x00}"),  # 文字表示速度設定
        ERASE_TEXTWINDOW:    (f"DUMMY{0x00}"),  # 文字表示window削除
        SET_WINDOW:          (f"DUMMY{0x00}"),  # 文字表示位置設定

        MOV_STR_PATTERN:     (f"DUMMY{0x00}"),  # 文字変数代入(主に章のタイトルに利用)
        MOV_NUM_PATTERN:     (f"DUMMY{0x00}"),  # 数字変数代入(詳細不明)

        LABEL_PATTERN:       (f"DUMMY{0x00}"),  # jump用ラベル
    }


    # 一行ごと読み込み
    for line in txt_lines:

        # 行頭/行末空白削除
        line = line.strip()

        # 行がある(=空白ではない)場合
        if line:

            ismatch = False

            # 正規表現検索
            for ptkey, ptval in PATTERNS.items():

                # キーのパターンと一致
                if (matched_data := re.match(ptkey, line)):
                    ismatch = True

                    # if (ptkey in [PAGE_TEXT_PATTERN, LINE_TEXT_PATTERN, TEXT_PATTERN]):
                    #     print(line)

                    if (ptkey in [BGM_PATTERN, BGM_LOOP_PATTERN]):
                        # print(matched_data.group('arg1'))
                        pass

                    if (ptkey in [SE_PATTERN, SE_LOOP_PATTERN]):
                        # print(matched_data.group('arg2'))
                        pass

                    if (ptkey in [BG_PATTERN]):
                        print(matched_data.group('arg1'))
                        pass

                    break

            if (ismatch == False):
                print(f'no_match: {line}')


def main():

    input_path = Path('D:/132_shuumatsu_gba/0.txt')

    with open(input_path, 'r', encoding='cp932') as file:
        lines = file.readlines()

    # 改行文字を削除
    lines = [line.strip() for line in lines]

    # 結果を表示
    convert_txt_to_gbabin(lines[10126:10598])
    convert_txt_to_gbabin(lines[10622:11709])
    convert_txt_to_gbabin(lines[11717:13244])
    convert_txt_to_gbabin(lines[13247:14528])
    convert_txt_to_gbabin(lines[14531:15539])
    convert_txt_to_gbabin(lines[15543:16884])
    convert_txt_to_gbabin(lines[16889:17897])
    convert_txt_to_gbabin(lines[17899:19128])
    convert_txt_to_gbabin(lines[19131:19758])

    pass




main()