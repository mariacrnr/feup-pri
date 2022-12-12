const express = require('express')
const request = require('request');
const cors = require('cors')
const bodyParser = require('body-parser');
const { response } = require('express');



const app = express()
app.use(cors())
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());


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
    console.log(query)

    const baseRequestUrl="http://localhost:8983/solr/parties/select?hl=on&hl.method=unified&defType=edismax&indent=true";
    party= (party!=null && party!='') ? '&fq=party:' + party : ''
    query = '&q='+query
    start = (start!=null && start!='') ? '&start=' + start : ''
    dateRange = (dateRange!=null && dateRange!='') ? '&fq=date:' + dateRange : ''
    
    let requestUrl=baseRequestUrl+'&q.op='+qop;
    let response = await fetch(requestUrl,{
        headers:{
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        method: 'POST', 
        mode: 'cors',
        body:query+'&qf=title^5 text'+party+dateRange+'&rows=10'+start+"&stopwords=true&synonyms=true"
    })
    let data = await response.json()
    return data
}

app.post('/', async (req, res) => {
    let response = await solrSearch(req.body.qop,req.body.q,req.body.party,req.body.dateRange,req.body.start)
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

    words = query.toLowerCase().match(/\b(\w+)\b/g)
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
        var words = textContent.toLowerCase().match(/\b(\w+)\b/g)
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
        words = textContent.toLowerCase().match(/\b(\w+)\b/g)
        words.forEach(word => {
            if(word in notRelevantVector){
                notRelevantVector[word]+=1
            }
            else{
                notRelevantVector[word]=1
            }
        });
        
    }


    let relevantCoefficient= 0.8/relevant.length
    let notRelevantCoefficient= 0.2/notRelevant.length


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

    let queryString ="("

    Object.keys(queryVector).forEach(key=>{
            queryString+=key+'^'+(Math.round((queryVector[key] + Number.EPSILON) * 100) / 100).toString()+' '
    })
    queryString+=") AND ("+ query + ")"

    let response = await solrSearch("OR",queryString,party,dateRange)
    res.send(response)
})

app.listen(port, () => {
  console.log(`App listening on port ${port}`)
})

