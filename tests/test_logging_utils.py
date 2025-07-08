import unittest
import logging
import tempfile
import pathlib
import os

from sampytools.logging_utils import init_logging, init_logging_to_file


class TestLoggingFunctions(unittest.TestCase):

    def tearDown(self):
        # Reset logging configuration after each test
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(handlers=[], force=True)

    def test_init_logging_sets_basic_config(self):
        init_logging(level=logging.DEBUG)
        self.assertEqual(logging.getLogger().level, logging.DEBUG)

        # Check that a log message can be emitted
        with self.assertLogs(level='DEBUG') as cm:
            logging.debug("Test debug message")
        self.assertTrue(any("Test debug message" in msg for msg in cm.output))

    def test_init_logging_to_file_creates_log_file_and_logs(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            log_path = pathlib.Path(tmpdirname) / "test.log"

            init_logging_to_file(log_path, level=logging.WARNING)

            # Emit log messages
            logging.debug("This should not appear")
            logging.warning("This should appear")

            # Flush and close all handlers to release file handles
            for handler in logging.getLogger().handlers:
                handler.flush()
                handler.close()
            logging.getLogger().handlers.clear()

            # Now it's safe to read the file
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.assertIn("This should appear", content)
            self.assertNotIn("This should not appear", content)
            self.assertTrue(log_path.exists())


if __name__ == '__main__':
    unittest.main()
