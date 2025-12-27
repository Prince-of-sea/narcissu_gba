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
開始地点は*表記から
終了はgoto行

'''
IMG_LIST = [
	[ 10,'e/amazora02.jpg'],
	[ 11,'e/amazora03.jpg'],
	[ 12,'e/b.jpg'],
	[ 13,'e/byoin7_rouka.jpg'],
	[ 14,'e/byoin_chusyajo.jpg'],
	[ 15,'e/byoin_heya_yu2.jpg'],
	[ 16,'e/byoin_rouka.jpg'],
	[ 17,'e/c00.jpg'],
	[ 18,'e/c001.jpg'],
	[ 19,'e/c001a.jpg'],
	[ 20,'e/c001b.jpg'],
	[ 21,'e/c002.jpg'],
	[ 22,'e/c003.jpg'],
	[ 23,'e/c004.jpg'],
	[ 24,'e/c005.jpg'],
	[ 25,'e/c0052.jpg'],
	[ 26,'e/c02.jpg'],
	[ 27,'e/c03.jpg'],
	[ 28,'e/c032.jpg'],
	[ 29,'e/c033.jpg'],
	[ 30,'e/c04.jpg'],
	[ 31,'e/c042.jpg'],
	[ 32,'e/car_byoin_chusyajo.jpg'],
	[ 33,'e/car_byoin_chusyajo_yoru.jpg'],
	[ 34,'e/car_byoin_chusyajo_yoru_ame.jpg'],
	[ 35,'e/car_michi01.jpg'],
	[ 36,'e/car_naname_michi01.jpg'],
	[ 37,'e/carkey.jpg'],
	[ 38,'e/chara_001.jpg'],
	[ 39,'e/chara_0012.jpg'],
	[ 40,'e/chara_0013.jpg'],
	[ 41,'e/chara_0013b.jpg'],
	[ 42,'e/chara_k01.jpg'],
	[ 43,'e/chara_k02.jpg'],
	[ 44,'e/chusha_hamabe_yu.jpg'],
	[ 45,'e/chusha_michi2_yoru.jpg'],
	[ 46,'e/chusha_michi2_yu.jpg'],
	[ 47,'e/chusha_michi_ame_yoru.jpg'],
	[ 48,'e/coin_tennai.jpg'],
	[ 49,'e/danwa.jpg'],
	[ 50,'e/danwa_ame.jpg'],
	[ 51,'e/danwa_yoru.jpg'],
	[ 52,'e/gs.jpg'],
	[ 53,'e/hashigeta.jpg'],
	[ 54,'e/hiki_kosoku2.jpg'],
	[ 55,'e/hiki_shigai_yu.jpg'],
	[ 56,'e/image01.jpg'],
	[ 57,'e/imege03.jpg'],
	[ 58,'e/imege04.jpg'],
	[ 59,'e/imege05.jpg'],
	[ 60,'e/imege06.jpg'],
	[ 61,'e/imege07.jpg'],
	[ 62,'e/imege072.jpg'],
	[ 63,'e/imege09.jpg'],
	[ 64,'e/imege92.jpg'],
	[ 65,'e/imege93.jpg'],
	[ 66,'e/imege94.jpg'],
	[ 67,'e/imege95.jpg'],
	[ 68,'e/imege96.jpg'],
	[ 69,'e/imege97.jpg'],
	[ 70,'e/joku_kosoku.jpg'],
	[ 71,'e/joku_kosoku_yu.jpg'],
	[ 72,'e/joku_shigaichi.jpg'],
	[ 73,'e/naname_inaka_ame2.jpg'],
	[ 74,'e/naname_inaka_yoru.jpg'],
	[ 75,'e/naname_inaka_yu.jpg'],
	[ 76,'e/naname_machi.jpg'],
	[ 77,'e/naname_machi2.jpg'],
	[ 78,'e/naname_machi2_yoru.jpg'],
	[ 79,'e/naname_michi.jpg'],
	[ 80,'e/naname_michi_yoru.jpg'],
	[ 81,'e/naname_yuki.jpg'],
	[ 82,'e/nar01.jpg'],
	[ 83,'e/nar01c.jpg'],
	[ 84,'e/nar01d.jpg'],
	[ 85,'e/narcissu_b.jpg'],
	[ 86,'e/narcissu_yoru_ame.jpg'],
	[ 87,'e/pachi.jpg'],
	[ 88,'e/setsumi_kaisou.jpg'],
	[ 89,'e/shanai_inaka.jpg'],
	[ 90,'e/shanai_michi01.jpg'],
	[ 91,'e/shanai_michi01_yoru.jpg'],
	[ 92,'e/shanai_michi01_yu.jpg'],
	[ 93,'e/shanai_michi01b.jpg'],
	[ 94,'e/shanai_michi02_yoru.jpg'],
	[ 95,'e/shanai_michi03_yu.jpg'],
	[ 96,'e/shanai_michi04.jpg'],
	[ 97,'e/sora01.jpg'],
	[ 98,'e/sora02.jpg'],
	[ 99,'e/sora03.jpg'],
	[100,'e/sora06.jpg'],
	[101,'e/sora07.jpg'],
	[102,'e/sora_ame01.jpg'],
	[103,'e/sora_ame01b.jpg'],
	[104,'e/sora_ame02.jpg'],
	[105,'e/sora_ame03.jpg'],
	[106,'e/sora_yoru01.jpg'],
	[107,'e/sora_yu.jpg'],
	[108,'e/soukou.jpg'],
	[109,'e/soukou_machi.jpg'],
	[110,'e/soukou_machi_yoru.jpg'],
	[111,'e/soukou_machi_yu.jpg'],
	[112,'e/soukou_yoru.jpg'],
	[113,'e/st00.jpg'],
	[114,'e/st01.jpg'],
	[115,'e/st02.jpg'],
	[116,'e/st03.jpg'],
	[117,'e/st04.jpg'],
	[118,'e/st05.jpg'],
	[119,'e/tv_hana.jpg'],
	[120,'e/umibe_yoru.jpg'],
	[121,'e/w.jpg'],
	[122,'e/yakkyoku.jpg'],
	[123,'e/yuki_kohan.jpg'],
	[124,'e/yukizora.jpg'],
	[125,'tui2/c0432.bmp'],
	[126,'tui2/c044.bmp'],
	[127,'tui2/c0442.bmp'],
	[128,'tui2/c045.bmp'],
	[129,'tui2/c046.bmp'],
	[130,'tui2/c047.bmp'],
	[131,'tui2/c049.bmp'],
	[132,'tui2/cat02.bmp'],
	[133,'tui2/cat03.bmp'],
	[134,'tui2/cat05.bmp'],
	[135,'tui2/cat06.bmp'],
	[136,'tui2/cat07.bmp'],
	[137,'tui2/cat072.bmp'],
	[138,'tui2/cat073.bmp'],
	[139,'tui/imege98.bmp'],
	[140,'tui/naname_inaka_yoru2.bmp'],
	[141,'yobi/car_byoin_chusyajo_yu.bmp'],
	[142,'yobi/cat03.bmp'],
	[143,'yobi/cat09.bmp'],
]


DEBUG_LIST = []

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

        TEXTCLEAR_PATTERN:   (f"DUMMY{0x00}"),  # テキストクリア(ボイス無しでのみ使用？)
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
                        # DEBUG_LIST.append(matched_data.group('arg1'))
                        pass

                    # 効果音・ボイス
                    elif (ptkey in [SE_PATTERN, SE_LOOP_PATTERN]):
                        # DEBUG_LIST.append(matched_data.group('arg2'))
                        pass

                    # 背景
                    elif (ptkey in [BG_PATTERN]):
                        for iml in IMG_LIST:
                            if (Path(iml[1]) == Path(matched_data.group('arg1'))):
                                line_command = ['!g', str(iml[0]), str(command_cnt)]
                                break


                    # テキスト
                    elif (ptkey in [PAGE_TEXT_PATTERN, LINE_TEXT_PATTERN, TEXT_PATTERN]):

                        line = line.replace(r'@', '').replace('\\', '')

                        if (ptkey == PAGE_TEXT_PATTERN):# 改ページ文章
                            line_command = ['_r', line, str(command_cnt)]

                        elif (ptkey == LINE_TEXT_PATTERN):# 改行文章
                            line_command = ['_t', line, str(command_cnt)]

                        elif (ptkey == TEXT_PATTERN):# 普通の文章
                            # todo?:行頭を原作に揃える場合は全角スペースで埋めて文字数を17の倍数にする
                            line_command = ['_m', line, str(command_cnt)]




                    if line_command:
                        line_command_list.append(line_command)
                    break

            if (ismatch == False):
                print(f'no_match: {line}')
    
    # 2→1次元配列へ変換してから0x00で結合してバイナリへ
    line_command_bin = b"\x00".join(
        s.encode("cp932")
        for row in line_command_list
        for s in row
    )
    
    return bytes(line_command_bin)



def main():

    input_path = Path('D:/132_shuumatsu_gba/0.txt')

    scn_bin_list = []

    with open(input_path, 'r', encoding='cp932') as file:
        lines = file.readlines()

    # 改行文字を削除
    lines = [line.strip() for line in lines]

    # 結果を表示
    # convert_txt_to_gbabin(lines[639:1101])# *image	"プロローグ"
    # convert_txt_to_gbabin(lines[1105:2184])# *honpen2	"７階"
    # convert_txt_to_gbabin(lines[2188:3690])# *honpen3	"銀のクーペ"
    # convert_txt_to_gbabin(lines[3693:4945])# *honpen4	"地図"
    # convert_txt_to_gbabin(lines[4948:5926])# *honpen5	"エメラルドの海"
    # convert_txt_to_gbabin(lines[5930:7258])# *honpen6	"一号線"
    # convert_txt_to_gbabin(lines[7263:8255])# *honpen7	"エコー"
    # convert_txt_to_gbabin(lines[8257:9471])# *honpen8	"ナルキッソス"
    # convert_txt_to_gbabin(lines[9474:10120])# *honpen9	"白石工務店"

    scn_bin_list.append(convert_txt_to_gbabin(lines[10126:10598]))# *image_voice	"プロローグ　ボイスＶｅｒ  "		10126	10598
    scn_bin_list.append(convert_txt_to_gbabin(lines[10622:11709]))# *honpen2_voice	"７階　ボイスＶｅｒ"			10622	11709
    scn_bin_list.append(convert_txt_to_gbabin(lines[11717:13244]))# *honpen3_voice	"銀のクーペ　ボイスＶｅｒ"		11717	13244
    scn_bin_list.append(convert_txt_to_gbabin(lines[13247:14528]))# *honpen4_voice	"地図　ボイスＶｅｒ"			13247	14528
    scn_bin_list.append(convert_txt_to_gbabin(lines[14531:15539]))# *honpen5_voice	"エメラルドの海　ボイスＶｅｒ"	14531	15539
    scn_bin_list.append(convert_txt_to_gbabin(lines[15543:16884]))# *honpen6_voice	"一号線　ボイスＶｅｒ"			15543	16884
    scn_bin_list.append(convert_txt_to_gbabin(lines[16889:17897]))# *honpen7_voice	"エコー　ボイスＶｅｒ"			16889	17897
    scn_bin_list.append(convert_txt_to_gbabin(lines[17899:19128]))# *honpen8_voice	"ナルキッソス　ボイスＶｅｒ"	17899	19128
    scn_bin_list.append(convert_txt_to_gbabin(lines[19131:19758]))# *honpen9_voice	"白石工務店　ボイスＶｅｒ"		19131	19758

    if DEBUG_LIST:
        for p in set(DEBUG_LIST): print(p)
    with open("output.bin", "wb") as f: f.write(b"\x00".join(scn_bin_list))
    pass


main()