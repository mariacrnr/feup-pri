import pandas as pd
import numpy as np
import dataframe_image as dfi
import calendar

path = "analysis/output/text_analysis/length/"

def import_refined_data(group):
    df = pd.read_json("data/refined/" + group + '_refined.json')
    return df

def save_dataframe_as_png(df, table_name):
    df_styled = df.style.background_gradient()
    dfi.export(df_styled, path + table_name + ".png")

def length_stats_per_month(df):
    group_by_month = df['text'].groupby(by=[df['date'].dt.month])

    avg_text_lenght_per_month = group_by_month.apply(lambda x: np.mean(x.str.len())).rename('Average')
    min_text_lenght_per_month = group_by_month.apply(lambda x: np.min(x.str.len())).rename('Min')
    max_text_lenght_per_month = group_by_month.apply(lambda x: np.max(x.str.len())).rename('Max')
    std_text_lenght_per_month = group_by_month.apply(lambda x: np.std(x.str.len())).rename('Std')

    text_length_per_month = pd.concat([avg_text_lenght_per_month, min_text_lenght_per_month, max_text_lenght_per_month, std_text_lenght_per_month], axis=1).reset_index()
    text_length_per_month.rename({'date': 'Month'}, axis='columns', inplace=True)
    text_length_per_month['Month'] = text_length_per_month['Month'].apply(lambda x: calendar.month_abbr[x])
    
    return text_length_per_month

def length_stats_per_year(df):
    group_by_year = df['text'].groupby(by=[df['date'].dt.year])

    avg_text_lenght_per_year = group_by_year.apply(lambda x: np.mean(x.str.len())).rename('Average')
    min_text_lenght_per_year = group_by_year.apply(lambda x: np.min(x.str.len())).rename('Min')
    max_text_lenght_per_year = group_by_year.apply(lambda x: np.max(x.str.len())).rename('Max')
    std_text_lenght_per_year = group_by_year.apply(lambda x: np.std(x.str.len())).rename('Std')

    text_length_per_year = pd.concat([avg_text_lenght_per_year, min_text_lenght_per_year, max_text_lenght_per_year, std_text_lenght_per_year], axis=1).reset_index()
    text_length_per_year.rename({'date': 'Year'}, axis='columns', inplace=True)
    
    return text_length_per_year

def total_length_stats(df):
    length_data = {'Avg Length': [df[0]['Average'].mean(), df[1]['Average'].mean(), df[2]['Average'].mean(), df[3]['Average'].mean()],
                'Min': [df[0]['Min'].min(), df[1]['Min'].min(), df[2]['Min'].min(), df[3]['Min'].min()],
                'Max': [df[0]['Max'].max(), df[1]['Max'].max(), df[2]['Max'].max(), df[3]['Max'].max()]}
    total_length = pd.DataFrame(length_data, ['PS', 'PSD', 'CH', 'IL'])

    save_dataframe_as_png(total_length, "total_pages_stats")


def run():
    political_parties = ['ps_merged', 'psd', 'ch', 'il']

    data_months = []
    data_years = []
    for group in political_parties:
        df = import_refined_data(group)

        length_months = length_stats_per_month(df)
        data_months.append(length_months)

        length_years = length_stats_per_year(df)
        data_years.append(length_years)

    total_length_stats(data_years)

run()