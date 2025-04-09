import pathlib
import re
import logging
from typing import List
from collections import Counter
from sampytools.configdict import ConfigDict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize
import logging

from sampytools.list_utils import get_list_diff, get_unique_records_from_list, get_intersection


def split_text_by_certain_substring_and_save(long_text, split_str, filepath: pathlib.Path):
    lines = long_text.split(split_str)
    filepath.write_text("\n\n".join(lines))
    for line in lines:
        print(line)
        print("\n\n")
    return lines


def join_lines_with_keyword(keyword: str, lines: List[str]):
    return f"{keyword}".join(lines)


def join_list_to_line(alist: List[str], join_char="\t"):
    """
    Join list of strings to a single line with specified join character
    :param alist:
    :param join_char:
    :return:
    """
    return f"{join_char}".join(alist)


def generate_tab_delimited_line_from_list(alist: List[str]):
    """
    Join list of strings to a single line with tab character
    :param alist: list of strings
    :return: string of tab delimited line
    """
    return join_list_to_line(alist, "\t")


def format_sql_query(sql_keywords, query):
    for keyword in sql_keywords:
        lines = re.split(keyword, query)
        query = join_lines_with_keyword(f"\n{keyword}\n\t", lines)
    return query


def extract_subtext_from_big_text(big_text_lines, line_one, line_two):
    start_idx = big_text_lines.index(line_one)
    end_idx = big_text_lines.index(line_two)
    return big_text_lines[start_idx:end_idx + 1]


def extract_lines_that_match_pattern(lines: List[str], thepattern, match_value: str) -> List[str]:
    """
    Extract lines matching certain pattern from list of lines
    """
    filtered_lines = [line for line in lines if re.search(thepattern, line).group() == match_value]
    return filtered_lines


def save_lines_to_file(file: pathlib.Path, lines: List):
    file.write_text("\n".join(lines))
    logging.info(f"Saved {len(lines)} lines to {file}")


def combine_lines_to_string(lines, join_char="\n"):
    return f"{join_char}".join(lines)


def extract_switches_values(text):
    """
    why are we wrapping the part before \\s+ in parantheses
    The parentheses are used to define a capturing group in the regular expression. A capturing group captures the text matched by the group for later use, such as extracting it as a separate item from the match.
    In this case, the first capturing group (-[a-zA-Z]+) matches the switch, which begins with a hyphen and is followed by one or more letters. The second capturing group (\S+) matches the value that follows the switch, which is one or more non-whitespace characters.
    By wrapping each of these parts in a capturing group, we can extract both the switch and its value as separate items from each match. The re.findall function returns a list of all matches, where each match is a tuple of the capturing groups' values in the order they are defined in the pattern.
    Therefore, switch_value_regex.findall(text) returns a list of tuples, where each tuple contains the switch and its value, which we can then convert to a dictionary using dict for easier access.
    :param text:
    :return:
    """
    switch_value_regex = re.compile(r'(-[a-zA-Z]+)\s+(\S+)')
    switches_values = switch_value_regex.findall(text)
    return dict(switches_values)


def remove_duplicate_lines_in_text(original_file: pathlib.Path, refined_filename: str = None, save_results=True):
    """
    Remove duplicate lines in the file and save it to the same folder with new filename
    :param original_file:
    :param refined_filename:
    :param save_results:
    :return:
    """
    log_folder = original_file.parent
    if not refined_filename:
        refined_filename = original_file.stem + "_refined" + original_file.suffix
    txt = original_file.read_text()
    lines = txt.split("\n")
    cnt = Counter(lines)
    new_file = log_folder / refined_filename
    new_file.write_text("\n".join(cnt.keys()))
    logging.info(f"reduced number of lines in {original_file} from {len(lines)} to {len(cnt)}")
    return ConfigDict({"new_file": new_file, "newtxtcnt": cnt})


def get_sorted_non_zero_words_and_freqs_from_csr_mat_row(csr_matrix_row, tfidf_features):
    """
    csr_matrix which is the result of transforming messages into word frquencies by TfidfVectorizer
    has zeros across many columns and non-zero values only for limited columns where the message
    actually contained that token. We want to get non-zero columns and values which represent token and word frequency
    Finally we want to sort these tokens by their word frequency
    :param csr_matrix_row:
    :param tfidf_features:
    :return:
    """
    items = [(w, csr_matrix_row[0, idx]) for idx, w in enumerate(tfidf_features) if csr_matrix_row[0, idx] > 0]
    items = sorted(items, key=lambda item: item[-1])
    return items


