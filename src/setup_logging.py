import os
import logging

import logging

LOG_FILE_PATH = os.path.join("log", "log")

def get_logger():
    logger = logging.getLogger()
    handler = logging.FileHandler(LOG_FILE_PATH)
    formatter = logging.Formatter('%(asctime)s %(levelname)-5s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

log = get_logger()
