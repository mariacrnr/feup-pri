import pandas as pd
import numpy as np

def import_clean_data(group):
    df = pd.read_json("data/clean/" + group + '_clean.json')
    return df

def save_refined_data(group, df):
    df = df.to_json(r'data/refined/'+ group + '_refined.json', orient='records')

def remove_empty_text(df):
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df.dropna()
    return df

def remove_duplicate_text(df):
    df.drop_duplicates(subset=['text'],
                     keep='last', inplace=True)
    return df

def run():
    political_parties = ['ps_merged', 'psd', 'ch', 'il']

    for group in political_parties:
        df = import_clean_data(group)
        df = remove_empty_text(df)
        df = remove_duplicate_text(df)

        save_refined_data(group, df)

run()
