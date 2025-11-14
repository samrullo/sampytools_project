import unittest
import pathlib
import tempfile
import zipfile
import shutil

# adjust the import to where your zip_file is defined
from sampytools.zip_utils import zip_file


class TestZipFile(unittest.TestCase):
    def setUp(self):
        # create a temp dir for each test
        self.tempdir = pathlib.Path(tempfile.mkdtemp())
        # sample file to be zipped
        self.sample_file = self.tempdir / "hello.txt"
        self.sample_contents = b"hello unit test\n"
        self.sample_file.write_bytes(self.sample_contents)

    def tearDown(self):
        # clean up tempdir
        shutil.rmtree(self.tempdir)

    def test_zip_file_creates_zip_default_path(self):
        """
        When zip_path is omitted, zip_file should create <file_stem>.zip
        in the same folder and include the file with arcname == file.name.
        """
        # call function under test (no zip_path -> default behavior)
        zip_file(self.sample_file)

        expected_zip = self.sample_file.parent / f"{self.sample_file.stem}.zip"
        self.assertTrue(expected_zip.exists(), f"Expected zip at {expected_zip} but not found")

        # open zip and check contents
        with zipfile.ZipFile(expected_zip, "r") as z:
            namelist = z.namelist()
            # arcname used in implementation is file.name -> "hello.txt"
            self.assertIn(self.sample_file.name, namelist)
            # read the file from archive and compare bytes
            with z.open(self.sample_file.name, "r") as f:
                read_bytes = f.read()
            self.assertEqual(read_bytes, self.sample_contents)

    def test_zip_file_creates_zip_explicit_path(self):
        """
        When zip_path is provided, zip_file should write to that path and
        still include the file with arcname == file.name.
        """
        custom_zip = self.tempdir / "custom_archive.zip"
        # call with explicit zip_path
        zip_file(self.sample_file, zip_path=custom_zip)

        self.assertTrue(custom_zip.exists(), "Expected custom zip file to exist")

        with zipfile.ZipFile(custom_zip, "r") as z:
            self.assertIn(self.sample_file.name, z.namelist())
            with z.open(self.sample_file.name, "r") as f:
                read_bytes = f.read()
            self.assertEqual(read_bytes, self.sample_contents)


if __name__ == "__main__":
    unittest.main()
