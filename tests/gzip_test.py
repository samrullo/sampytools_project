import unittest
import pathlib
import tempfile
import shutil
import gzip
import os

# adjust import path as needed; this assumes compress_to_gz and decompress_gz
# are defined in sampytools.zip_utils
from sampytools.zip_utils import decompress_gz, compress_to_gz


class TestGzUtils(unittest.TestCase):
    def setUp(self):
        # create temporary directory for testing
        self.tempdir = pathlib.Path(tempfile.mkdtemp())
        self.sample_name = "example.txt"
        self.sample_file = self.tempdir / self.sample_name
        self.sample_data = b"this is a test file\n"

        # write the plain file (we'll gzip it next for decompress tests)
        self.sample_file.write_bytes(self.sample_data)

        # create a .gz compressed version of the sample (used by decompress tests)
        self.gz_path = self.tempdir / (self.sample_name + ".gz")
        with open(self.sample_file, "rb") as f_in:
            with gzip.open(self.gz_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        # remove the uncompressed original to ensure decompress produces it
        self.sample_file.unlink()

    def tearDown(self):
        # clean up the temporary directory after each test
        shutil.rmtree(self.tempdir)

    #
    # Tests for decompress_gz (your original cases)
    #
    def test_decompress_gz_default_location(self):
        """When save_to_folder is None, output should appear next to the .gz file."""
        returned_path = decompress_gz(self.gz_path)

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

    #
    # Tests for compress_to_gz (new tests)
    #
    def test_compress_to_gz_creates_gz_next_to_file(self):
        """compress_to_gz should create a .gz file next to the input file by default."""
        # create plain file to compress
        plain = self.tempdir / "to_compress.txt"
        plain.write_bytes(self.sample_data)

        gz_path = compress_to_gz(plain)

        expected_gz = plain.parent / (plain.name + ".gz")
        self.assertEqual(gz_path, expected_gz)
        self.assertTrue(expected_gz.exists(), "Expected .gz file to be created")
        # sanity check: decompress and compare bytes
        with gzip.open(expected_gz, "rb") as f_in:
            contents = f_in.read()
        self.assertEqual(contents, self.sample_data)

    def test_compress_to_gz_custom_folder_and_roundtrip(self):
        """compress_to_gz should allow specifying output folder; round-trip decompress matches."""
        plain = self.tempdir / "roundtrip.txt"
        plain.write_bytes(self.sample_data)

        outdir = self.tempdir / "gz_out"
        outdir.mkdir()

        gz_path = compress_to_gz(plain, save_to_folder=outdir)
        self.assertTrue(gz_path.exists())

        # remove original then decompress into same outdir to verify round-trip
        plain.unlink()
        decompressed = decompress_gz(gz_path, save_to_folder=outdir)
        self.assertTrue(decompressed.exists())
        self.assertEqual(decompressed.read_bytes(), self.sample_data)

    def test_compress_to_gz_overwrite_gz_if_exists(self):
        """If a .gz with same name exists, compress_to_gz should overwrite it."""
        plain = self.tempdir / "overwrite.txt"
        plain.write_bytes(self.sample_data)

        gz_path = compress_to_gz(plain)
        # write different bytes into the gz (simulate stale file)
        with gzip.open(gz_path, "wb") as f:
            f.write(b"old gz content")

        # compress again, should overwrite
        gz_path2 = compress_to_gz(plain)
        self.assertEqual(gz_path, gz_path2)
        with gzip.open(gz_path, "rb") as f:
            new_bytes = f.read()
        self.assertEqual(new_bytes, self.sample_data)

    def test_compress_to_gz_missing_input_raises(self):
        """Trying to compress a non-existing input should raise FileNotFoundError."""
        missing = self.tempdir / "does_not_exist.txt"
        with self.assertRaises(FileNotFoundError):
            compress_to_gz(missing)


if __name__ == "__main__":
    unittest.main()
