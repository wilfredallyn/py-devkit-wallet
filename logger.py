import logging


file_handler = logging.FileHandler("run.log")


def setup_logger():
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        logger.addHandler(file_handler)
    return logger
