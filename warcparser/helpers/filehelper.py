from os import path


class FileHelper:
    """
    File helper class.
    """

    @staticmethod
    def check_war_file(filename: str) -> bool:
        """
        Check if the given filepath contains a valid WARC that can be parsed.
        :param filename: The filepath to read.
        :return: True if valid.
        """
        return path.exists(filename) and (filename.endswith('warc') or filename.endswith('warc.gz'))

    @staticmethod
    def file_exists(filename: str) -> bool:
        """
        Check if the given filepath exists.
        :param filename: A filepath.
        :return: True if it exists.
        """
        return path.exists(filename)