def get_common_common_part_of_message_across_documents(message, tokenizer, csr_matrix_row, tfidf_features,
                                                       throw_off_thresh=1):
    """
    We are assuming a use case where we have lots of similar messages that differ only by one or two words
    We want this function to return common part across these similar messages
    :param message:
    :param tokenizer:
    :param csr_matrix_row:
    :param tfidf_features:
    :param throw_off_thresh:
    :return:
    """
    tokens = tokenizer(message)
    words_and_freqs = get_sorted_non_zero_words_and_freqs_from_csr_mat_row(csr_matrix_row, tfidf_features)
    words_and_freqs = sorted(words_and_freqs, key=lambda item: item[-1])
    words_and_freqs = words_and_freqs[:-1 * throw_off_thresh]
    words = [word for (word, freq) in words_and_freqs]
    return " ".join([token for token in tokens if token.lower() in words])


def get_message_clusters(messages, n_components=7):
    """
    We are trying to categorize a list of messages into clusters
    To achieve this we first convert all messages to word frequency sparce matrix via TfidfVectorizer
    Then we reduce csr_matrix dimension to n_components principal components with NMF (Non-negative Factorizing Model)
    Finally we compute similarities between messages taking dot products and assign a cluster label to each message based on that calculation
    :param messages:
    :param n_components:
    :return:
    """
    # TfidfVectorizer trains on our messages and transforms them to a sparse matrix
    tfidf = TfidfVectorizer()
    csr_mat = tfidf.fit_transform(messages)

    # initialize tokenizer for later usage
    tokenizer = tfidf.build_tokenizer()

    logging.info(f"sparce matrix shape : {csr_mat.shape}")

    # tfidf features (tokens) across all messages
    tfidf_features = tfidf.get_feature_names()
    logging.info(f"there are total of {len(tfidf_features)} tfidf features for specified messages")

    # NMF to reduce csr_matr dimensionality to principal components
    nmf = NMF(n_components=n_components)
    nmf_features = nmf.fit_transform(csr_mat)

    # normalize nmf features
    norm_nmf_features = normalize(nmf_features)

    # initial a dictionary to hold messages and their mapped cluster
    clustered_messages = {}

    for idx, message in enumerate(messages):
        if message not in clustered_messages:
            essential_part = get_common_common_part_of_message_across_documents(message, tokenizer, csr_mat[idx],
                                                                                tfidf_features, 1)
            similarities = norm_nmf_features.dot(norm_nmf_features[idx, :])
            for msg_idx, similarity in enumerate(similarities):
                if similarity > 0.9:
                    clustered_messages[messages[msg_idx]] = essential_part

    logging.info(
        f"total of {len(clustered_messages)} distinct messages were mapped to {len(set(clustered_messages.values()))} distinct clusters")
    return ConfigDict({'clustered_messages': clustered_messages, 'tfidf': tfidf, 'tfidf_features': tfidf_features,
                       'tokenizer': tokenizer, 'nmf_feature': nmf_features})


def compare_two_files(file_one: pathlib.Path, file_two: pathlib.Path) -> ConfigDict:
    """
    Compare two files and return the lines that are different
    :param file_one:
    :param file_two:
    :return: differences between two files as config dict
    """
    file_one_lines = get_unique_records_from_list(file_one.read_text().split("\n"))
    file_two_lines = get_unique_records_from_list(file_two.read_text().split("\n"))
    file1_vs_file2 = get_list_diff(file_one_lines, file_two_lines)
    logging.info(f"{file_one.name} vs {file_two.name} diff : {len(file1_vs_file2)} lines")
    file2_vs_file1 = get_list_diff(file_two_lines, file_one_lines)
    logging.info(f"{file_two.name} vs {file_one.name} diff : {len(file2_vs_file1)} lines")
    file1_file2_intersection = get_intersection(file_one_lines, file_two_lines)
    logging.info(f"{file_one.name} and {file_two.name} intersection : {len(file1_file2_intersection)} lines")
    return ConfigDict(
        {"file1_vs_file2": file1_vs_file2, "file2_vs_file1": file2_vs_file1, "file1_lines": file_one_lines,
         "file2_lines": file_two_lines, "intersection": file1_file2_intersection})


def get_delimited_records_from_file(afile: pathlib.Path, delimiter: str = "\t", encoding="utf-8") -> List[List[str]]:
    """
    Get delimited records from a file with lines that are delimited by some character like tab
    :param afile: filepath
    :param delimiter: delimiter character
    :param encoding:
    :return: list of lists
    """
    text = afile.read_text(encoding=encoding)
    lines = [line for line in text.split("\n") if line != ""]
    return [line.strip().split(delimiter) for line in lines]


def remove_items_with_certain_val_from_list(alist: List[str], string_to_remove: str = "") -> List[str]:
    """
    Remove items with certain value from list
    :param alist: list of strings
    :param string_to_remove: string to remove
    :return: list of strings
    """
    return [item for item in alist if item != string_to_remove]
