from pathlib import Path
from config_manager import config
from logging_handler import export_logger


def write_csv(data):
    try:
        Path(config.get("CSV.file_path")).parents[0].mkdir(parents=True, exist_ok=True)

        with open(config.get("CSV.file_path"), mode="w+", encoding="UTF-8") as file:
            export_logger.debug(f"Opened csv file {config.get('CSV.file_path')}")

            delimiter = config.get("CSV.delimiter")
            headers = delimiter.join(data.keys())
            values = delimiter.join(map(str, data.values()))
            export_logger.debug(f"Generated headers and values")

            file.write(headers + "\n")
            file.write(values)
            export_logger.info(f"Saved CSV to {config.get('CSV.file_path')}")
        export_logger.info("Closed csv file")
    except Exception as e:
        export_logger.error(e)
