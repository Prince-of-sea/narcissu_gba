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
    cnvmodegui = messagebox.askokcancel("確認", "モード？\nok:ボイス有り低音質\nキャンセル:ボイス無し高音質")
    gui_cfg['conv_mode'] = 1 if cnvmodegui else 2
    root.destroy()

    return gui_cfg