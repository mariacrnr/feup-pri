import requests
import json
import re
from sympy import true


def text_cleanup(content):

    text = content.decode("UTF-8",'replace')
    clean_text = re.sub("[\n\t\r]"," ",text)
    evenly_spaced_text = re.sub(" +"," ",clean_text)

    return evenly_spaced_text

def start_data_requests(hits_per_page, date, website):

    hits=1
    i=0

    while(hits > 0):

        request = requests.get("https://arquivo.pt/textsearch?q=&siteSearch=" + website + "&from="+ str(date) +"&dedupValue=" + str(hits_per_page) + "&maxItems=" +
            str(hits_per_page)+"&offset="+ str(i * hits_per_page))    
        print("Request Processed")

        data = json.loads(request.content)
        hits = len(data["response_items"])

        jsonData = []
        f = open(str(i)+".json", "w")

        for item in data["response_items"]:
            next_request = requests.get(item["linkToExtractedText"])
            print(next_request.status_code)

            text = text_cleanup(next_request.content);

            jsonData.append({"date": item["tstamp"], "link": item["linkToArchive"], "contentLength": item["contentLength"], "text": text})
            
        f.write(json.dumps(jsonData, indent=4, ensure_ascii=False))
        f.close()

        i+=1
        

start_data_requests(100, 2020, "www.pcp.pt")
