#!/usr/bin/env python3
from pathlib import Path
import math
import re

from core.config import AppConfig
from .paths import IMG_LIST, BGM_LIST, SE_LIST, VOICE_LIST


def decrypt_0x84(data: bytes) -> bytes:
    """0x84 複合化"""
    bin_list = []  # 復号したバイナリを格納する配列の作成

    for b in range(len(data)):  # 復号 0x84でbitxor
        bin_list.append(bytes.fromhex(
            str((hex(int(data[b]) ^ int(0x84))[2:].zfill(2)))))

    decode_text = (b''.join(bin_list)).decode('cp932', errors='ignore')
    return decode_text


def extract_concept(text):
    # 文字列を抽出する正規表現 - "（"以降は除外
    match = re.search(r'(csel )?"　■　(.+?)(（.+)?",\*ns[0-9]{2},', text)
    if match:
        return match.group(2)
    return None


def convert_txt_main(txt_lines: list[str], is_product: bool = False) -> list[str]:

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

    # 仮
    command_cnt = '0014'

    line_command_list = []

    # 一行ごと読み込み
    for line in txt_lines:

        # 行頭/行末空白削除
        line = line.strip()

        # Productシナリオの場合の正規表現を使った個別修正
        if is_product:

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
                                line_command = ['!b', str(iml[0]), str(command_cnt)]
                                break

                    # 効果音・ボイス
                    elif (ptkey in [SE_PATTERN, SE_LOOP_PATTERN]):
                        se_path = matched_data.group('arg2')

                        for iml in (SE_LIST + VOICE_LIST):
                            if (Path(iml[1]) == Path(se_path)):
                                line_command = ['!e', str(iml[0]), str(command_cnt)]
                                break

                    # 音消す(SEループ削除は後で実装)
                    elif (ptkey in [BGM_FADEOUT_PATTERN, STOP_ALL_PATTERN]):
                        # DEBUG_LIST.append(matched_data.group('arg2'))
                        line_command = ['!b', str(1), str(command_cnt)]
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

                        for iml in IMG_LIST:
                            if (Path(iml[1]) == Path(bg_path)):
                                iml_0 = iml[0]
                                if (iml_0 == 130):  # 130番は特殊扱い - 129と同じ画像なので129扱い
                                    iml_0 = 129
                                line_command  = ['!g', str(iml_0),    str(command_cnt)]
                                line_command += ['#t', str(wait_time), str(command_cnt)]

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
                                    line_command += ['_t', ls, str(command_cnt)]

                                # Productシナリオ時 - 改ページ扱いに変更
                                else:
                                    line_command += ['_r', ls, str(command_cnt)]
                            
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

                    elif (ptkey in [WAIT_PATTERN, WAIT_SHORT_PATTERN]):
                        wait_time_rawstr = matched_data.group('arg1')
                        wait_time_rawint = int(wait_time_rawstr)
                        wait_time = math.ceil(wait_time_rawint / 100)

                        if (wait_time < 1):
                            wait_time = 1

                        line_command = ['#t', str(wait_time), str(command_cnt)]

                    if line_command:
                        line_command_list.append(line_command)
                    break

            if (ismatch == False):
                print(f'no_match: {line}')

    
    # 2→1次元配列へ変換
    scn_list = [item for sublist in line_command_list for item in sublist]
    
    return scn_list


