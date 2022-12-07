const express = require('express')
const request = require('request');
const cors = require('cors')


const app = express()
app.use(cors())

const port = 3000

app.get('/', (req, res) => {
    const baseRequestUrl="http://localhost:8983/solr/parties/select?hl=on&hl.method=unified&defType=edismax&indent=true";
    let rows='&rows=10';
    let date="";
    let party=req.query.party!=null ? '&fq=party:' + req.query.party : ''
    let qop="AND";
    let qf="title^5 text";
    let query = '&q='+req.query.q
    let start = req.query.start!=null ? '&start=' + req.query.start : ''
    let dateRange = req.query.dateRange!=null ? '&fq=date:' + req.query.dateRange : ''
    let requestUrl=baseRequestUrl+'&q.op='+qop+query+'&qf='+qf+party+dateRange+rows+start;

    request(requestUrl, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            res.send(response.body)
        }
    })
})

app.listen(port, () => {
  console.log(`App listening on port ${port}`)
})

