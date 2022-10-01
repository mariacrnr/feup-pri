import requests
import json
import re
from sympy import true


hitsPerPage=100
i=0
hits=1
while(hits>0):
    r=requests.get("https://arquivo.pt/textsearch?q=&siteSearch=www.pcp.pt&from=2020&dedupValue="+str(hitsPerPage)+"&maxItems="+str(hitsPerPage)+"&offset="+str(i*hitsPerPage))
    print("ok")
    byte_values=r.content
    data=json.loads(byte_values)
    hits=len(data["response_items"])

    jsonObjectToStore=[]
    f = open(str(i)+".json", "w")
    for item in data["response_items"]:
        r=requests.get(item["linkToExtractedText"])
        print(r.status_code)
        text=r.content.decode("UTF-8",'replace')
        clean_text=re.sub("[\n\t\r]"," ",text)
        evenly_spaced_text=re.sub(" +"," ",clean_text)
        jsonObjectToStore.append({"date":item["tstamp"],"link":item["linkToArchive"],"contentLength":item["contentLength"],"text":evenly_spaced_text})
        
    f.write(json.dumps(jsonObjectToStore, indent=4,ensure_ascii=False))
    f.close()    
    i+=1