def convert_txt(lines: list[str], cfg: AppConfig) -> dict:
    """シナリオテキスト変換の全処理"""

    # 必要な初期データ準備
    scn_list = {
        '000': ['0', '0000', '!t', '起動', '0000', '#W', '200', '0000', '#t', '10', '0000', 
                '!g', '0', '0000', '#t', '6', '0000', '!g', '1', '0000', '#t', '6', '0000', '!j', '1', '0000', ';;', ''],
        '003': ['0', '0000', '#W',  '0', '0000', '#t',  '1', '0000', '#W', '1', '0000'],
        '006': ['0', '0000', '!t', 'プロダクト',   '0000', '#W', '0', '0000'],
    }

    # 本編シナリオ
    if (not cfg.include_voice):
        # ボイス無し版
        scn_list['003'] += convert_txt_main(lines[639:1101])
        scn_list['003'] += convert_txt_main(lines[1105:2184])
        scn_list['003'] += (['!g', '3', '0000', '#t', '120', '0000'])
        scn_list['003'] += convert_txt_main(lines[2188:3690])
        scn_list['003'] += (['!g', '4', '0000', '#t', '120', '0000'])
        scn_list['003'] += convert_txt_main(lines[3693:4945])
        scn_list['003'] += (['!g', '5', '0000', '#t', '120', '0000'])
        scn_list['003'] += convert_txt_main(lines[4948:5926])
        scn_list['003'] += (['!g', '6', '0000', '#t', '120', '0000'])
        scn_list['003'] += convert_txt_main(lines[5930:7258])
        scn_list['003'] += (['!g', '7', '0000', '#t', '120', '0000'])
        scn_list['003'] += convert_txt_main(lines[7263:8255])
        scn_list['003'] += (['!g', '8', '0000', '#t', '120', '0000'])
        scn_list['003'] += convert_txt_main(lines[8257:9471])
        scn_list['003'] += (['!g', '9', '0000', '#t', '120', '0000'])
        scn_list['003'] += convert_txt_main(lines[9474:10120])
    else:
        # ボイス有り版
        scn_list['003'] += (convert_txt_main(lines[10126:10598]))
        scn_list['003'] += (convert_txt_main(lines[10622:11709]))
        scn_list['003'] += (['!g', '3', '0000', '#t', '120', '0000'])
        scn_list['003'] += (convert_txt_main(lines[11717:13244]))
        scn_list['003'] += (['!g', '4', '0000', '#t', '120', '0000'])
        scn_list['003'] += (convert_txt_main(lines[13247:14528]))
        scn_list['003'] += (['!g', '5', '0000', '#t', '120', '0000'])
        scn_list['003'] += (convert_txt_main(lines[14531:15539]))
        scn_list['003'] += (['!g', '6', '0000', '#t', '120', '0000'])
        scn_list['003'] += (convert_txt_main(lines[15543:16884]))
        scn_list['003'] += (['!g', '7', '0000', '#t', '120', '0000'])
        scn_list['003'] += (convert_txt_main(lines[16889:17897]))
        scn_list['003'] += (['!g', '8', '0000', '#t', '120', '0000'])
        scn_list['003'] += (convert_txt_main(lines[17899:19128]))
        scn_list['003'] += (['!g', '9', '0000', '#t', '120', '0000'])
        scn_list['003'] += (convert_txt_main(lines[19131:19758]))

    # 本編シナリオ末尾追加
    scn_list['003'] += (['!g', '1', '0014', '#t', '1', '0014', '!j', '1', '0014', ';;', ''])

    # Ｐｒｏｄｕｃｔシナリオ
    scn_list['006'] += (convert_txt_main(lines[298:319], True))
    scn_list['006'] += (['!t', extract_concept(lines[321]), '0014'])
    scn_list['006'] += (convert_txt_main(lines[327:375], True))
    scn_list['006'] += (['!t', extract_concept(lines[322]), '0014'])
    scn_list['006'] += (convert_txt_main(lines[378:481], True))
    scn_list['006'] += (['!t', extract_concept(lines[323]), '0014'])
    scn_list['006'] += (convert_txt_main(lines[485:525], True))
    scn_list['006'] += (['!t', extract_concept(lines[324]), '0014'])
    scn_list['006'] += (convert_txt_main(lines[528:570], True))
    scn_list['006'] += (['!g', '1', '0014', '#t', '1', '0014', '!j', '1', '0014', ';;', ''])

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
        if (cfg.debug_mode):
            output_txt_path = cfg.debug_dir / f'SCN{scn_key}.txt'
            debug_txt = "\n".join(scn_val)
            
            with open(output_txt_path, "w", encoding="cp932") as f:
                f.write(debug_txt)
    
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
    
    # savid作成
    create_savid(cfg)
        
    return