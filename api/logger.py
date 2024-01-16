import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

LOG_FORMAT = "<green>{level}: {time:YYYY-MM-DD at HH:mm:ss}</green> <blue>({extra[source]}::{function})</blue> {message}"
logger.remove()
logger.add(sys.stdout, colorize=True, format=LOG_FORMAT, level=LOG_LEVEL)
logger.add("logs/app.log", format=LOG_FORMAT, level=LOG_LEVEL,
           rotation="1 day", retention="1 year", compression="zip")


def get_logger(source):
    return logger.bind(source=source)
