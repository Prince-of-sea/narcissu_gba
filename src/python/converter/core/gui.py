#!/usr/bin/env python3
from operator import call
import sys
import webbrowser

import dearpygui.dearpygui as dpg

from core.config import AppConfig
from core.converter import convert_main


gui_cfg = {"conv_mode": 1}


def close():
    dpg.stop_dearpygui()
    sys.exit(0)


def open_repositorieslink():
    url = "https://github.com/Prince-of-sea/narcissu_gba/"
    webbrowser.open(url, new=1, autoraise=True)
    return


def copyrights():
    return


def licenses():
    return


def conv_mode_radio_callback(sender, app_data, cfg: AppConfig):
    t = {
        cfg.sound_quality_high_message: 1,
        cfg.sound_quality_low_message: 2,
    }
    gui_cfg["conv_mode"] = t[app_data]
    print(gui_cfg)
    return


def convert_button_callback(cfg: AppConfig, gui_cfg: dict):
    convert_main(cfg, gui_cfg)
    return


def gui_main(cfg: AppConfig) -> None:
    """gui本処理"""

    ### 言うまでもなく仮 後で全部書き直す ###
    print(f" +++ {cfg.app_name} Ver.{cfg.app_version} +++ ")

    # root = tkinter.Tk()
    # cnvmodegui = messagebox.askokcancel(
    #     "確認", "モード？\nok:ボイス有り低音質\nキャンセル:ボイス無し高音質"
    # )
    # gui_cfg["conv_mode"] = 1 if cnvmodegui else 2
    # root.destroy()

    dpg.create_context()

    dpg.set_exit_callback(close)

    with dpg.font_registry():
        with dpg.font(file=r"C:\Windows\Fonts\meiryo.ttc", size=16) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
        dpg.bind_font(default_font)

    dpg.create_viewport(
        title=f"{cfg.app_name} ver.{cfg.app_version}",
        width=480,
        height=300,
        resizable=False,
    )

    with dpg.window(tag="Main Window", no_resize=True):
        with dpg.menu_bar():
            with dpg.menu(label="設定"):
                dpg.add_menu_item(label="終了", callback=close)

            with dpg.menu(label="このソフトについて"):
                dpg.add_menu_item(label="サイトを開く", callback=open_repositorieslink)
                dpg.add_menu_item(
                    label="権利者表記",
                    callback=copyrights,
                )
                dpg.add_menu_item(
                    label="ライセンス",
                    callback=licenses,
                )

        with dpg.child_window(
            height=180,
            border=True,
        ):
            with dpg.tree_node(label="基本設定", default_open=True):
                with dpg.group(horizontal=False):
                    dpg.add_text("変換モードの指定：")
                    dpg.add_radio_button(
                        items=(
                            f"{cfg.sound_quality_high_message}",
                            f"{cfg.sound_quality_low_message}",
                        ),
                        horizontal=False,
                        tag="conv_mode_radio",
                        callback=conv_mode_radio_callback,
                        user_data=cfg,
                    )

            with dpg.tree_node(label="詳細設定", default_open=True):
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(
                        label="変換途中のファイルを出力する（デバッグ）",
                        tag="debug_checkbox",
                        default_value=False,
                    )

        with dpg.group(horizontal=True):
            dpg.add_progress_bar(default_value=0, tag="progress_bar", overlay="0%")
            dpg.add_button(
                label="Convert",
                tag="convert_button",
                callback=lambda: convert_button_callback(cfg, gui_cfg),
            )

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Main Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

    ### 変換メイン処理呼び出し ### - 正式にはGUIから呼ばれる
    # convert_main(cfg, gui_cfg)

    return
