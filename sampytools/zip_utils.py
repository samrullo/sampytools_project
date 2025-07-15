import pathlib
import zipfile


def unzip_archive(zipfilepath: pathlib.Path, save_to_folder: pathlib.Path = None):
    """
    Unzip zipped file to specified folder
    :param zipfilepath: zipped file path
    :param save_to_folder: save to folder
    :return:
    """
    if save_to_folder is None:
        save_to_folder = zipfilepath.parent / zipfilepath.stem
    with zipfile.ZipFile(zipfilepath, "r") as z:
        z.extractall(save_to_folder)
