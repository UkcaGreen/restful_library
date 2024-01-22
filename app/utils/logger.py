import logging


def create_custom_logger(name: str) -> logging.Logger:
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    custom_logger = logging.getLogger(name)
    custom_logger.setLevel(logging.DEBUG)

    custom_logger.addHandler(handler)

    return custom_logger
