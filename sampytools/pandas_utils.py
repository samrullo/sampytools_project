import pathlib
import pandas as pd
import logging
import re
from typing import List, Tuple, Dict, Union,Any
from sampytools.list_utils import construct_dict_from_list_of_key_values, reverse_list, \
    add_new_values_in_certain_item_location
from enum import IntEnum


def make_column_names_unique(df: pd.DataFrame) -> pd.DataFrame:
    """
    for dataframes that have duplicate column names, make column names unique by adding indices to their names
    :param df: dataframe
    :return: dataframe now with columns renamed to be unique
    """
    cols = df.columns.tolist()
    cols_df = pd.DataFrame({'col_idx': cols, 'col_name': cols})
    cols_count_df = cols_df.groupby('col_idx')[['col_name']].count()

    def append_index_to_duplicate_columns(duplicate_columns, cols_list):
        new_cols = []
        for col in cols_list:
            if col in duplicate_columns.keys():
                new_cols.append(col + str(duplicate_columns[col]))
                duplicate_columns[col] += 1
            else:
                new_cols.append(col)
        return new_cols

    duplicate_columns = cols_count_df[cols_count_df['col_name'] > 1].index.tolist()
    duplicate_cols_dict = {col: 1 for col in duplicate_columns}

    return df[append_index_to_duplicate_columns(duplicate_cols_dict, cols)]


def strip_string_columns(df, string_columns) -> pd.DataFrame:
    """
    Strip blanks from the end of string values
    :param df: dataframe
    :param string_columns: columns with string values
    :return: dataframe whose string values are now stripped
    """
    for col in string_columns:
        df[col] = df[col].fillna("")
        df[col] = df[col].apply(str.strip)
    return df


