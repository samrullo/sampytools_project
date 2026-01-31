import unittest

from sampytools.dict_utils import convert_delimited_text_to_dict, convert_dict_to_delimited_text


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


class TestConvertDelimitedTextToDict(unittest.TestCase):

    def test_reverse_true_default_join(self):
        # reverse=True => value;key;value;key...
        text = "1;a;2;b"
        result = convert_delimited_text_to_dict(text)
        expected = {"a": "1", "b": "2"}
        self.assertEqual(result, expected)

    def test_reverse_false_default_join(self):
        # reverse=False => key;value;key;value...
        text = "a;1;b;2"
        result = convert_delimited_text_to_dict(text, reverse=False)
        expected = {"a": "1", "b": "2"}
        self.assertEqual(result, expected)

    def test_custom_join_char(self):
        text = "10,x,20,y"
        result = convert_delimited_text_to_dict(text, join_char=",", reverse=True)
        expected = {"x": "10", "y": "20"}
        self.assertEqual(result, expected)

    def test_empty_text(self):
        # Current behavior: "".split(";") -> [""] and loop tries idx+1 => IndexError
        with self.assertRaises(IndexError):
            convert_delimited_text_to_dict("")

    def test_single_pair_reverse_true(self):
        text = "bar;foo"
        result = convert_delimited_text_to_dict(text, reverse=True)
        expected = {"foo": "bar"}
        self.assertEqual(result, expected)

    def test_single_pair_reverse_false(self):
        text = "foo;bar"
        result = convert_delimited_text_to_dict(text, reverse=False)
        expected = {"foo": "bar"}
        self.assertEqual(result, expected)

    def test_odd_number_of_items_raises(self):
        # Missing the final key/value partner should raise IndexError (current behavior)
        with self.assertRaises(IndexError):
            convert_delimited_text_to_dict("1;a;2", reverse=True)

    def test_duplicate_keys_last_wins(self):
        # reverse=True => key is the second item in each pair
        text = "1;a;2;a"
        result = convert_delimited_text_to_dict(text, reverse=True)
        self.assertEqual(result, {"a": "2"})


if __name__ == "__main__":
    unittest.main()
