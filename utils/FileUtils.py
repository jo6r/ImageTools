import os
import shutil
from pathlib import Path
from typing import List


class FileUtils:
    @staticmethod
    def get_list_of_files(path: str) -> List[str]:
        list_of_files = list()
        for (dirpath, dirnames, filenames) in os.walk(path):
            list_of_files += [os.path.join(dirpath, file) for file in filenames]

        return list_of_files

    @staticmethod
    def get_list_of_files_filter(path: str, ext_filter: List[str]) -> List[str]:
        list_of_files = list()
        for (dirpath, dirnames, filenames) in os.walk(path):
            list_of_files += [os.path.join(dirpath, file) for file in filenames if Path(file).suffix in ext_filter]

        return list_of_files

    @staticmethod
    def file_exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def gen_file_name_suffix(path: str, suffix="_temp") -> str:
        """
        Generate temp file name based on input file path
        :param path: file path
        :param suffix: suffix of temp file
        :return: path to temp file
        """
        ext = Path(path).suffix
        return str.replace(path, ext, "") + suffix + ext

    @staticmethod
    def backup_file(path) -> str:
        backup_path = FileUtils.gen_file_name_suffix(path, "_original")
        return shutil.copy(path, backup_path)

    @staticmethod
    def move(src_path: str, dest_path: str) -> str:
        return shutil.move(src_path, dest_path)
