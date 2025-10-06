from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time}</green> | <level>{message}</level>")

def get_logger():
    return logger
