import pandas as pd

def combine_data(file1, file2):
    data1 = pd.read_json(file1)
    data2 = pd.read_json(file2)

    combined_data = pd.concat([data1, data2])

    return combined_data

def run():
    combined_data = combine_data("data/raw/ps.json", "data/raw/ps_www.json")
    combined_data.to_json(r'data/raw/ps_merged.json', orient='records')

run()