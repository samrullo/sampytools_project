import unittest
import pathlib
import tempfile
import zipfile
import shutil

from sampytools.zip_utils import zip_file  # adjust if the import path differs


class TestZipFile(unittest.TestCase):
    def setUp(self):
        # create temporary directory for testing
        self.tempdir = pathlib.Path(tempfile.mkdtemp())
        self.sample_file = self.tempdir / "example.txt"
        self.sample_data = b"this is a test file\n"
        self.sample_file.write_bytes(self.sample_data)

    def tearDown(self):
        # clean up the temporary directory after each test
        shutil.rmtree(self.tempdir)

    def test_zip_file_default_path(self):
        """Test that zip_file() creates <filename>.zip when zip_path is None."""
        zip_path = zip_file(self.sample_file)

        # assert zip file created correctly
        self.assertTrue(zip_path.exists(), f"Expected zip file {zip_path} to exist.")
        self.assertEqual(zip_path.suffix, ".zip")

        # verify archive contents
        with zipfile.ZipFile(zip_path, "r") as z:
            namelist = z.namelist()
            self.assertIn(self.sample_file.name, namelist)

            # verify file content is the same after extraction
            with z.open(self.sample_file.name) as f:
                extracted_data = f.read()
            self.assertEqual(extracted_data, self.sample_data)

    def test_zip_file_custom_path(self):
        """Test that zip_file() writes to a user-specified zip_path."""
        custom_zip = self.tempdir / "custom_output.zip"
        result_path = zip_file(self.sample_file, custom_zip)

        # assert returned path equals the one we passed
        self.assertEqual(result_path, custom_zip)
        self.assertTrue(custom_zip.exists())

        with zipfile.ZipFile(custom_zip, "r") as z:
            self.assertIn(self.sample_file.name, z.namelist())

    def test_zip_file_overwrite_existing(self):
        """Test that zip_file() overwrites an existing zip file cleanly."""
        zip_path = self.tempdir / "overwrite.zip"

        # create a dummy zip file first
        with zipfile.ZipFile(zip_path, "w") as z:
            z.writestr("dummy.txt", "old content")

        # now call zip_file() again, it should overwrite
        zip_file(self.sample_file, zip_path)

        with zipfile.ZipFile(zip_path, "r") as z:
            namelist = z.namelist()
            self.assertNotIn("dummy.txt", namelist)  # old file removed
            self.assertIn(self.sample_file.name, namelist)


if __name__ == "__main__":
    unittest.main()
