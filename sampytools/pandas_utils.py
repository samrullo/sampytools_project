import pandas as pd
import logging
import re
from typing import List, Tuple


def make_column_names_unique(df: pd.DataFrame):
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

    return append_index_to_duplicate_columns(duplicate_cols_dict, cols)


def strip_string_columns(df, string_columns):
    for col in string_columns:
        df[col] = df[col].fillna("")
        df[col] = df[col].apply(str.strip)
    return df


def strip_trailing_and_leading_spaces_from_dataframe(df):
    for col in df.columns:
        try:
            df[col] = df[col].fillna("")
            df[col] = df[col].apply(str.strip)
            df[col] = df[col].apply(str.lstrip)
        except Exception as e:
            logging.info(f"strip_trailing_and_leading_spaces_from_dataframe error on col {col}: {e}")
            continue
    return df


def convert_columns_to_numeric(df, numeric_columns):
    for col in numeric_columns:
        df[col] = df[col].fillna(0)
        df[col] = pd.to_numeric(df[col])
    return df


def diff_df_maker(df, cols: list, diff_cols: list, index, suffixes=('_x', '_y')):
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


def order_merged_dataframe_cols(mrg_df, index_col, mrg_cols, suffixes):
    """
    Order columns of the merged dataframe so that relevant columns appear side by side
    :param mrg_df:
    :param index_col:
    :param mrg_cols:
    :param suffixes:
    :return:
    """
    suffix_x, suffix_y = suffixes
    ordered_cols = [index_col]
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


def pandas_series_multi_index_to_columns(agg_series: pd.Series, series_col_name="count"):
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


def convert_columns_to_str(df, str_columns=None):
    """
    Convert specified columns to string
    :param df:
    :param str_columns:
    :return:
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