def strip_trailing_and_leading_spaces_from_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip trailing and leading white spaces from string values of dataframe columns
    :param df: dataframe
    :return: dataframe now with string columns stripped of trailing and leading whitespaces
    """
    # this will attempt to convert all columns to strings
    for col in df.columns:
        try:
            df[col] = df[col].fillna("")
            df[col] = df[col].apply(str.strip)
            df[col] = df[col].apply(str.lstrip)
        except Exception as e:
            logging.info(f"strip_trailing_and_leading_spaces_from_dataframe error on col {col}: {e}")
            continue
    return df


def convert_columns_to_numeric(df: pd.DataFrame, numeric_columns: List[str], fill_na_val: float = 0.0) -> pd.DataFrame:
    """
    convert specified columns to numeric
    :param df: dataframe
    :param numeric_columns: list of columns that should be converted to numeric type
    :param fill_na_val : fill na value
    :return: dataframe now with numeric columns
    """
    for col in numeric_columns:
        df[col] = df[col].fillna(fill_na_val)
        df[col] = pd.to_numeric(df[col])
    return df


def diff_df_maker(df: pd.DataFrame, cols: List[str], diff_cols: List[str], index: str,
                  suffixes: Tuple[str, str] = ('_x', '_y')) -> pd.DataFrame:
    """
    Compare values of related columns in a merged dataframe by taking difference, absolute difference and ratio
    :param df: dataframe
    :param cols: list of column names before merging two dataframes
    :param diff_cols: list of numeric columns names that need to be compared
    :param index: the column name on which two dataframes were merged
    :param suffixes: tuple suffixes that were used when merging two dataframes
    :return: dataframe with comparison
    """
    write_cols = []
    if not isinstance(index, list):
        index = [index]
    for col in cols:
        if col in index:
            write_cols.append(col)
        else:
            write_cols.append(col + suffixes[0])
            write_cols.append(col + suffixes[1])
            if col in diff_cols:
                write_cols.append('diff_' + col)
                write_cols.append('diff_' + col + '_pct')
                write_cols.append('abs_diff_' + col)
                write_cols.append('abs_diff_' + col + '_pct')
                df['diff_' + col] = df[col + suffixes[0]] - df[col + suffixes[1]]
                df['diff_' + col + '_pct'] = (df[col + suffixes[0]] / df[col + suffixes[1]] - 1) * 100
                df['abs_diff_' + col] = abs(df[col + suffixes[0]] - df[col + suffixes[1]])
                df['abs_diff_' + col + '_pct'] = abs((df[col + suffixes[0]] / df[col + suffixes[1]] - 1) * 100)
    return df[write_cols].copy()


def group_count_sort_series(df, group_cols, count_column, ascending=False):
    """
    Group by specified columns and returns counts in descending order
    :param df:
    :param group_cols:
    :param count_column:
    :param ascending:
    :return:
    """
    return df.groupby(group_cols)[count_column].count().sort_values(ascending=ascending)


def order_merged_dataframe_cols(mrg_df:pd.DataFrame, index_cols:List[str], mrg_cols:List[str], suffixes:Tuple[str,str])->pd.DataFrame:
    """
    Order columns of the merged dataframe so that relevant columns appear side by side
    :param mrg_df: dataframe that is the result of merging two dataframes with identical columns
    :param index_cols: index columns used when merging two dataframes
    :param mrg_cols: columns that have suffixes appended to them
    :param suffixes: suffixes used when merging two dataframes
    :return: merged dataframes with columns ordered
    """
    suffix_x, suffix_y = suffixes
    ordered_cols = index_cols
    for col in mrg_cols:
        ordered_cols.append(col + suffix_x)
        ordered_cols.append(col + suffix_y)
    return mrg_df[ordered_cols]


def compare_dataframes(df1, df2, on='index', how='left', suffix_one='_one', suffix_two='_two'):
    """
    Merge two dataframes on a common key and sort columns s
    :param df1:
    :param df2:
    :param on:
    :param how:
    :return:
    """
    mrg_df = pd.merge(right=df1, left=df2, on=on, how=how, suffixes=(suffix_one, suffix_two))
    mrg_cols = df1.columns.tolist()
    mrg_cols.remove(on)
    mrg_df = order_merged_dataframe_cols(mrg_df, on, mrg_cols, (suffix_one, suffix_two))
    return mrg_df


def pandas_multi_index_to_columns(agg_df: pd.DataFrame):
    """
    Move multi-index to columns
    :param agg_df:
    :return: dataframe whose multi index values are moved to individual columns
    """
    index_names = list(agg_df.index.names)
    existing_cols = list(agg_df.columns)
    for col in index_names:
        agg_df[col] = agg_df.index.get_level_values(col)
    agg_df = agg_df[index_names + existing_cols]
    agg_df.index = range(len(agg_df))
    return agg_df


def pandas_series_multi_index_to_columns(agg_series: pd.Series, series_col_name: str = "count") -> pd.DataFrame:
    """
    Multi index series to dataframe with columns representing each level of multi level index
    :param agg_series: series with multi level index
    :param series_col_name: series column name
    :return: dataframe with columns representing levels of multi level index
    """
    index_names = list(agg_series.index.names)
    df = pd.DataFrame({series_col_name: agg_series.values})
    cols = index_names + [series_col_name]
    for col in index_names:
        df[col] = agg_series.index.get_level_values(col)
    df = df[cols]
    df.index = range(len(df))
    return df


def wrap_code_in_wiki_macro(code_text):
    return f"""<div class="content-wrapper">
            <ac:structured-macro ac:macro-id="b87ebee5-5cfb-49aa-a5f1-b0586f8ec0e0" ac:name="code" ac:schema-version="1">
              <ac:parameter ac:name="language">sql</ac:parameter>
              <ac:parameter ac:name="theme">Midnight</ac:parameter>
              <ac:plain-text-body><![CDATA[{code_text}]]></ac:plain-text-body>
            </ac:structured-macro>
          </div>"""


def convert_dataframe_to_wiki_table(df, code_col="empty", good_table_class_name="some_code", col_styles=None):
    """
    Convert dataframe into good wiki table
    :param df:
    :param code_col:
    :param good_table_class_name:
    :param col_styles:
    :return:
    """
    cols = df.columns.tolist()
    if not col_styles:
        col_styles = {col: 200 if col != code_col else 1000 for col in cols}
    header = f"""<div class="{good_table_class_name}">
              <p>
                <br/>
              </p>
              <table class="wrapped">
                <colgroup>{"".join(['<col style="width:' + str(col_styles[col]) + 'px;"/>' for col in col_styles])}                  
                </colgroup>
                <thead>
                  <tr>{" ".join([f'<th>{col}</th>' for col in cols])}                    
                  </tr>
                </thead>
            """
    body = f"""<tbody>{"".join(["<tr>" + "".join([f"<td>{row[col] if col != code_col else wrap_code_in_wiki_macro(row[col])}</td>" for col in cols]) + "</tr>" for i, row in df.iterrows()])}</tbody></table></div>"""
    return header + body


def convert_columns_to_str(df: pd.DataFrame, str_columns: List[str] = None) -> pd.DataFrame:
    """
    Convert specified columns to string
    :param df: dataframe
    :param str_columns: list columns that need to be converted to string
    :return: dataframe with now specified columns converted to string
    """
    if not str_columns:
        str_columns = df.columns
    for col in str_columns:
        try:
            df[col] = df[col].fillna("")
            df[col] = df[col].apply(str)
        except Exception as e:
            logging.info(f"{e}")
            continue
    return df


def convert_columns_to_lowercase_and_nowhitespace(df: pd.DataFrame, join_char: str = ".") -> pd.DataFrame:
    """
    Remove punctuation marks from column names and convert column names to lowercase
    :param df:
    :param join_char:
    :return:
    """
    df.columns = df.columns.map(lambda col: f"{join_char}".join(re.findall(r"\w+", col)).lower())
    return df


def sort_columns_of_merged_dataframe(mrg_df, key_cols, cols, suffixes):
    """
    Sort columns of a merged dataframe so that we can compare column values from original dataframes easily
    :param mrg_df:
    :param key_cols:
    :param cols:
    :param suffixes:
    :return: merged dataframe with sorted columns
    """
    sorted_cols = []
    suffix_left, suffix_right = suffixes
    for col in cols:
        sorted_cols.append(col + suffix_left)
        sorted_cols.append(col + suffix_right)
    mrg_df = mrg_df[key_cols + sorted_cols]
    return mrg_df


import numpy as np


def create_new_key_from_two_cols_for_dataframe(df, col_one, col_two, new_key_name="new_key"):
    """
    Make a new key from two columns of a dataframe, which is a simple tuple with two elements
    :param df:
    :param col_one:
    :param col_two:
    :param new_key_name:
    :return:
    """
    df[new_key_name] = [(col_one, col_two) for col_one, col_two in zip(df[col_one].tolist(), df[col_two].tolist())]
    return df


def get_records_with_certain_criteria_from_dataframe(df, key_col, eval_col, criteria=np.max):
    """
    Extract records from dataframe with repeating values where we are interested in certain values only
    For instance cashflows dataframe where one cusip has cashflows for many dates, but we are interested only in the last payment dates for all cusips
    :param df:
    :param key_col:
    :param eval_col:
    :param criteria:
    :return:
    """
    df = create_new_key_from_two_cols_for_dataframe(df, key_col, eval_col)
    grp_df = df.groupby(key_col)[[eval_col]].agg(criteria)
    crit_df = pandas_multi_index_to_columns(grp_df)
    crit_df = create_new_key_from_two_cols_for_dataframe(crit_df, key_col, eval_col)
    target_df = df[df["new_key"].isin(crit_df["new_key"])]
    return target_df


def clean_up_multi_index_cols(mi_cols: List[Tuple[str, ...]]) -> List[Tuple[str, ...]]:
    """
    Remove empty strings from multi index columns
    :param mi_cols:
    :return:
    """
    cleaned_mi_cols = []
    for mi_col in mi_cols:
        cleaned_mi_cols.append(tuple([token for token in mi_col if token != ""]))
    return cleaned_mi_cols


def convert_multi_index_col_to_one_dim_col(df: pd.DataFrame, join_char: str = ".") -> pd.DataFrame:
    """
    Convert multi index column to one dimensional column
    :param df:
    :param join_char:
    :return:
    """
    mi_cols = df.columns
    mi_cols = clean_up_multi_index_cols(list(mi_cols))
    df.columns = [f"{join_char}".join(mi_col) for mi_col in mi_cols]
    return df


def write_dataframes_to_excel(sht: Dict[str, Tuple[pd.DataFrame, bool]], folder: pathlib.Path, filename: str):
    """
    write multiple dataframes into single excel file
    :param sht: Dictionary that maps sheet names to dataframe and whether to save with indices
    :param folder: folder to save into
    :param filename: filename to save with, must end with .xlsx
    :return: None
    """
    with pd.ExcelWriter(folder / filename, engine="openpyxl") as writer:
        for sheet_name, (df, save_index) in sht.items():
            df.to_excel(writer, sheet_name=sheet_name, index=save_index)
    logging.info(f"Finished writing {len(sht)} dataframes into {folder / filename}")


def convert_df_col_to_dicts(df: pd.DataFrame, col_name: str, sep: str = ";",
                            should_reverse: bool = False) -> pd.DataFrame:
    """
    Convert dataframe columns that has key,vals separated by character to a dictionary
    :param df: dataframe
    :param col_name: column that has text of key,val separated by character
    :param sep: separator character
    :param should_reverse: should we reverse list after separate by character
    :return: dataframe with the column now having dictionry instead of key,val text
    """
    df[col_name] = df[col_name].map(lambda col_text: col_text.split(sep))
    if should_reverse:
        df[col_name] = df[col_name].apply(reverse_list)
    df[col_name] = df[col_name].apply(construct_dict_from_list_of_key_values)
    return df


def get_distinct_keys_from_list_of_dicts(thedict_list: List[dict]):
    """
    Get distinct key names from a list of dictionaries
    :param thedict_list: list of dictionaries. most often we expect dictionaries to have similar keys
    :return: distinct list of keys used by dictionaries in the list
    """
    all_keys = []
    for thedictval in thedict_list:
        thekeys = list(thedictval.keys())
        all_keys += thekeys
    return list(set(all_keys))


def extract_dict_keys_to_columns(df: pd.DataFrame, col_name: str, remove_orig_col: bool = False,
                                 prefix: str = "") -> pd.DataFrame:
    """
    Extract keys of dictionaries to dataframe columns
    :param df: dataframe
    :param col_name: column that has dictionaries
    :param remove_orig_col: whether to remove original column after extracting its values to separate columns
    :return: dataframe now has new columns representing keys in dictionaries
    """
    all_keys = get_distinct_keys_from_list_of_dicts(df[col_name].tolist())
    logging.info(f"{col_name} contains {len(all_keys)} distinct keys")
    if prefix:
        added_col_names = [f"{prefix}_{col}" for col in all_keys]
    else:
        added_col_names = all_keys
    new_col_names = add_new_values_in_certain_item_location(df.columns.tolist(), col_name, added_col_names,
                                                            include_orig_item=not remove_orig_col)
    for new_col in all_keys:
        if prefix:
            new_col_name = f"{prefix}_{new_col}"
        else:
            new_col_name = new_col
        df[new_col_name] = df[col_name].map(lambda thedict: thedict[new_col] if new_col in thedict else "")
    return df[new_col_names]


def get_mask_for_matching_column_against_pattern(df: pd.DataFrame, col_name: str, one_pattern: re.Pattern):
    """
    Get True/False series by matching dataframe column values against a pattern
    :param df: dataframe
    :param col_name: column with string values
    :param one_pattern: pattern to match
    :return: mask with True/False values
    """
    return df[col_name].map(lambda col_val: True if re.match(one_pattern, col_val) else False)


def filter_df_records_matching_one_pattern(df: pd.DataFrame, col_name: str, one_pattern: re.Pattern):
    """
    Return dataframe records by matching column values against a pattern
    :param df: dataframe
    :param col_name: column that has string values
    :param one_pattern: regex pattern
    :return: filtered dataframe
    """
    return df[get_mask_for_matching_column_against_pattern(df, col_name, one_pattern)]


class LogicalOperator(IntEnum):
    OR = 0
    AND = 1


def filter_df_records_matching_text_patterns(df: pd.DataFrame, col_name: str,
                                             text_patterns: List[Union[str, re.Pattern]]) -> pd.DataFrame:
    """
    Return dataframe records by matching column values against a list of regex patterns.

    :param df: DataFrame
    :param col_name: Column name that contains string values.
    :param text_patterns: List of regex patterns or strings.
    :return: Filtered DataFrame
    """
    if not text_patterns:
        return df  # Return original df if no patterns provided

    # Create a combined boolean mask
    mask = df[col_name].astype(str).apply(lambda x: any(re.search(pattern, x.lower()) for pattern in text_patterns))
    return df[mask]


def list_of_dict_to_dataframe(records: List[Dict[Any, Any]], key_col_name: str=None, value_col_name: str=None)->pd.DataFrame:
    """
    Convert a list of dictionaries to dataframe
    A single dictionary has structure {key_col_name:key_col_val,value_col_name:value_col_val}
    :param records:
    :param key_col_name:
    :param value_col_name:
    :return:
    """
    if key_col_name is None or value_col_name is None:
        one_record=records[0]
        key_col_name,value_col_name=tuple(one_record.keys())
    record_dict = {}
    for item in records:
        record_dict[item[key_col_name]] = item[value_col_name]
    return pd.DataFrame([record_dict])


def print_df_header(df:pd.DataFrame, no_of_head_rows:int=5, cols:List[str]=None):
    """
    Print dataframe header
    :param df:
    :param no_of_head_rows: number of head rows to print
    :param cols:
    :return:
    """
    if cols is None:
        cols = df.columns.tolist()
    print(df[cols].head(no_of_head_rows).to_string())


def remove_nonnumeric_chars_from_numeric_cols(df:pd.DataFrame,nonnumeric_chars:List[str]=None, numeric_cols:List[str]=None)->pd.DataFrame:
    """
    remove non numeric chars from values of numeric cols to prepare them for conversion
    :param df: dataframe with numeric cols
    :param nonnumeric_chars: non numeric chars like comma
    :param numeric_cols: numeric column names
    :return:
    """
    if nonnumeric_chars is None:
        nonnumeric_chars=[","]
    if numeric_cols is None:
        numeric_cols=df.columns.tolist()
    for col in numeric_cols:
        for non_numeric_char in nonnumeric_chars:
            df[col]=df[col].fillna("").apply(str).map(lambda numeric_col : numeric_col.replace(non_numeric_char,""))
    return df