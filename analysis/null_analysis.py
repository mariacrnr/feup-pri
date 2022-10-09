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

def total_missing_data(df, group, missing_data):
    total = df.isnull().sum()
    percent = df.isnull().sum()/df.isnull().count()*100.0
    total_missing = pd.concat([total, percent], axis=1, keys=['Number', 'Percent'])

    save_dataframe_as_png(total_missing, group + '/total_missing_data_' + group)

    total_missing = total_missing.loc[['text']]

    missing_data[0].append(total_missing.iloc[0]['Number'])
    missing_data[1].append(total_missing.iloc[0]['Percent'])

    return missing_data

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

    fig.savefig(path + group + "/missing_text_per_type_" + group + ".png", dpi=72)

def missing_data_all_parties(missing_data):
    total_missing = {'Missing Data': missing_data[0], 'Percentage': missing_data[1]}
    total_missing = pd.DataFrame(total_missing, ['PS', 'PSD', 'CH', 'IL'])

    save_dataframe_as_png(total_missing, 'total_missing_data')

def run(group):
    os.makedirs(path + group, exist_ok=True)
    df = import_clean_data(group)
    df = replace_empty_with_nulls(df)
    total_missing_data(df, group)
    missing_values = missing_data_per_group(df, group)
    plot_missing_data_per_type(df, missing_values, group)


def run():
    political_parties = ['ps_merged', 'psd', 'ch', 'il']

    missing_data = [[],[]]
    for group in political_parties:
        os.makedirs(path + group, exist_ok=True)

        df = import_clean_data(group)
        df = replace_empty_with_nulls(df)

        missing_data = total_missing_data(df, group, missing_data)

        missing_values = missing_data_per_group(df, group)
        plot_missing_data_per_type(df, missing_values, group)

    missing_data_all_parties(missing_data)
    

run()

