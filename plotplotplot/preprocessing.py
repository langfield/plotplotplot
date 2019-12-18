""" DATA PREPROCESSING. """
from typing import List, Tuple
import pandas as pd  # type: ignore


def read_csv(file_path: str) -> Tuple[List[pd.DataFrame], List[str], List[int]]:
    """ Read in a csv file to a list of dataframes. """

    print("Reading from file:", file_path)
    df = pd.read_csv(file_path)
    keys = list(df.columns)
    dfs = []

    column_counts = []
    i = 0
    for i, _key in enumerate(keys):
        column_counts.append(1)

    # Iterate over column split, and create a seperate DataFrame for
    # each subplot. Add the subplot names to `y_labels`.
    y_labels = []
    for i, count in enumerate(column_counts):
        key_list = []
        if count == 1:
            y_labels.append(keys[i])
            key_list.append(keys[i])
            dfs.append(df[key_list])
        else:
            words = []
            for j in range(count):
                words.append(keys[i + j])
                words.append("/")
                key_list.append(keys[i + j])
            y_labels.append("".join(words[:-1]))
            dfs.append(df[key_list])
    print("Generating", len(dfs), "subplots.")

    return dfs, y_labels, column_counts
