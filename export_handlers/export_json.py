import json
from config_manager import config
from logging_handler import export_logger


def write_json(data):
    try:
        with open(config.get("JSON.file_path"), mode="w+", encoding="UTF-8") as file:
            export_logger.debug(f"Opened json file {config.get('JSON.file_path')}")
            json.dump(data, file, indent=config.get("JSON.indent"), ensure_ascii=False)
            export_logger.info(f"Saved json to {config.get('JSON.file_path')}")
        export_logger.debug(f"Closed json file {config.get('JSON.file_path')}")
    except Exception as e:
        export_logger.error(e)