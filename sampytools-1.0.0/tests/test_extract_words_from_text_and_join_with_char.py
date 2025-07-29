import re
import unittest

from sampytools.text_utils import extract_words_from_text_and_join_with_char

class TestExtractWordsAndJoin(unittest.TestCase):

    def test_default_join_char(self):
        result = extract_words_from_text_and_join_with_char("Hello world! This is great.")
        self.assertEqual(result, "Hello_world_This_is_great")

    def test_custom_join_char(self):
        result = extract_words_from_text_and_join_with_char("Hello world!", join_char="-")
        self.assertEqual(result, "Hello-world")

    def test_empty_text(self):
        result = extract_words_from_text_and_join_with_char("")
        self.assertEqual(result, "")

    def test_text_with_special_chars_only(self):
        result = extract_words_from_text_and_join_with_char("!@#$%^&*")
        self.assertEqual(result, "")

    def test_text_with_numbers(self):
        result = extract_words_from_text_and_join_with_char("abc 123 def")
        self.assertEqual(result, "abc_123_def")

    def test_join_char_as_space(self):
        result = extract_words_from_text_and_join_with_char("Multiple   spaces here", join_char=" ")
        self.assertEqual(result, "Multiple spaces here")

if __name__ == '__main__':
    unittest.main()
