import logging


def init_logging(level=logging.INFO):
    logging.basicConfig(level=level,  # Set log level
                        format='%(asctime)s - %(levelname)s - %(message)s')
