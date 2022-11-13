import pandas as pd
import requests 


QUERY_TYPE='complex_query'

queries = pd.read_json('data/queries.json')

for i in range(len(queries)):
    url = queries.iloc[i][QUERY_TYPE]
    relevant_documents=queries.iloc[i]['links']
    response=requests.get(url).json()['response']
    retrieved_documents=response['numFound']
    response_df = pd.json_normalize(response['docs'])
    relevant_documents_retrieved=0
    for relevant_document in relevant_documents:
        if(response_df['link'].str.contains(relevant_document,regex=False).any()):
            relevant_documents_retrieved+=1
    
    precision=relevant_documents_retrieved/retrieved_documents
    recall=relevant_documents_retrieved/len(relevant_documents)
    
    print("Query "+str(i+1) +" :")
    print("\tPrecision: "+str(precision))
    print("\tRecall: "+str(recall))

    
    
        
    