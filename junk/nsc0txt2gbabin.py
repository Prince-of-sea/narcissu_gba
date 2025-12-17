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

    # 正規表現そのものをキーにした辞書
    # キー：正規表現（名前付きグループ）
    # 値　：GBA側にシナリオとして読み込ませるためのバイナリそのもの
    PATTERNS = {
        # 上から順で読み取らせるので基準が緩いものほど下に
        r'^dwave\s+(?P<arg1>\d+),\s*"(?P<arg2>.*)"':     (f"DUMMY{0x00}"), # 効果音
        r'^dwaveloop\s+(?P<arg1>\d+),\s*"(?P<arg2>.*)"': (f"DUMMY{0x00}"), # 効果音ループ(単発 or BGM扱い 検討中)
        r'^dwavestop\s+(?P<arg1>\d+)':                   (f"DUMMY{0x00}"), # 効果音停止
        r'^mp3\s+"(?P<arg1>.*)"':                    (f"DUMMY{0x00}"), # bgm
        r'^mp3loop\s+"(?P<arg1>.*)"':                (f"DUMMY{0x00}"), # bgmループ(とりあえず単発で実装)
        r'^mp3fadeout\s+(?P<arg1>\d+)':              (f"DUMMY{0x00}"), # bgm止める
        r'^stop$':                                   (f"DUMMY{0x00}"), # 音声全停止

        r'^bg\s+"(?P<arg1>.*)",\s*(?P<arg2>\d+)':    (f"DUMMY{0x00}"), #背景
        
        r'^click$':                                  (f"DUMMY{0x00}"), # クリックして次へ(空文章用意で実装)
        r'^wait\s+(?P<arg1>\d+)':                    (f"DUMMY{0x00}"), # ウェイト
        r'^!w(?P<arg1>\d+)':                         (f"DUMMY{0x00}"), # ウェイト
        
        r'^([^\x01-\x7E]|@)+\x5c':                     (f"DUMMY{0x00}"), # 改ページ文章
        r'^([^\x01-\x7E]|@)+@':                        (f"DUMMY{0x00}"), # 改行文章
        r'^([^\x01-\x7E]|@)+':                         (f"DUMMY{0x00}"), # 普通の文章

        # 面倒なので場所ごとに個別で潰す可能性の高い命令
        r'^!sd$':                                    (f"DUMMY{0x00}"), # 文字表示速度変更
        r'^!s(?P<arg1>\d+)':                         (f"DUMMY{0x00}"), # 文字表示速度設定
        r'^erasetextwindow\s+':                      (f"DUMMY{0x00}"), # 文字表示window削除
        r'^setwindow\s+':                            (f"DUMMY{0x00}"), # 文字表示位置設定
        r'^mov\s+\$(?P<arg1>.*),\s*"(?P<arg2>.*)"':  (f"DUMMY{0x00}"), # 文字変数代入(主に章のタイトルに利用)
        r'^mov\s+\%(?P<arg1>.*),\s*(?P<arg2>\d+)':   (f"DUMMY{0x00}"), # 数字変数代入(詳細不明)
        r'^\*(?P<arg1>.*)':                          (f"DUMMY{0x00}"), # jump用ラベル
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


                    # print(matched_data)

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