#!/usr/bin/env python3
import tkinter
from tkinter import messagebox

def gui_main() -> dict:
    '''gui本処理'''

    ### 言うまでもなく仮 後で全部書き直す ###
    print(' +++ narcissu_gba beta版 +++ ')

    gui_cfg = {
        'conv_mode': None,
    }

    root = tkinter.Tk()
    cnvmodegui = messagebox.askokcancel("確認", "モード？\nok:ボイス有り低音質\nキャンセル:ボイス無し高音質")
    gui_cfg['conv_mode'] = 1 if cnvmodegui else 2
    root.destroy()

    return gui_cfg