import logging
import pathlib


def init_logging(level=logging.INFO):
    logging.basicConfig(level=level,  # Set log level
                        format='%(asctime)s - %(levelname)s - %(message)s')


def init_logging_to_file(log_path: pathlib.Path, level=logging.INFO):
    """
    Re-initializes logging to write to a file, replacing prior handlers if necessary.
    """
    # Ensure the parent directory exists
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Clear all existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Reconfigure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )