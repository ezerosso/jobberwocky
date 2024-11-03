import logging
import sys

def setup_logger():
    logger = logging.getLogger('jobberwocky')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()