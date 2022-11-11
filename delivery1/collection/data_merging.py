import pandas as pd

path = "data/raw/"

def combine_data(files):
    data = []
    for file in files:
        file_data = pd.read_json(file) 
        data.append(file_data)

    combined_data = pd.concat(data)

    return combined_data

def get_parties_data():

    ps = ["data/raw/ps1.json", "data/raw/ps2.json"]
    psd = ["data/raw/psd1.json", "data/raw/psd2.json", "data/raw/psd3.json"]
    pcp = ["data/refined/pcp1.json", "data/refined/pcp2.json", "data/refined/pcp3.json", "data/refined/pcp4.json"]
    livre = ["data/raw/livre1.json", "data/raw/livre2.json"]
    bloco = ["data/raw/bloco1.json", "data/raw/bloco2.json"]

    parties = {"ps": ps, "psd": psd, "pcp": pcp, "livre": livre, "bloco": bloco}

    return parties


def run():

    parties = get_parties_data()

    for party in parties:
        combined_data = combine_data(parties[party])
        path = 'data/raw/' + party + '.json'
        combined_data.to_json(path, orient='records')

run()