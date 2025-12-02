#!/usr/bin/env python3
from pathlib import Path
import tkinter
from tkinter import filedialog

def gui_main() -> dict:
    '''gui本処理'''

    ### 言うまでもなく仮 後で全部書き直す ###
    print(' +++ narcissu_gba alpha版 +++ ')

    gui_cfg = {
        'input_dir': None,
        'output_dir': None,
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

    return gui_cfg