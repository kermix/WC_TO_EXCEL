import logging

import os
import sys

import openpyxl as xl
from openpyxl import Workbook


def __setup_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('log.txt', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

logger = __setup_logger(__name__)


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def to_comma_separated_string(value):
    if isinstance(value, (list, tuple, set)):
        return ','.join(str(x) for x in value)
    return str(value)


def merge_db(db_filename):
    db_wb = Workbook()

    for file in os.listdir():
        if file.endswith(".xlsx"):
            wb = xl.load_workbook(file)
            for ws in wb.worksheets:
                db_ws = db_wb.create_sheet(ws.title)

                max_row, max_col = ws.max_row, ws.max_column

                for i in range(1, max_row + 1):
                    for j in range(1, max_col + 1):
                        cell = ws.cell(row=i, column=j)
                        db_ws.cell(row=i, column=j).value = cell.value

                db_ws.delete_cols(1)
                db_ws.delete_rows(3)

    ws = db_wb.get_sheet_by_name('Sheet')
    db_wb.remove_sheet(ws)
    db_wb.save(str(db_filename))


