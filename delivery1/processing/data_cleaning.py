import pandas as pd

def import_raw_data(group):
    df = pd.read_json("data/raw/" + group + '.json')
    return df

def save_cleaned_data(group, df):
    df = df.to_json(r'data/clean/'+ group + '_clean.json', orient='records')

def removing_unrecognized_characters(df):
    df["text"]=pd.Series(df['text'], dtype="string")

    df["text"]=df["text"].str.replace("[\n\t\r]","",regex=True)
    df["text"]=df["text"].str.replace(" +"," ",regex=True)

    return df

def run():
    political_parties = ['ps_merged', 'psd', 'ch', 'il']

    for group in political_parties:
        df = import_raw_data(group)
        df = removing_unrecognized_characters(df)
        save_cleaned_data(group, df)


run()

