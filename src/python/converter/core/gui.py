#!/usr/bin/env python3
import dearpygui.dearpygui as dpg
import webbrowser
import sys

from core.config import AppConfig
from core.converter import convert_main


def close():
    dpg.stop_dearpygui()
    sys.exit(0)


def open_repositorieslink():
    url = "https://github.com/Prince-of-sea/narcissu_gba/"
    webbrowser.open(url, new=1, autoraise=True)
    return


def copyrights(cfg: AppConfig):

    with dpg.mutex():
        with dpg.window(label='copyrights', modal=True) as msg_window:
            dpg.add_text(f'{cfg.app_name} ver.{cfg.app_version}\n(C) 2025-2026 Prince-of-sea / PC-CNT')
            dpg.add_button(label='OK', callback=lambda: dpg.configure_item(
                    msg_window, show=False))
            
    dpg.split_frame()
    dpg.set_item_pos(msg_window,
                    [dpg.get_viewport_client_width() // 2 - dpg.get_item_width(msg_window) // 2,
                     dpg.get_viewport_client_height() // 2 - dpg.get_item_height(msg_window) // 2])
    return


def licenses(cfg: AppConfig):
    webbrowser.open(cfg.license_txt_path, new=1, autoraise=True)
    return


def convert_button_callback(cfg: AppConfig):
    cfg.debug_mode = bool(dpg.get_value("debug_checkbox"))
    convert_main(cfg)
    return


def gui_main(cfg: AppConfig) -> None:
    """gui本処理"""

    dpg.create_context()
    dpg.set_exit_callback(close)

    with dpg.font_registry():
        with dpg.font(file=cfg.font_path, size=16) as default_font:
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
                    callback=lambda: copyrights(cfg),
                )
                dpg.add_menu_item(
                    label="ライセンス",
                    callback=lambda: licenses(cfg),
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
                            f"{cfg.sound_quality_low_message}",
                            f"{cfg.sound_quality_high_message}",
                        ),
                        horizontal=False,
                        tag="conv_mode_radio",
                        default_value=f"{cfg.sound_quality_low_message}",
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
                callback=lambda: convert_button_callback(cfg),
            )

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Main Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

    return
