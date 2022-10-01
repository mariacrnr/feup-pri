import requests
import json

i=0
hits=1
while(hits>0):
    r=requests.get("https://arquivo.pt/textsearch?q=&siteSearch=www.ps.pt&from=2020&dedupValue=2000&maxItems=2000&offset="+str(i))
    print("new page")
    print(r.status_code)
    byte_values=r.content
    data=json.loads(byte_values)
    hits=len(data["response_items"])
    for item in data["response_items"]:
        r=requests.get(item["linkToExtractedText"])
        print(r.status_code)
        text=r.content.decode("utf8")
        f = open("files/"+item["date"]+".txt", "w")
        f.write(item["linkToArchive"]+"\n")
        f.write(text)
        f.close()
    i+=2000
