#!/usr/bin/env python3
import dearpygui.dearpygui as dpg
import time
import datetime


def dpg_all_enable_item(is_enable_item: bool) -> None:
    """全要素入力可能or不可能に"""
    for i in dpg.get_aliases():
        try:
            if (is_enable_item):
                dpg.enable_item(i)
            else:
                dpg.disable_item(i)
        except:
            pass
    return


def message_box(msg_title: str, msg: str) -> None:
    """window表示"""

    with dpg.mutex():
        with dpg.window(label=f'{msg_title}', modal=True) as msg_window:
            dpg.add_text(f'{msg}')
            dpg.add_button(label='OK', callback=lambda: dpg.configure_item(
                    msg_window, show=False))
            
    dpg.split_frame()
    dpg.set_item_pos(msg_window,
                    [dpg.get_viewport_client_width() // 2 - dpg.get_item_width(msg_window) // 2,
                     dpg.get_viewport_client_height() // 2 - dpg.get_item_height(msg_window) // 2])
    
    return


def configure_progress_bar(value: float, is_smooth: bool = False) -> None:
    """プログレスバーの設定を行う"""

    # 滑らかに移動する場合
    if (is_smooth):

        # 現在の進捗率から0.5秒掛けて目標値までスムーズに移動
        now_value = dpg.get_value("progress_bar") * 100
        datetime_start = datetime.datetime.now()
        datetime_end = datetime_start + datetime.timedelta(seconds=0.5)

        while True:
            datetime_now = datetime.datetime.now()
            if (datetime_now > datetime_end):
                break
            elapsed = (datetime_now - datetime_start).total_seconds()
            progress = now_value + (value - now_value) * (elapsed / 0.5)
            dpg.set_value("progress_bar", progress / 100)
            dpg.configure_item("progress_bar", overlay=f"{int(progress)}%")
            time.sleep(0.01)
    
    # 最終的に目標値に設定
    dpg.set_value("progress_bar", value / 100)
    dpg.configure_item("progress_bar", overlay=f"{int(value)}%")

    return
