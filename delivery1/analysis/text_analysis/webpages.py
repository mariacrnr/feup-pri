import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar

path = "analysis/output/text_analysis/webpages/"

def import_refined_data(group):
    df = pd.read_json("data/refined/" + group + '_refined.json')
    return df

def save_dataframe_as_csv(df, table_name):
    df.to_csv(path + table_name + ".csv")

def pages_per_month(df):
    group_by_month = df['text'].groupby(by=[df['date'].dt.month])

    pages_per_month = group_by_month.count().reset_index()
    pages_per_month.rename({'date': 'Month', 'text': 'Number of Pages'}, axis='columns', inplace=True)
    pages_per_month['Month'] = pages_per_month['Month'].apply(lambda x: calendar.month_abbr[x])

    return pages_per_month

def plot_pages_per_month(df):
    fig, ax = plt.subplots(figsize=(30, 8))
    x_axis = np.arange(0,36,3)
    width = 0.7

    for x, y in enumerate(df[0]['Number of Pages'].tolist()):
        ax.annotate(y, (3 * x - 3*width/2, y), ha='center')
    for x, y in enumerate(df[1]['Number of Pages'].tolist()):
        ax.annotate(y, (3 * x - width/2, y), ha='center')
    for x, y in enumerate(df[2]['Number of Pages'].tolist()):
        ax.annotate(y, (3 * x + width/2, y), ha='center')
    for x, y in enumerate(df[3]['Number of Pages'].tolist()):
        ax.annotate(y, (3 * x + 3*width/2, y), ha='center')

    plt.bar(x_axis - 3*width/2, df[0]['Number of Pages'].tolist(), width, alpha=0.7, color= "darkred", label='PS')
    plt.bar(x_axis - width/2, df[1]['Number of Pages'].tolist(), width, alpha=0.7, color= "darkorange", label="PSD")
    plt.bar(x_axis + width/2, df[2]['Number of Pages'].tolist(), width, alpha=0.7, color= "darkblue", label="CHEGA")
    plt.bar(x_axis + 3*width/2, df[3]['Number of Pages'].tolist(), width, alpha=0.7, color= "lightblue", label="IL")

    plt.xticks(x_axis, df[0]['Month'].tolist())
    plt.legend(["PS", "PSD", "CHEGA", "IL"])
    plt.title('Number of Pages Per Month')
    plt.xlabel('Months 2017-2022')
    plt.ylabel('Number of Pages')

    fig.savefig(path + "/pages_per_month.pdf")

def pages_per_year(df, start, end):
    group_by_year = df['text'].groupby(by=[df['date'].dt.year])

    pages_through_time = group_by_year.count().reset_index()
    pages_through_time.rename({'date': 'Year', 'text': 'Number of Pages'}, axis='columns', inplace=True)

    pages_through_time = pages_through_time.merge(how='right', on=['Year'], right = pd.DataFrame({'Year':np.arange(start, end)})).sort_values(by=["Year"]).reset_index().fillna(int(0)).drop(['index'], axis=1)

    return pages_through_time

def plot_pages_per_year(df):
    fig, ax = plt.subplots(figsize=(30, 8))
    x_axis = np.arange(0,15,3)
    width = 0.7

    for x, y in enumerate(df[0]['Number of Pages'].tolist()):
        ax.annotate(y, (3 * x - 3*width/2, y), ha='center')
    for x, y in enumerate(df[1]['Number of Pages'].tolist()):
        ax.annotate(y, (3 * x - width/2, y), ha='center')
    for x, y in enumerate(df[2]['Number of Pages'].tolist()):
        ax.annotate(y, (3 * x + width/2, y), ha='center')
    for x, y in enumerate(df[3]['Number of Pages'].tolist()):
        ax.annotate(y, (3 * x + 3*width/2, y), ha='center')

    plt.bar(x_axis - 3*width/2, df[0]['Number of Pages'].tolist(), width, alpha=0.7, color= "darkred", label='PS')
    plt.bar(x_axis - width/2, df[1]['Number of Pages'].tolist(), width, alpha=0.7, color= "darkorange", label="PSD")
    plt.bar(x_axis + width/2, df[2]['Number of Pages'].tolist(), width, alpha=0.7, color= "darkblue", label="CHEGA")
    plt.bar(x_axis + 3*width/2, df[3]['Number of Pages'].tolist(), width, alpha=0.7, color= "lightblue", label="IL")

    plt.xticks(x_axis, df[0]['Year'].tolist())
    plt.legend(["PS", "PSD", "CHEGA", "IL"])
    plt.title('Number of Pages Per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Pages')

    fig.savefig(path + "/pages_per_year.pdf")

def pages_stats(df):
    pages_data = {'Avg Number of Pages': [df[0]['Number of Pages'].mean(), df[1]['Number of Pages'].mean(), df[2]['Number of Pages'].mean(), df[3]['Number of Pages'].mean()],
              'Min': [df[0]['Number of Pages'].min(), df[1]['Number of Pages'].min(), df[2]['Number of Pages'].min(), df[3]['Number of Pages'].min()],
              'Max': [df[0]['Number of Pages'].max(), df[1]['Number of Pages'].max(), df[2]['Number of Pages'].max(), df[3]['Number of Pages'].max()]}
    total_pages = pd.DataFrame(pages_data, ['PS', 'PSD', 'CH', 'IL'])

    save_dataframe_as_csv(total_pages, "total_pages_stats")

def run():
    political_parties = ['ps_merged', 'psd', 'ch', 'il']

    data_months = []
    data_years = []
    for group in political_parties:
        df = import_refined_data(group)

        pages_months = pages_per_month(df)
        data_months.append(pages_months)

        pages_years = pages_per_year(df, 2017, 2022)
        data_years.append(pages_years)

    plot_pages_per_month(data_months)
    plot_pages_per_year(data_years)

    pages_stats(data_years)

run()