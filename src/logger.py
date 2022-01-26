"""Global logger for project"""
import logging
import sys

LOGGING_FORMAT = "[%(levelname)s] %(asctime)s - %(message)s"


logging.basicConfig(
    stream=sys.stdout,
    filemode="w",
    format=LOGGING_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger()
