import unittest
import pathlib
import tempfile
import shutil
import gzip

from sampytools.zip_utils import decompress_gz


class TestDecompressGz(unittest.TestCase):
    def setUp(self):
        # create temporary directory for testing
        self.tempdir = pathlib.Path(tempfile.mkdtemp())
        self.sample_name = "example.txt"
        self.sample_file = self.tempdir / self.sample_name
        self.sample_data = b"this is a test file\n"

        # write the plain file (we'll gzip it next)
        self.sample_file.write_bytes(self.sample_data)

        # create a .gz compressed version of the sample
        self.gz_path = self.tempdir / (self.sample_name + ".gz")
        with open(self.sample_file, "rb") as f_in:
            with gzip.open(self.gz_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        # remove the uncompressed original to ensure decompress produces it
        self.sample_file.unlink()

    def tearDown(self):
        # clean up the temporary directory after each test
        shutil.rmtree(self.tempdir)

    def test_decompress_gz_default_location(self):
        """When save_to_folder is None, output should appear next to the .gz file."""
        returned_path = decompress_gz(self.gz_path)

        # expected output path is same folder, filename without .gz
        expected_path = self.gz_path.parent / self.gz_path.stem
        self.assertEqual(returned_path, expected_path)
        self.assertTrue(expected_path.exists(), "Expected decompressed file to exist")

        # check contents match original bytes
        data = expected_path.read_bytes()
        self.assertEqual(data, self.sample_data)

    def test_decompress_gz_custom_folder(self):
        """When save_to_folder is provided, the output file is written there."""
        custom_dir = self.tempdir / "out"
        custom_dir.mkdir()

        returned_path = decompress_gz(self.gz_path, save_to_folder=custom_dir)

        expected_path = custom_dir / self.gz_path.stem
        self.assertEqual(returned_path, expected_path)
        self.assertTrue(expected_path.exists())
        self.assertEqual(expected_path.read_bytes(), self.sample_data)

    def test_decompress_gz_overwrite_if_exists(self):
        """If output file already exists, decompress should overwrite it."""
        expected_path = self.gz_path.parent / self.gz_path.stem
        # create an existing file with different content
        expected_path.write_bytes(b"old content\n")

        returned_path = decompress_gz(self.gz_path)
        self.assertEqual(returned_path, expected_path)
        # ensure content was replaced
        self.assertEqual(expected_path.read_bytes(), self.sample_data)

    def test_decompress_gz_missing_file_raises(self):
        """Trying to decompress a missing file should raise FileNotFoundError."""
        missing = self.tempdir / "no_such_file.txt.gz"
        with self.assertRaises(FileNotFoundError):
            decompress_gz(missing)


if __name__ == "__main__":
    unittest.main()
