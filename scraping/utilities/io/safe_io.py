import logging
import os
import shutil

log = logging.getLogger("safe_io")


def rename(old_name: str, new_name: str):
    """
    Renames file or folder and logs error when an error occurs

    Args:
        old_name (str): File or folder path to be renamed
        new_name (str): New name or path
    """
    try:
        os.rename(old_name, new_name)
    except PermissionError as e:
        log.warning(f"File or folder {old_name} could not be renamed to {new_name}.\nError: {e}")


def delete_file(path: str):
    """
    Deletes file and logs error when an error occurs

    Args:
        path (str): Path of file to be removed
    """
    try:
        if os.path.exists(path):
            os.remove(path)
        else:
            log.info(f"File {path} does not exist.")
    except PermissionError as e:
        log.warning(f"File {path} could not be removed.\nError: {e}")


def delete_folder(path: str):
    """
    Deletes folder and logs error when an error occurs

    Args:
        path (str): Path of folder to be removed
    """
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
        else:
            log.info(f"Folder {path} does not exist.")
    except PermissionError as e:
        log.warning(f"Folder {path} could not be removed.\nError: {e}")
