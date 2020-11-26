import platform


class OsUtils:
    @staticmethod
    def get_os_name() -> str:
        return platform.system().lower()

    @staticmethod
    def is_windows() -> bool:
        if platform.system().lower() == "windows":
            return True
        else:
            return False
