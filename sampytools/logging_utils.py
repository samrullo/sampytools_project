import logging
import pathlib


def init_logging(level=logging.INFO):
    logging.basicConfig(level=level,  # Set log level
                        format='%(asctime)s - %(levelname)s - %(message)s')


def init_logging_to_file(log_path: pathlib.Path, level=logging.INFO, mode: str = 'a'):
    """
    Re-initializes logging to write to a file, replacing prior handlers if necessary.

    Parameters:
    - log_path: Path to the log file.
    - level: Logging level (e.g., logging.INFO).
    - mode: File mode - 'a' to append (default), 'w' to overwrite.
    """
    # Validate mode
    if mode not in ('a', 'w'):
        raise ValueError("mode must be either 'a' (append) or 'w' (overwrite)")

    # Ensure the parent directory exists
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Clear all existing handlers
    for handler in logging.root.handlers[:]:
        handler.flush()
        handler.close()
        logging.root.removeHandler(handler)

    # Reconfigure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, mode=mode, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
