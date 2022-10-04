import requests
import json
from calendar import monthrange


def get_estimated_number_results(website, date):
    request = requests.get("https://arquivo.pt/textsearch?q=&siteSearch=" + website + "&from="+ str(date))
    data = json.loads(request.content)
    estimated_nr_results = data["estimated_nr_results"]
    return estimated_nr_results
    
def number_of_days_in_month(year:int, month:int):
    return monthrange(year, month)[1]

def request_and_save(request_string,file_name):

    f = open(file_name, "w")
    request = requests.get(request_string)
    data = json.loads(request.content)
    jsonData = []

    for item in data["response_items"]:
        next_request = requests.get(item["linkToExtractedText"])
        #print("1 item")
        text = next_request.content.decode("UTF-8",'replace')

        jsonData.append({"date": item["date"], "link": item["linkToArchive"], "contentLength": len(text), "text": text})

def start_data_requests(start_year, end_year, website, file_name):

    f = open(file_name, "w")
    f.close()
    jsonData = []

    for j in range(end_year-start_year):
        year_str=str(start_year+j)
        for i in range(12):
            month_str=("0"+str(i+1)) if i<9 else str(i+1)

            start_date=str(year_str)+str(month_str)+"01"+"000000"
            end_date=str(year_str)+str(month_str)+str(number_of_days_in_month(start_year+j,i+1))+"000000"

            request = requests.get("https://arquivo.pt/textsearch?q=&siteSearch=" + website + "&from="+ start_date+ "&to="+ end_date + "&dedupValue=10&maxItems=10")
            print("Start date: "+start_date)
            print("End date: "+ end_date)

            data = json.loads(request.content)

            for item in data["response_items"]:
                next_request = requests.get(item["linkToExtractedText"])
                #print("1 item")
                text = next_request.content.decode("UTF-8",'replace')

                jsonData.append({"date": item["date"], "link": item["linkToArchive"], "contentLength": len(text), "text": text})
                
    f.write(json.dumps(jsonData, indent=4, ensure_ascii=False))
            


#political_parties = {"ps.pt": 1999, "www.psd.pt": 1996, "partidochega.pt": 2019 , "iniciativaliberal.pt": 2017 , "pcp.pt": 1996, "www.bloco.org": 2005, "www.pan.com.pt": 2013, "partidolivre.pt": 2018}

start_data_requests(1999, 2001, "www.ps.pt","ps.json")