import unittest

from sampytools.dict_utils import convert_dict_to_delimited_text


class TestConvertDictToDelimitedText(unittest.TestCase):

    def test_reverse_true_default_join(self):
        d = {"a": "1", "b": "2"}
        result = convert_dict_to_delimited_text(d)
        # reverse=True, so order is value-key repeated
        expected = "1;a;2;b"
        self.assertEqual(result, expected)

    def test_reverse_false_default_join(self):
        d = {"a": "1", "b": "2"}
        result = convert_dict_to_delimited_text(d, reverse=False)
        expected = "a;1;b;2"
        self.assertEqual(result, expected)

    def test_custom_join_char(self):
        d = {"x": "10", "y": "20"}
        result = convert_dict_to_delimited_text(d, join_char=",")
        expected = "10,x,20,y"
        self.assertEqual(result, expected)

    def test_empty_dict(self):
        d = {}
        result = convert_dict_to_delimited_text(d)
        expected = ""
        self.assertEqual(result, expected)

    def test_single_item(self):
        d = {"foo": "bar"}
        result_true = convert_dict_to_delimited_text(d, reverse=True)
        result_false = convert_dict_to_delimited_text(d, reverse=False)
        self.assertEqual(result_true, "bar;foo")
        self.assertEqual(result_false, "foo;bar")


if __name__ == "__main__":
    unittest.main()
