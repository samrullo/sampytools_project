import itertools
from collections import Counter
from typing import List, Tuple, Any, Dict, Union


def flatten_list_of_lists(list_of_lists):
    return list(itertools.chain.from_iterable(list_of_lists))


def get_list_from_string(the_string_of_lines):
    the_list = the_string_of_lines.split("\n")
    the_list = [item.strip() for item in the_list]
    if "" in the_list:
        the_list.remove("")
    return the_list


def get_chunked_list(original_list, chunk_size: int = 400):
    chunked_list = [original_list[i:i + chunk_size] for i in range(0, len(original_list), chunk_size)]
    return chunked_list


def generate_comma_separated_text(item_list, with_quote=True):
    str_item_list = [str(item).strip() for item in item_list]
    if with_quote:
        comma_seperated_text = ','.join(f"'{item}'" for item in str_item_list)
    else:
        comma_seperated_text = ','.join(str_item_list)
    return comma_seperated_text


def search_list(_list: List[str], _text: str) -> List[str]:
    """
    Get elements of a list that contain certain text
    :param _list: list of strings
    :param _text: string to search in the list
    :return:
    """
    return [item for item in _list if _text.lower() in item.lower()]


def get_intersection(list1, list2):
    """
    Get intersection of two lists
    This returns elements that are both in list1 and list2
    :param list1:
    :param list2:
    :return:
    """
    set2 = set(list2)
    return list(dict.fromkeys(item for item in list1 if item in set2))


def get_list_diff(list1:list, list2:list):
    """
    Get difference between two lists
    This return elements form list1 that are not in list2
    :param list1:
    :param list2:
    :return:
    """
    return list(dict.fromkeys(item for item in list1 if item not in set(list2)))



def print_list_items(mylist):
    for item in mylist:
        print(item)


def reverse_list(thelist: List[Any]) -> List[Any]:
    """
    Reverse list items and return new list
    """
    return thelist[::-1]


def construct_dict_from_list_of_key_values(flat_list: List[Any]) -> Dict[Any, Any]:
    """
    Convert a flat list where keys and values appear one after another to dictionary
    """
    return dict(zip(flat_list[::2], flat_list[1::2]))


def add_new_values_in_certain_item_location(orig_list: List[Any], item_val: Union[str, int, float], new_vals: List[Any],
                                            include_orig_item: bool = True) -> List[Any]:
    """
    Add new values in the location where item_val appears
    :param orig_list:
    :param item_val:
    :param new_vals:
    :param include_orig_item: whether to include original item in the list
    :return:
    """
    item_index = orig_list.index(item_val)
    if include_orig_item:
        return orig_list[:item_index + 1] + new_vals + orig_list[item_index + 1:]
    else:
        return orig_list[:item_index] + new_vals + orig_list[item_index + 1:]


def get_unique_records_from_list(alist: List[Union[str, int, float, Any]]) -> List[Union[str, int, float, Any]]:
    """
    Get unique records from a list of strings, integers, floats or any other type
    :param alist: list of strings or floats or integers or any types
    :return: unique list of records with order preserved
    """
    return list(dict.fromkeys(alist))


def get_field_counts_of_records(list_of_records: List[List[str]]) -> Counter:
    """
    return field counts of records in a list of records
    :param list_of_records:
    :return:
    """
    return Counter([len(record) for record in list_of_records])


def get_dupe_and_nondupe_items_from_list(alist: List[str]) -> Tuple[List[str], List[str]]:
    """
    Get duplicate and non-duplicate items from a list
    :param alist:
    :return:
    """
    cnt = Counter(alist)
    dupe_items = [item for item, count in cnt.items() if count > 1]
    nondupe_items = [item for item, count in cnt.items() if count == 1]
    return dupe_items, nondupe_items
