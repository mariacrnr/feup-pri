import pandas as pd
import datetime
import numpy as np

def import_data(group):
    df = pd.read_json("data/" + group + '.json')
    df['date']=df['date'].astype(np.int64) // 10**9
    return df

def add_title_field(data):
    # removes the last backlash from the links that have it
    data['title'] = data['link'].apply(lambda x: x[:-1] if x[-1] == '/' else x)

    # gets only the text after the last backlash
    data['title'] = data['title'].str.rsplit(pat='/', n=1).str[-1]

    # replaces '-' dividors with empty space
    data['title'] = data['title'].str.replace('-', ' ')
    
def change_date_field(data):
    # removes the last backlash from the links that have it
    data['date'] = data['date'].apply(lambda x: datetime.datetime.fromtimestamp(x).isoformat())



def add_party_field(party, data):
    data['party'] = party.upper()

def save_data(group, df):
    df = df.to_json(r'data/'+ group + '.json', orient='records')
    
def create_random_sample():
    parties = ['bloco','chega','il','livre','pan','pcp','ps','psd']

    final_data=pd.DataFrame()
    for party in parties:
        data = import_data(party)
        final_data = pd.concat([final_data, data.sample(n=200,random_state=0)], ignore_index=True)
        del data
    save_data('sample', final_data)
    
         
        
        

def run():
    parties = ['bloco','chega','il','livre','pan','pcp','ps','psd']

    for party in parties:
        print(party)
        data = import_data(party)
        change_date_field(data)
        add_title_field(data)
        add_party_field(party, data)
        save_data(party, data)
        del data 
               
               
create_random_sample()