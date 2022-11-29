from time import sleep
import requests
import json
from calendar import monthrange


def number_of_days_in_month(year:int, month:int):
    return monthrange(year, month)[1]


def retrieve_data(start_year, end_year, website, output_file_name):

    f = open("raw/" + output_file_name + ".json", "w",encoding="UTF-8")
    f.write("[\n")

    request_counter=0
    for j in range(end_year-start_year):
        year_str=str(start_year+j)
        for i in range(12):

            month_str=("0"+str(i+1)) if i<9 else str(i+1)
            print("Year: " + year_str + "\nMonth: " + month_str+"\n")            

            start_date=str(year_str)+str(month_str)+"01"+"000000"
            end_date=str(year_str)+str(month_str)+str(number_of_days_in_month(start_year+j,i+1))+"000000"

            request_string = "https://arquivo.pt/textsearch?q=&siteSearch=" + website + "&from="+ start_date+ "&to="+ end_date + "&dedupValue=2000&maxItems=2000"

            if(request_counter==250):
                sleep(60)
                request_counter=0
            request = requests.get(request_string)
            request_counter+=1


            while(request.status_code!=200):
                #print("Too many requests")
                if(request.status_code==429 or request_counter==250):
                    sleep(60)
                    request_counter=0
                else:
                    print("Request error: "+str(request.status_code))
                request = requests.get(request_string)
                request_counter+=1

            data = json.loads(request.content)
            for k in range(len(data["response_items"])):
                if(k!=0 or i!=0 or j!=0 ):
                    f.write(",\n")
                if(request_counter==250):
                    sleep(60)
                    request_counter=0
                next_request = requests.get(data["response_items"][k]["linkToExtractedText"])
                request_counter+=1
                while(request.status_code!=200 and request.status_code!=404):
                    #print("Too many requests")
                    if(request.status_code==429 or request_counter==250):
                        sleep(60)
                        request_counter=0
                    else:
                        print("Request error: "+str(request.status_code))
                        print("Link: " + data["response_items"][k]["linkToExtractedText"])
                    next_request = requests.get(data["response_items"][k]["linkToExtractedText"])
                    request_counter+=1

                text = next_request.content.decode("UTF-8",'replace')
                json.dump({"date": data["response_items"][k]["date"], "link": data["response_items"][k]["linkToArchive"], "contentLength": len(text),"type":data["response_items"][k]["mimeType"], "title": data["response_items"][k]["title"], "text": text}, fp=f,indent=4, ensure_ascii=False)
                
    f.write("\n]")


def run():
    group_links = {'ps' : "ps.pt", 'ps_www': "www.ps.pt", 'psd': 'www.psd.pt', 'ch' : "partidochega.pt", 'il': "iniciativaliberal.pt"}
    start_year = 2017
    end_year = 2023

    for group in group_links:
        retrieve_data(start_year, end_year, group_links[group], group)
            
# run()            
retrieve_data(2019,2023,"partidochega.pt", "chega")
