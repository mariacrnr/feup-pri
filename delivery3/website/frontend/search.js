

function search(){
    const searchInputValue = searchInput.value;
    if(searchInputValue=='') return;
    const partyInputValue = partyInput.options[partyInput.selectedIndex].value;
    const dateFromInputValue = dateFromInput.value;
    const dateToInputValue = dateToInput.value;
    const partyParam= partyInputValue=='' ? '' : "&party="+partyInputValue
    const dateFromParam = (dateFromInputValue=='') ? '' : "&from="+dateFromInputValue
    const dateToParam = (dateToInputValue=='') ? '' : "&to="+dateToInputValue

    window.location.href="http://localhost:8080/search-results.html?q="+searchInputValue+partyParam+dateFromParam+dateToParam
}

async function requestSolr(query,qop="AND",start=0){
    console.log(start,query)
    const baseRequestUrl="http://localhost:3000/";
    const dateFrom= dateFromInput.value=='' ? '1970-01-01' : dateFromInput.value
    const dateTo= dateToInput.value=='' ? '2023-01-01' : dateToInput.value
    const dateParam= (dateFromInput.value==null && dateToInput.value==null) ? '' : "&dateRange=["+dateFrom+"T00:00:00Z TO "+dateTo+"T23:59:59Z]";
    const partyParam= partyInput.value=='' ? '' : '&party='+partyInput.value
    let startParam= start==null ? '' : '&start='+start
    let requestUrl=baseRequestUrl;

    const response = await fetch(requestUrl, {
        headers:{
            'Content-Type': 'application/x-www-form-urlencoded'
        },
		method: 'POST', // *GET, POST, PUT, DELETE, etc.
		mode: 'cors', // no-cors, *cors, same-origin
        body: 'qop='+qop+'&q='+query+partyParam+dateParam+startParam
	}).then(response=>{
		return response.json();
	});
    console.log(response)
	return response;
}

function setUpEventListeners(){
    const refreshResultsButton = document.getElementById('refresh-results-button');
    const optionButtons = document.getElementsByClassName('options-button');


    searchButton.addEventListener('click', (event) => {
        event.preventDefault();
        search()
    });

    searchInput.addEventListener('keypress', (event) =>{
        if (event.code === "Enter") {  //checks whether the pressed key is "Enter"
            event.preventDefault();
            search()
        }
    })
    

    for (let index = 0; index < optionButtons.length; index++) {
        const optionButton = optionButtons[index];

        optionButton.addEventListener('click',(event)=>{
            let hiddenMenu = event.target.parentElement.getElementsByClassName('relevant-menu-hidden')[0]
            hiddenMenu.style.display= (hiddenMenu.style.display=='' || hiddenMenu.style.display=='none') ? 'flex' : 'none'

            hiddenMenu.children[0].addEventListener('click',(event)=>{
                refreshResultsButton.style.display='block'
                hiddenMenu.style.display= 'none'
                hiddenMenu.parentElement.parentElement.parentElement.className='search-result-item relevant-search-result'
            })

            hiddenMenu.children[1].addEventListener('click',(event)=>{
                refreshResultsButton.style.display='block'
                hiddenMenu.style.display= 'none'
                hiddenMenu.parentElement.parentElement.parentElement.className='search-result-item not-relevant-result'
            })
            
        })
    }

    refreshResultsButton.addEventListener('click', (e)=>{
        let relevantElements = document.getElementsByClassName('relevant-search-result');
        let relevantIDs=[]
        for (let index = 0; index < relevantElements.length; index++) {
            relevantIDs.push(relevantElements[index].id)
        }

        let notRelevantElements = document.getElementsByClassName('not-relevant-result');
        let notRelevantIDs=[]
        for (let index = 0; index < notRelevantElements.length; index++) {
            notRelevantIDs.push(notRelevantElements[index].id)
        }
        let query = urlParams.get('q');

        const baseRequestUrl="http://localhost:3000/new-query"
        const partyInputValue = partyInput.options[partyInput.selectedIndex].value;
        const dateParam= (dateFromInput.value=='' && dateToInput.value=='') ? '' : "["+dateFromInput.value+"T00:00:00Z TO "+dateToInput.value+"T23:59:59Z]";


        let body = {"q":query,"relevant":relevantIDs,"notRelevant":notRelevantIDs,"party":partyInputValue,"dateRange":dateParam}
        const response = fetch(baseRequestUrl, {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST', 
            mode: 'cors',
            body: JSON.stringify(body)
        }).then(async response=>{
            data = await response.json()
            if(parseResults(data)){
                console.log(data)
                setUpEventListeners()
                e.target.style.display='none'
            }
            console.log(data)

            urlParams.set('q',data['responseHeader']['params']['q'])
            urlParams.set('qop',data['responseHeader']['params']['q.op'])
            setUpPageSwitch()

        });
    })

    let previousPage=document.getElementById('previous-page-button')
    let nextPage=document.getElementById('next-page-button')
    
    previousPage.removeEventListener('click',previousPageClick)
    previousPage.addEventListener('click',previousPageClick)
    
    nextPage.removeEventListener('click',previousPageClick)
    nextPage.addEventListener('click',nextPageClick)    

}

function nextPageClick(){
    if(urlParams.get('start')=='')
        return
    let qop=urlParams.get('qop')==null ? "AND" : "OR"
    let start = urlParams.get('start')==null ? 0 : parseInt(urlParams.get('start'))
    urlParams.set('start',start+10)
    requestSolr(urlParams.get('q'),qop,start+10).then(resultsJson=>{
        if(parseResults(resultsJson))
            setUpEventListeners()
    })
}

