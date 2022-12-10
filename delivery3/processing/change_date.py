import pandas as pd
import datetime
import json
import numpy as np

def import_data(group):
    df = pd.read_json("../solr/data/" + group + '.json')
    df['date']=df['date'].astype(np.int64) // 10**9
    return df
    
def change_date_field(data):
    data['date'] = data['date'].apply(lambda x: datetime.datetime.fromtimestamp(x).isoformat())

def save_data(group, df):
    df = df.to_json(r'../solr/data/dates/'+ group + '.json', orient='records')
    

def combine_data(files):
    data = []
    for file in files:
        file_data = pd.read_json(file) 
        data.append(file_data)

    combined_data = pd.concat(data)

    return combined_data

def run():
    parties = ['bloco','chega','il','livre','pan','pcp','ps','psd']

    for party in parties:
        print(party)
        data = import_data(party)
        change_date_field(data)
        save_data(party, data)
        del data 

run()

# p = combine_data(['../solr/data/dates/pcp1.json','../solr/data/dates/pcp2.json','../solr/data/dates/pcp3.json'])
# save_data("pcp", p)