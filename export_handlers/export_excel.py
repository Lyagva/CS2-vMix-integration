import openpyxl
from config_manager import config
from logging_handler import export_logger


def write_excel(data):
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Data"
        export_logger.debug("Opened empty Excel Workbook")

        ws.append(list(data.keys()))
        ws.append(list(data.values()))
        export_logger.debug("Written Excel Workbook")

        save_path = config.get("EXCEL.file_path")
        wb.save(save_path)
        export_logger.info(f"Saved Excel Workbook to {save_path}")
    except Exception as e:
        export_logger.error(e)
