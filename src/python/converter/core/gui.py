#!/usr/bin/env python3
from pathlib import Path
import tkinter
from tkinter import filedialog, messagebox

def gui_main() -> dict:
    '''gui本処理'''

    ### 言うまでもなく仮 後で全部書き直す ###
    print(' +++ narcissu_gba beta版 +++ ')

    gui_cfg = {
        'input_dir': None,
        'output_dir': None,
        'include_voice': False,
        'sound_quality': 0,
    }

    while (not gui_cfg['input_dir']):
        print('入力ディレクトリを指定してください:')
        root = tkinter.Tk()
        root.withdraw()
        gui_cfg['input_dir'] = Path(filedialog.askdirectory())
        print(gui_cfg['input_dir'])
        root.destroy()
    
    while (not gui_cfg['output_dir']):
        print('出力ディレクトリを指定してください:')
        root = tkinter.Tk()
        root.withdraw()
        gui_cfg['output_dir'] = Path(filedialog.askdirectory())
        print(gui_cfg['output_dir'])
        root.destroy()
    
    root = tkinter.Tk()
    gui_cfg['include_voice'] = messagebox.askokcancel("確認", "ボイス入れる？")
    root.destroy()

    root = tkinter.Tk()
    sndhigh = messagebox.askokcancel("確認", "音質上げる?\nok:9118 キャンセル:6241")
    gui_cfg['sound_quality'] = 9118 if sndhigh else 6241
    root.destroy()

    # 高音質でボイス有りは容量的に厳しいので警告
    if (gui_cfg['include_voice']) and (gui_cfg['sound_quality'] >= 9118):
        root = tkinter.Tk()
        messagebox.showinfo("だめだね", "ボイスを入れる場合、音質は9118にはできません(容量的に厳しいので)\nとりあえず今は6241扱いで通します\n\n※正式版ではOK押せないようにしてね")
        root.destroy()
        gui_cfg['sound_quality'] = 6241

    return gui_cfg