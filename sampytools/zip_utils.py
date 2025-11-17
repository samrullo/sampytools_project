import pathlib
import zipfile
import logging
import gzip
import shutil



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
        logging.info(f"Extracted {zipfilepath} -> {save_to_folder}")
    return save_to_folder


def decompress_gz(gz_path: pathlib.Path, save_to_folder: pathlib.Path = None):
    """
    Decompress a .gz file to the specified folder
    """
    if save_to_folder is None:
        save_to_folder = gz_path.parent

    output_path = save_to_folder / gz_path.stem  # remove .gz extension
    with gzip.open(gz_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    logging.info(f"Extracted {gz_path} -> {output_path}")
    return output_path


def zip_file(file_path: pathlib.Path, zip_path: pathlib.Path = None):
    """
    Create a zip archive containing one file.
    :param file_path: path of the file to zip
    :param zip_path: where to save the zip file (defaults to same folder)
    """
    if zip_path is None:
        zip_path = file_path.parent / f"{file_path.stem}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(file_path, arcname=file_path.name)

    logging.info(f"Zipped {file_path} -> {zip_path}")
    return zip_path