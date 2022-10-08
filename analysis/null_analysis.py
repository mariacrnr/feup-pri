import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataframe_image as dfi
import os

path = "analysis/output/null_analysis/"

def import_clean_data(group):
    df = pd.read_json("data/clean/" + group + '_clean.json')
    return df

def save_dataframe_as_png(df, table_name):
    df_styled = df.style.background_gradient()
    dfi.export(df_styled, path + table_name + ".png")

def replace_empty_with_nulls(df):
    return df.replace(r'^\s*$', np.nan, regex=True)

def total_missing_data(df, group):
    total = df.isnull().sum()
    percent = df.isnull().sum()/df.isnull().count()*100.0
    missing_data = pd.concat([total, percent], axis=1, keys=['Number', 'Percent'])

    save_dataframe_as_png(missing_data, group + '/total_missing_data_' + group)

def missing_data_per_group(df, group):
    total_values_per_type = df['type'].value_counts()
    missing_values_per_type = df.loc[df['text'].isnull(), 'type'].value_counts()
    percent = (missing_values_per_type / total_values_per_type) * 100
    missing_values = pd.concat([missing_values_per_type, total_values_per_type, percent], axis=1, keys=['Missing Text', 'Total', 'Percent']).fillna(0)

    save_dataframe_as_png(missing_values, group + '/missing_data_' + group)

    return missing_values


def plot_missing_data_per_type(df, missing_values, group):
    labels = missing_values.index.to_list()

    fig,ax = plt.subplots(figsize=(15, 15))
    for i in range(len(labels)):
        plt.bar(labels[i], missing_values['Total'][i], alpha=0.25, color= "blue")
        plt.bar(labels[i], missing_values['Missing Text'][i], color= "darkblue")

    plt.title('Missing Text Per Website Type')
    plt.legend(labels = ["Total", "Missing Text"])
    plt.xlabel('Types')
    plt.ylabel('Number of Pages')
    fig.autofmt_xdate()

    fig.savefig("analysis/output/null_analysis/" + group + "/missing_text_per_type_" + group + ".png", dpi=1000)

def run(group):
    os.makedirs(path + group, exist_ok=True)
    df = import_clean_data(group)
    df = replace_empty_with_nulls(df)
    total_missing_data(df, group)
    missing_values = missing_data_per_group(df, group)
    plot_missing_data_per_type(df, missing_values, group)


def run_all():
    political_parties = ['ps_merged', 'psd', 'ch', 'il']
    for group in political_parties:
        run(group)

run_all()

