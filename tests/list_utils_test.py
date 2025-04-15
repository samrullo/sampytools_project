import unittest
from sampytools.list_utils import add_new_values_in_certain_item_location


class MyTestCase(unittest.TestCase):
    def test_add_new_values_in_certain_item_location(self):
        orig_list = ["one", "bang", "two"]
        new_list = add_new_values_in_certain_item_location(orig_list, "bang", ["bang_one", "bang_two", "bang_three"],
                                                           include_orig_item=True)
        self.assertEqual(["one", "bang", "bang_one", "bang_two", "bang_three", "two"], new_list)  # add assertion here

    def test_get_dupe_and_nondupe_items_from_list(self):
        from sampytools.list_utils import get_dupe_and_nondupe_items_from_list
        alist = ["one", "two", "three", "one"]
        dupelist, nondupelist = get_dupe_and_nondupe_items_from_list(alist)
        print(dupelist)
        self.assertEqual(len(dupelist), 1)

    def test_get_list_diff(self):
        from sampytools.list_utils import get_list_diff
        list_one = ["one", "two", "three", "five", "seven", "four"]
        list_two = ["one", "two"]
        diff = get_list_diff(list_one, list_two)
        print(diff)
        self.assertTrue(len(diff) == 4)

    def test_get_intersection(self):
        from sampytools.list_utils import get_intersection
        list_one = ["one", "two", "three", "five", "seven", "four"]
        list_two = ["one", "two"]
        intersect = get_intersection(list_one, list_two)
        print(f"intersection : {intersect}")
        self.assertTrue(len(intersect) == 2)


if __name__ == '__main__':
    unittest.main()
