#!/usr/bin/env python3
import tempfile

from core.resource_extractor import extract_resources
from core.file_checker import check_files
from core.scenario_converter import convert_scenario
from core.image_converter import convert_images
from core.audio_converter import convert_audio
from core.packer import pack_resources
from core.config import create_config
from core.gui import gui_main
from utils.log import log_info


def main():
    log_info("Start conversion tool")

    # メイン
    with tempfile.TemporaryDirectory() as temp_dir:

        gui_cfg = gui_main()

        cfg = create_config(temp_dir, gui_cfg)

        if check_files(cfg):
            extract_resources(cfg)
            convert_scenario(cfg)
            convert_images(cfg)
            convert_audio(cfg)
            pack_resources(cfg)

    log_info("All done!")


if __name__ == "__main__":
    main()