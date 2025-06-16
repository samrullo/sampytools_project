import unittest
import pathlib
import json
from typing import Dict

# Assume the target function is in json_utils.py
# Adjust the import based on your project structure
from sampytools.json_utils import read_json_file


class TestReadJsonFile(unittest.TestCase):
    def setUp(self):
        # Create a test directory and a temporary JSON file
        self.test_dir = pathlib.Path.cwd() / "testdata"
        self.test_dir.mkdir(exist_ok=True)
        self.test_file = self.test_dir / "sample.json"
        self.test_data = {
            "name": "Subkhon",
            "role": "developer",
            "skills": ["python", "data analysis"]
        }
        self.test_file.write_text(json.dumps(self.test_data), encoding="utf-8")

    def test_read_json_file(self):
        # Read the file using the target function
        result: Dict = read_json_file(self.test_file)

        # Validate the contents
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], self.test_data["name"])
        self.assertListEqual(result["skills"], self.test_data["skills"])

    def tearDown(self):
        # Clean up test file
        if self.test_file.exists():
            self.test_file.unlink()
        if self.test_dir.exists():
            self.test_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
