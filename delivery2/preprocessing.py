import pandas as pd

def import_data(group):
    df = pd.read_json("data/" + group + '.json')
    return df

def add_title_field(data):
    # removes the last backlash from the links that have it
    data['title'] = data['link'].apply(lambda x: x[:-1] if x[-1] == '/' else x)

    # gets only the text after the last backlash
    data['title'] = data['title'].str.rsplit(pat='/', n=1).str[-1]

    # replaces '-' dividors with empty space
    data['title'] = data['title'].str.replace('-', ' ')

def add_party_field(party, data):
    data['party'] = party.upper()

def save_data(group, df):
    df = df.to_json(r'data/'+ group + '.json', orient='records')

def run():
    parties = ['ps', 'psd', 'chega', 'pcp', 'bloco', 'il', 'pan', 'livre']

    for party in parties:
        print(party)
        data = import_data(party)
        add_title_field(data)
        add_party_field(party, data)
        save_data(party, data)
        
run()