function previousPageClick(){
    if(urlParams.get('start')==''){
        return  
    }
    let qop=urlParams.get('qop')==null ? "AND" : "OR"
    let start = urlParams.get('start')==null ? 0 : parseInt(urlParams.get('start'))
    if(urlParams.get('start')-10==0)
        urlParams.delete('start')
    else{
        urlParams.set('start',start-10)
    }
    requestSolr(urlParams.get('q'),qop,start-10).then(resultsJson=>{
        
        if(parseResults(resultsJson))
            setUpEventListeners()
        
    })
}



function createSearchResult(id,title,highlight,link){
    let searchResultsContainer = document.getElementById('search-results');

    let outerDiv=document.createElement('div');
    outerDiv.setAttribute('class','search-result-item');
    outerDiv.setAttribute('id',id)

    let linkH5=document.createElement('h5')
    linkH5.textContent=link.substring(0,(link.length<80 ? link.length : 80))+'...'

    let divLinkOptions=document.createElement('div')
    divLinkOptions.setAttribute('class','link-and-options')

    let linkA=document.createElement('a')
    linkA.setAttribute('href',link)
    linkA.append(linkH5)
    
    let divRelevantMenu=document.createElement('div')
    divRelevantMenu.setAttribute('class','relevant-menu')

    let optionsIcon=document.createElement('img')
    optionsIcon.setAttribute('src','/images/options.svg')
    optionsIcon.setAttribute('class','options-button')

    let divRelevantMenuHidden=document.createElement('div')
    divRelevantMenuHidden.setAttribute('class','relevant-menu-hidden')
    let relevantMenuH4=document.createElement('h4')
    relevantMenuH4.textContent="Mark as relevant"

    let nonRelevantMenuH4=document.createElement('h4')
    nonRelevantMenuH4.textContent="Mark as not relevant"

    divRelevantMenuHidden.append(relevantMenuH4)
    divRelevantMenuHidden.append(nonRelevantMenuH4)

    
    divRelevantMenu.append(optionsIcon)
    divRelevantMenu.append(divRelevantMenuHidden)

    divLinkOptions.append(linkA)
    divLinkOptions.append(divRelevantMenu)



    let resultTitleA=document.createElement('a')
    resultTitleA.setAttribute('href',link)
    let resultTitleH2=document.createElement('h2')
    resultTitleH2.textContent=title==undefined ? 'Untitled webpage' : title
    resultTitleA.append(resultTitleH2)
    let highlightP=document.createElement('p')
    highlightP.innerHTML=highlight
    
    outerDiv.append(divLinkOptions)
    outerDiv.append(resultTitleA)
    outerDiv.append(highlightP)

    searchResultsContainer.appendChild(outerDiv)

}

function parseResults(resultsJson){
    let searchResultsContainer = document.getElementById('search-results');
    while (searchResultsContainer.firstChild) {
        searchResultsContainer.removeChild(searchResultsContainer.firstChild);
    }
	const timeSolrMilliseconds=resultsJson['responseHeader']['QTime']
	const response=resultsJson['response']
	const numberOfResults=response['numFound']
	const numberFoundExact=response['numFoundExact']
	const resultDocs=response['docs']
	const resultHighlights=resultsJson['highlighting']
    
    let resultsAndTimeH5=document.getElementById("results-time");
    resultsAndTimeH5.innerHTML= (numberFoundExact ? 'Exactly ' : 'About ') +numberOfResults.toLocaleString()+ ' results ('+timeSolrMilliseconds/1000.0+' seconds)'

    
	resultDocs.forEach(result => {
        let highlighted =resultHighlights[result['id']]['text'][0]
        if(highlighted==undefined){
            highlighted=result['text']
        }
        highlighted=highlighted.substring(0,(highlighted.length<400 ? highlighted.length : 400)) + '...'
        let link = result['link']
        let id=result['id']

		createSearchResult(id,result['title'],highlighted,link)
	});

    let previousPage=document.getElementById('previous-page-button')
    let separator = document.getElementById('page-selector-sep')
    let nextPage=document.getElementById('next-page-button')
    let start= urlParams.get('start')==null ? 0 : parseInt(urlParams.get('start'))

    if(start==null||start==0){
        previousPage.style.display='none'
        separator.style.display='none'
        if(10>numberOfResults){
            nextPage.style.display='none'
            separator.style.display='none'
        }
    }
    else{
        previousPage.style.display='block'
        separator.style.display='block'
        nextPage.style.display='block'

        let newStartValue=parseInt(start)+10
        if(newStartValue>numberOfResults){
            nextPage.style.display='none'
            separator.style.display='none'
        }
        newStartValue=parseInt(start)-10
    }

    return true

}
const url = window.location.search;
const urlParams = new URLSearchParams(url);

const searchButton = document.getElementById('search-button');
const searchInput = document.getElementById('search-input');
const partyInput = document.getElementById('party-filter');
const dateFromInput = document.getElementById('start-date-filter');
const dateToInput = document.getElementById('end-date-filter');


searchInput.value=urlParams.get('q');
partyInput.value=urlParams.get('party')==undefined ? '' : urlParams.get('party')
dateFromInput.value=urlParams.get('from');
dateToInput.value=urlParams.get('to');
let start= urlParams.get('start');

requestSolr(searchInput.value).then(resultsJson=>{
	if(parseResults(resultsJson)){
        setUpEventListeners()
    }

})



