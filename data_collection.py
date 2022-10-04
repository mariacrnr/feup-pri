import requests
import json
from calendar import monthrange
from threading import Thread
from os import mkdir, remove


def get_estimated_number_results(website, date):
    request = requests.get("https://arquivo.pt/textsearch?q=&siteSearch=" + website + "&from="+ str(date))
    data = json.loads(request.content)
    estimated_nr_results = data["estimated_nr_results"]
    return estimated_nr_results
    
def number_of_days_in_month(year:int, month:int):
    return monthrange(year, month)[1]

def request_and_save(request_string,file_name):

    request = requests.get(request_string)
    data = json.loads(request.content)
    jsonData = []
    if "response_items" in data:
        for item in data["response_items"]:
            next_request = requests.get(item["linkToExtractedText"])
            text = next_request.content.decode("UTF-8",'replace')
            jsonData.append({"date": item["date"], "link": item["linkToArchive"], "contentLength": len(text), "text": text})
    if(len(jsonData)>0):
        f = open(file_name+".json", "w")
        json.dump(jsonData, fp=f,indent=4, ensure_ascii=False)
        f.close()

def retrieve_data(start_year, end_year, website,output_file_name):

    t_list=[]
    f_list=[]

    for j in range(end_year-start_year):
        year_str=str(start_year+j)
        for i in range(12):
            month_str=("0"+str(i+1)) if i<9 else str(i+1)

            start_date=str(year_str)+str(month_str)+"01"+"000000"
            end_date=str(year_str)+str(month_str)+str(number_of_days_in_month(start_year+j,i+1))+"000000"

            request_string = "https://arquivo.pt/textsearch?q=&siteSearch=" + website + "&from="+ start_date+ "&to="+ end_date + "&dedupValue=2000&maxItems=2000"
            thread_file_name=start_date+end_date
            f_list.append(thread_file_name)
            t = Thread(target=request_and_save,args=(request_string,thread_file_name))
            # maybe fazer thread pool?
            t_list.append(t)
            t.start()
        for t in t_list:
            t.join()
        
    combine_files(f_list,output_file_name)

                
    # f.write(json.dumps(jsonData, indent=4, ensure_ascii=False))
            
def combine_files(file_list,output_file_name):
    
    f = open(output_file_name+".json", "w")

    for f1 in file_list:
        try:
            with open(f1+".json", 'r') as infile:
                json.dump(json.load(infile), fp=f,indent=4, ensure_ascii=False)
            remove(f1+".json")
        except FileNotFoundError:
            continue



#political_parties = {"ps.pt": 1999, "www.psd.pt": 1996, "partidochega.pt": 2019 , "iniciativaliberal.pt": 2017 , "pcp.pt": 1996, "www.bloco.org": 2005, "www.pan.com.pt": 2013, "partidolivre.pt": 2018}

retrieve_data(1999, 2001, "www.ps.pt","ps")