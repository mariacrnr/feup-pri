import pandas as pd
import requests 
from sklearn.metrics import PrecisionRecallDisplay
import matplotlib.pyplot as plt
import json

def evaluate(system,query_type,indexed):

    queries = pd.read_json('titles.json')
    results=[]
    mean_avg_precision=[]
    graphs_data=[]
    for i in range(5):
        url = queries.iloc[i][query_type+'_query']
        relevant_documents=queries.iloc[i][query_type+'_links']
        response=requests.get(url).json()['response']
        retrieved_documents=response['numFound'] if response['numFound']<30 else 30
        if(retrieved_documents>0):
            response_df = pd.json_normalize(response['docs'])
            relevant_documents_retrieved=0
            relevant_documents_retrieved_10=0
            
            positions=list(range(retrieved_documents))
            relevant=[0 for _ in range(retrieved_documents)]

            for relevant_document in relevant_documents:
                if(response_df['link'].str.contains(relevant_document,regex=False).any()):
                    relevant_documents_retrieved+=1
                if(response_df['link'][0:(len(relevant_documents) if len(relevant_documents)<10 else 10)].str.contains(relevant_document,regex=False).any()):
                    relevant_documents_retrieved_10+=1
                
                
            for k in range(len(response_df)):
                if(indexed):
                    link=response_df.iloc[k]['link']
                else:
                    link=response_df.iloc[k]['link'][0]
                if(link in relevant_documents):
                    if(k==0):
                        positions[k]=1
                    else:
                        positions[k]=positions[k-1]+1
                    relevant[k]=1
                else:
                    if(k!=0):
                        positions[k]=positions[k-1]


            recall_list=list(map(lambda x:x/len(relevant_documents),positions))
            precision_list=list(range(retrieved_documents))
            
            for k in range(retrieved_documents):
                precision_list[k]=positions[k]/(k+1)
                
            avg_precision=0 if relevant[0:10].count(1)==0 else sum(map(lambda x,y:x*y,precision_list[0:10],relevant[0:10]))/relevant[0:10].count(1)

            
            graphs_data.append([recall_list[0:10],precision_list[0:10],"Query"+str(i+1)])
            
            # plt.show()
            
            precision_10=relevant_documents_retrieved_10/(len(relevant_documents) if len(relevant_documents)<10 else 10)
            precision=relevant_document if relevant_document==0 else relevant_documents_retrieved/retrieved_documents
            recall=relevant_documents_retrieved/len(relevant_documents)
            f_measure=(precision+recall) if (precision+recall)==0 else 2*precision*recall/(precision+recall)
            
            print("Query "+str(i+1) +" :")
            print("\tPrecision: "+str(precision))
            print("\tP@"+str((len(relevant_documents) if len(relevant_documents)<10 else 10))+": "+str(precision_10))
            print("\tAvg Precision: "+str(avg_precision))

            print("\tF Measure: "+str(f_measure))
            print("\tRecall: "+str(recall))
        else:
            precision_10=0
            precision=0
            recall=0
            f_measure=0
            avg_precision=0
        results.append({'precision':precision,'p10':precision_10,'avg_precision':avg_precision,'f_measure':f_measure,'recall':recall})
        mean_avg_precision.append(avg_precision)
    
    
    for g in graphs_data:
        plt.plot(g[0],g[1],marker='o',label=g[2])

    plt.xlim(0, 1.1)
    plt.ylim(0, 1.1)
    plt.legend(loc='lower left')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.savefig('evaluation_output/'+system+'/'+query_type+'.pdf')
    plt.clf()
    
    mean_avg_precision=sum(mean_avg_precision)/5
    results.append({'mean_avg_precision':mean_avg_precision})
    with open('evaluation_output/'+system+'/'+query_type+'.json', 'w') as fp:
        json.dump(results, fp)
    
    
def run():
    print("Simple Query:")
    evaluate('system_1','simple',False)
    print("Complex Query:")
    evaluate('system_1','complex',False)
    
run()