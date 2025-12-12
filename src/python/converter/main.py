from core.resource_extractor import extract_resources
from core.file_checker import check_files
from core.scenario_converter import convert_scenario
from core.image_converter import convert_images
from core.audio_converter import convert_audio
from core.packer import pack_resources

from utils.log import log_info


def main():
    log_info("Start conversion tool")

    # 例）順番だけ書いておく
    extract_resources()
    check_files()
    convert_scenario(debug=False)
    convert_images()
    convert_audio()
    pack_resources()

    log_info("All done!")


if __name__ == "__main__":
    main()
