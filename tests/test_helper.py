import unittest
from warcparser.helpers.filehelper import FileHelper


class TestFileHelper(unittest.TestCase):
    """
    Tests for warcparser.helpers.filehelper module.
    """

    def test_check_war_file_exists(self):
        self.assertTrue(FileHelper.check_war_file('test_input/test.warc.gz'))

    def test_check_war_file_does_not_exist(self):
        self.assertFalse(FileHelper.check_war_file('test_input/doesnotexist.warc.gz'))

    def test_file_exists(self):
        self.assertTrue(FileHelper.file_exists('test_input/test.warc.gz'))

    def test_file_does_not_exist(self):
        self.assertFalse(FileHelper.file_exists('test_input/doesnotexist.warc.gz'))


if __name__ == "__main__":
    unittest.main()
