import requests
from time import sleep
import pandas as pd
import json
import re
import urllib.parse

def retrieve_date(url):
    result = re.search(r"(wayback\/)(\d+)(?:\/)", url)
    return result.group(2)

def retrieve_link(url):
    result = re.search(r"(wayback\/)(\d+)(\/)(.*)", url)
    return result.group(4)

def retrieve_title(arquivo_url):
    link=retrieve_link(arquivo_url)
    date=retrieve_date(arquivo_url)
    link=urllib.parse.quote_plus(link)
    url="https://arquivo.pt/textsearch?metadata="+link+"/"+date
    request = requests.get(url)
    while(request.status_code!=200):
        print("Too many requests")
        if(request.status_code==429):
            sleep(60)
            request = requests.get(url)
        else:
            print("Request error: "+str(request.status_code))
            return ''
   
    title_data = json.loads(request.content)
    if(len(title_data['response_items'])>0):
        title = title_data['response_items'][0]['title']
        return title
    return ''


def add_title_field(data):
    data['title'] = data['link'].apply(retrieve_title)

    
    

def import_data(group):
    df = pd.read_json("../data/" + group + '.json')
    return df

def save_data(group, df):
    json_data=df.to_json(orient='records')
    parsed = json.loads(json_data)
    f = open('../data/after_processing/'+ group + '.json', "w",encoding="UTF-8")
    json.dump(parsed, fp=f,indent=4, ensure_ascii=False)

def run():
    parties = ['il']

    for party in parties:
        print(party)
        data = import_data(party)
        add_title_field(data)
        save_data(party,data)


run()