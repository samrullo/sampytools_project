import logging


def init_logging(level=logging.INFO):
    logging.basicConfig(
        level=level, format="%(asctime)s - %(levelname)s - %(message)s"  # Set log level
    )
