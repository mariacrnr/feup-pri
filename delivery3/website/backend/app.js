const express = require('express')
const request = require('request');
const cors = require('cors')
const bodyParser = require('body-parser');
const { response } = require('express');



const app = express()
app.use(cors())
app.use(bodyParser.json());


const port = 3000

async function getElementById(id){
    const baseRequestUrl="http://localhost:8983/solr/parties/select?hl=on&hl.method=unified&defType=edismax&indent=true&q.op=AND&qf=id&q="+id;
    let response = await fetch(baseRequestUrl,{
        method: 'GET', 
        mode: 'cors',
    })
    let data = await response.json()
    return data
}

async function solrSearch(qop,query,party=null,dateRange=null,start=null){
    const baseRequestUrl="http://localhost:8983/solr/parties/query?hl=on&hl.method=unified&defType=edismax&indent=true";
    party=party!=null ? '&fq=party:' + party : ''
    query = '&q='+query
    start = start!=null ? '&start=' + start : ''
    console.log("vai ser aqui")
    console.log(dateRange)
    dateRange = dateRange!=null ? '&fq=date:' + dateRange : ''
    
    let requestUrl=baseRequestUrl+'&q.op='+qop;
    let response = await fetch(requestUrl,{
        headers:{
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        method: 'POST', 
        mode: 'cors',
        body:query+'&qf=title^5 text'+party+dateRange+'&rows=10'+start
    })
    let data = await response.json()
    return data
}

app.get('/', async (req, res) => {
    let response = await solrSearch("AND",req.query.q,req.query.party,req.query.dateRange,req.query.start)
    res.send(response)
})

app.post('/new-query', async (req, res) => {
    let query = req.body.q
    let party = req.body.party
    let dateRange = req.body.dateRange
    let relevant = req.body.relevant
    let notRelevant = req.body.notRelevant

    let relevantVector={}
    let notRelevantVector={}
    let queryVector = {}

    words = query.match(/\b(\w+)\b/g)
    words.forEach(word => {
        if(word in queryVector){
            queryVector[word]+=1
        }
        else{
            queryVector[word]=1
        }
    });

    for (let index = 0; index < relevant.length; index++) {
        const id = relevant[index]

        let result = await getElementById(id)

        let textContent = ''
        if(result['response']['numFound']>0){
            textContent = result['response']['docs'][0]['text']
        }
        var words = textContent.match(/\b(\w+)\b/g)
        words.forEach(word => {
            if(word in relevantVector){
                relevantVector[word]+=1
            }
            else{
                relevantVector[word]=1
            }
        });
    }

    for (let index = 0; index < notRelevant.length; index++) {
        const id = notRelevant[index];

        let result = await getElementById(id)
        let textContent = ''
        if(result['response']['numFound']>0){
            textContent = result['response']['docs'][0]['text']
        }
        words = textContent.match(/\b(\w+)\b/g)
        words.forEach(word => {
            if(word in notRelevantVector){
                notRelevantVector[word]+=1
            }
            else{
                notRelevantVector[word]=1
            }
        });
        
    }


    let relevantCoefficient= 10.0/relevant.length
    let notRelevantCoefficient= 1.0/notRelevant.length

    Object.keys(relevantVector).forEach(key=>{
        if(key in queryVector){
            queryVector[key]+=relevantCoefficient*relevantVector[key]
        }
        else{
            queryVector[key]=relevantCoefficient*relevantVector[key]
        }
    })

    Object.keys(notRelevantVector).forEach(key=>{
        if(key in queryVector){
            queryVector[key]-=notRelevantCoefficient*notRelevantVector[key]
        }
        else{
            queryVector[key]=-1.0*notRelevantCoefficient*notRelevantVector[key]
        }
    })
    console.log(queryVector)

    let queryString =""

    Object.keys(queryVector).forEach(key=>{
        if(queryVector[key]>0)
            queryString+=key+'^'+Math.round(queryVector[key]).toString()+' '
        
    })
    let response = await solrSearch("OR",queryString,party,dateRange)
    res.send(response)
})

app.listen(port, () => {
  console.log(`App listening on port ${port}`)
})

