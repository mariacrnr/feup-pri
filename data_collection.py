from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor,wait
from time import sleep
import requests
import json
from calendar import monthrange
from os import remove


def number_of_days_in_month(year:int, month:int):
    return monthrange(year, month)[1]


def retrieve_data(start_year, end_year, website,output_file_name):

    f = open(output_file_name+".json", "w")
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
                json.dump({"date": data["response_items"][k]["date"], "link": data["response_items"][k]["linkToArchive"], "contentLength": len(text), "text": text}, fp=f,indent=4, ensure_ascii=False)
                if((k+1)!=len(data["response_items"]) and (i+1)!=12 and (j+1)!=(end_year-start_year)):
                    f.write(",\n")
    f.write("\n]")

            



#political_parties = {"ps.pt": 1999, "www.psd.pt": 1996, "partidochega.pt": 2019 , "iniciativaliberal.pt": 2017 , "pcp.pt": 1996, "www.bloco.org": 2005, "www.pan.com.pt": 2013, "partidolivre.pt": 2018}

retrieve_data(1999, 2023, "www.ps.pt","ps")