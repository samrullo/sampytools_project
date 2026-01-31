from typing import Dict


def convert_dict_to_delimited_text(thedict: Dict[str, str], join_char: str = ";", reverse: bool = True) -> str:
    """
    Convert dictionary to a delimited string, where all keys and values are joined with character one after another
    :param thedict:
    :param join_char:
    :param reverse:
    :return:
    """
    key_val_list = []
    for key, val in thedict.items():
        if reverse:
            key_val_list += [str(val), str(key)]
        else:
            key_val_list += [str(key), str(val)]
    return f"{join_char}".join(key_val_list)

def convert_delimited_text_to_dict(text: str, join_char: str = ";", reverse: bool = True) -> Dict[str, str]:
    """
    Convert delimited string to dictionary, where all keys and values are joined with character one after another
    :param text:
    :param join_char:
    :param reverse:
    :return:
    """
    items = text.split(join_char)
    thedict = {}
    for idx in range(0, len(items), 2):
        if reverse:
            thedict[items[idx + 1]] = items[idx]
        else:
            thedict[items[idx]] = items[idx + 1]
    return thedict