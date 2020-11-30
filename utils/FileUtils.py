import os
import shutil
from pathlib import Path
from typing import List


class FileUtils:
    @staticmethod
    def get_list_of_files(path: str) -> List[str]:
        """
        return all files from folder and sub-folders
        :param path: path to root folder
        :return: List of files (paths)
        """
        list_of_files = list()
        for (dirpath, dirnames, filenames) in os.walk(path):
            list_of_files += [os.path.join(dirpath, file) for file in filenames]

        return list_of_files

    @staticmethod
    def get_list_of_files_filter(path: str, ext_filter: List[str]) -> List[str]:
        """
        return filtered files from folder and sub-folders
        :param path: path to root folder
        :param ext_filter: list of allowed extensions [".jpg", ".png"]
        :return: List of files (paths)
        """
        list_of_files = list()
        for (dirpath, dirnames, filenames) in os.walk(path):
            list_of_files += [os.path.join(dirpath, file) for file in filenames if Path(file).suffix in ext_filter]

        return list_of_files

    @staticmethod
    def file_exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def get_file_ext(path: str) -> str:
        return Path(path).suffix

    @staticmethod
    def get_file_name(path: str) -> str:
        return Path(path).name

    @staticmethod
    def get_file_path(path: str) -> str:
        return Path(path).parent

    @staticmethod
    def backup_file(path, suffix="_original") -> str:
        """
        backup file in same folder with different name
        :param suffix: suffix witch is added do file name
        :param path: path to file
        :return: path to new file
        """
        backup_path = FileUtils.gen_temp_file_name(path, suffix)
        return shutil.copy(path, backup_path)

    @staticmethod
    def gen_temp_file_name(path: str, suffix="_temp") -> str:
        """
        Generate temporary file name based on input file path
        :param path: file path
        :param suffix: suffix of temp file
        :return: path to temporary file
        """
        ext = FileUtils.get_file_ext(path)
        return str.replace(path, ext, "") + suffix + ext

    @staticmethod
    def move(src_path: str, dest_path: str) -> str:
        return shutil.move(src_path, dest_path)
