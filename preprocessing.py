import json

import numpy as np
import pandas as pd

#DATA PREPROCESSING

def read_csv(file_path):
 
    print("Reading from file:", file_path)

    df = pd.read_csv(file_path)
    print(df)
    keys = list(df.columns)
    dfs = []

    column_counts = []
    i = 0
    for i in range(len(keys)):
        key = keys[i]
        column_counts.append(1)
        i += 1

    # Iterate over column split, and create a seperate DataFrame for 
    # each subplot. Add the subplot names to `ylabels`. 
    ylabel = ""
    ylabels = []
    for i,count in enumerate(column_counts):
        key_list = []
        if count == 1:
            ylabels.append(keys[i])
            key_list.append(keys[i])
            dfs.append(df[key_list])
        else:
            words = []
            for j in range(count):
                words.append(keys[i + j])
                words.append("/")
                key_list.append(keys[i + j])
            ylabels.append("".join(words[:-1]))
            dfs.append(df[key_list])
    print("Generating", len(dfs), "subplots.")
    
    return dfs, ylabels, column_counts

def read_json(file_path, phase):

    phases = ['train', 'validate', 'test']
    assert phase in phases
    
    print("Reading from file:", file_path)
    def isfloat(x):
        try:
            a = float(x)
        except ValueError:
            return False
        else:
            return True

    def isint(x):
        try:
            a = float(x)
            b = int(a)
        except ValueError:
            return False
        else:
            return a == b

    with open(file_path, encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        
        phase_key = phase + "Results"

        row_list = []
        log_list = json_data[phase_key]

        # Construct train array. 
        for i, stepdict in enumerate(log_list):
            row = []
            for key, val in stepdict.items():
                if isint(val):
                    row.append(int(val))
                elif isfloat(val):
                    row.append(float(val))
                else:
                    row.append(val)
            row_list.append(row) 

        log_df = pd.DataFrame(log_list)
        keys = list(log_df.columns)
        log_df['index'] = log_df.index
        log_df['index'] = log_df['index'].apply(lambda x: x*10)
       
    dfs = []

    # This column_counts generation process assumes 
    # `top5` always follows `top1` in keys. 
    column_counts = []
    i = 0
    for i in range(len(keys)):
        key = keys[i]
        if key == 'top1':
            column_counts.append(2)
        elif key != 'top5':
            column_counts.append(1)
        i += 1

    # Iterate over column split, and create a seperate DataFrame for 
    # each subplot. Add the subplot names to `ylabels`. 
    ylabel = ""
    ylabels = []
    for i,count in enumerate(column_counts):
        key_list = ['index']
        if count == 1:
            ylabels.append(keys[i])
            key_list.append(keys[i])
            dfs.append(log_df[key_list])
        else:
            words = []
            for j in range(count):
                words.append(keys[i + j])
                words.append("/")
                key_list.append(keys[i + j])
            ylabels.append("".join(words[:-1]))
            dfs.append(log_df[key_list])
    print("Generating", len(dfs), "subplots.")
    
    return dfs, ylabels, column_counts
