import pandas as pd
import pathlib
import logging
import re

def locate_filename(thefolder: pathlib.Path, pattern: re.Pattern) -> str:
    matched_filenames = [file.name for file in thefolder.iterdir() if re.match(pattern, file.name.lower())]
    if len(matched_filenames) == 0:
        logging.warning(f"Could not locate file matching pattern {pattern} in folder {thefolder}")
        return ""
    elif len(matched_filenames) > 1:
        logging.warning(
            f"Multiple files matching pattern {pattern} in folder {thefolder}: {matched_filenames}. Using the first one.")
    return matched_filenames[0]
