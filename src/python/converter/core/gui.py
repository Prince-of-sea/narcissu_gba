#!/usr/bin/env python3
import dearpygui.dearpygui as dpg
import webbrowser
import sys

from core.config import AppConfig
from core.converter import convert_main
from core.gui_utils import message_box


def close():
    dpg.stop_dearpygui()


def open_repositorieslink(cfg: AppConfig):
    webbrowser.open(cfg.repo_url, new=1, autoraise=True)
    return


def copyrights(cfg: AppConfig):

    message_box('copyrights',
                f'{cfg.app_name} ver.{cfg.app_version}\n(C) 2025-2026 Prince-of-sea / PC-CNT')

    return


def licenses(cfg: AppConfig):
    webbrowser.open(cfg.license_txt_path, new=1, autoraise=True)
    return


def convert_button_callback(cfg: AppConfig):
    cfg.out_temp_file_checkbox = bool(dpg.get_value("out_temp_file_checkbox"))
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
        height=280,
        small_icon=f"{cfg.icon_path}",
        large_icon=f"{cfg.icon_path}",
        resizable=False,
    )

    with dpg.window(tag="Main Window", no_resize=True):
        with dpg.menu_bar():
            with dpg.menu(label="設定"):
                dpg.add_menu_item(label="終了", callback=close)

            with dpg.menu(label="このソフトについて"):
                dpg.add_menu_item(
                    label="サイトを開く",
                    callback=lambda: open_repositorieslink(cfg),
                    )
                dpg.add_menu_item(
                    label="権利者表記",
                    callback=lambda: copyrights(cfg),
                )
                dpg.add_menu_item(
                    label="ライセンス",
                    callback=lambda: licenses(cfg),
                )

        with dpg.child_window(
            height=176,
            border=True,
        ):
            with dpg.tree_node(label="基本設定", default_open=True):
                with dpg.group(horizontal=False):
                    dpg.add_text(
                        "変換モードの指定：",
                        tag="convert_mode_text",
                    )
                    with dpg.tooltip(parent="convert_mode_text"):
                        dpg.add_text("変換モードを指定できます\nボイスがない方が高音質です")

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

            with dpg.tree_node(label="詳細設定", default_open=False):
                with dpg.table(header_row=False, borders_innerH=False, borders_innerV=False):
                    dpg.add_table_column(no_resize=True, width_fixed=True)
                    dpg.add_table_column(no_resize=True, width_fixed=True)

                    with dpg.table_row():
                        dpg.add_checkbox(
                            label="変換途中のファイルを出力する",
                            tag="out_temp_file_checkbox",
                            default_value=False,
                        )
                        with dpg.tooltip(parent="out_temp_file_checkbox"):
                            dpg.add_text("GBA向け圧縮データを、\nROMとは別に出力します")

                    with dpg.table_row():
                        dpg.add_checkbox(
                            label="Chapter1のサブタイトルを表示",
                            tag="ch1_subtitle_checkbox",
                            default_value=False,
                        )
                        with dpg.tooltip(parent="ch1_subtitle_checkbox"):
                            dpg.add_text("Chapter1開始時にサブタイトルが\n挟まれるようになります\n(原作には存在しない表示です)")

        with dpg.group(horizontal=True):
            dpg.add_progress_bar(
                tag="progress_bar",
                default_value=0,
                overlay="0%",
                width=380,
            )
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
