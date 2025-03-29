import unittest
import pathlib
import shutil


class MyTestCase(unittest.TestCase):
    def test_unzip_archive(self):
        from sampytools.zip_utils import unzip_archive
        wfolder = pathlib.Path.cwd() / "test_data"
        zipfilepath = wfolder / "myfiles.zip"
        save_to_folder=zipfilepath.parent
        unzip_archive(zipfilepath, save_to_folder)
        unzip_archive(zipfilepath)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
