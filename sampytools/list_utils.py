import itertools


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


def search_list(_list, _text):
    """
    Get elements of a list that contain certain text
    :param _list:
    :param _text:
    :return:
    """
    return [item for item in _list if _text in item]


def get_intersection(list1, list2):
    """
    Get intersection of two lists
    This returns elements that are both in list1 and list2
    :param list1:
    :param list2:
    :return:
    """
    return list(set(list1) & set(list2))


def get_list_diff(list1, list2):
    """
    Get difference between two lists
    This return elements form list1 that are not in list2
    :param list1:
    :param list2:
    :return:
    """
    return list(set(list1) - set(list2))


def print_list_items(mylist):
    for item in mylist:
        print(item)