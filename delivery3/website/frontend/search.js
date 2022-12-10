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
const start= urlParams.get('start');


function setUpEventListeners(){
    const refreshResultsButton = document.getElementById('refresh-results-button');
    const optionButtons = document.getElementsByClassName('options-button');


    searchButton.addEventListener('click', (event) => {
        event.preventDefault();
        const searchInputValue = searchInput.value;
        if(searchInputValue=='') return;
        const partyInputValue = partyInput.options[partyInput.selectedIndex].value;
        const dateFromInputValue = dateFromInput.value;
        const dateToInputValue = dateToInput.value;
        const partyParam= partyInputValue=='' ? '' : "&party="+partyInputValue
        const dateFromParam = (dateFromInputValue=='') ? '' : "&from="+dateFromInputValue
        const dateToParam = (dateToInputValue=='') ? '' : "&to="+dateToInputValue
    
        window.location.href="http://localhost:8080/search-results.html?q="+searchInputValue+partyParam+dateFromParam+dateToParam
    });

    searchInput.addEventListener('keypress', (event) =>{
        if (event.code === "Enter") {  //checks whether the pressed key is "Enter"
            event.preventDefault();
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
    })
    

    for (let index = 0; index < optionButtons.length; index++) {
        const optionButton = optionButtons[index];

        optionButton.addEventListener('click',(event)=>{
            let hiddenMenu = event.target.parentElement.getElementsByClassName('relevant-menu-hidden')[0]
            console.log(hiddenMenu.style.display)
            hiddenMenu.style.display= (hiddenMenu.style.display=='' || hiddenMenu.style.display=='none') ? 'flex' : 'none'

            hiddenMenu.children[0].addEventListener('click',(event)=>{
                refreshResultsButton.style.display='block'
                hiddenMenu.style.display= 'none'
                hiddenMenu.parentElement.parentElement.parentElement.className='search-result-item relevant-search-result'
            })

            hiddenMenu.children[1].addEventListener('click',(event)=>{
                refreshResultsButton.style.display='block'
                console.log(hiddenMenu.style.display)
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
        const dateParam= (dateFromInput.value==null && dateToInput.value==null) ? '' : "["+dateFromInput.value+"T00:00:00Z TO "+dateToInput.value+"T23:59:59Z]";


        let body = {"q":query,"relevant":relevantIDs,"notRelevant":notRelevantIDs,"party":partyInputValue,"dateRange":dateParam}
        const response = fetch(baseRequestUrl, {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST', 
            mode: 'cors',
            body: JSON.stringify(body)
        }).then(async response=>{
            let searchResultsContainer = document.getElementById('search-results');
            searchResultsContainer.innerHTML=""
            data = await response.json()
            if(parseResults(data,true)){
                setUpEventListeners()
                e.target.remove()
            }
        });
    })

}



async function requestSolr(query){
    const baseRequestUrl="http://localhost:3000/?";
    const rows=10;
    const dateFrom= dateFromInput.value=='' ? '1970-01-01' : dateFromInput.value
    const dateTo= dateToInput.value=='' ? '2023-01-01' : dateToInput.value
    const dateParam= (dateFromInput.value==null && dateToInput.value==null) ? '' : "&dateRange=["+dateFrom+"T00:00:00Z TO "+dateTo+"T23:59:59Z]";
    const partyParam= partyInput.value=='' ? '' : '&party='+partyInput.value
    let qop="AND";
    let qf="title^5 text";
    let startParam= start==null ? '' : '&start='+start

    let requestUrl=baseRequestUrl+'q='+query+partyParam+dateParam+startParam;

    const response = await fetch(requestUrl, {
		method: 'GET', // *GET, POST, PUT, DELETE, etc.
		mode: 'cors', // no-cors, *cors, same-origin
	}).then(response=>{
		return response.json();
	});
	return response;
}

function createSearchResult(id,title,highlight,link,refreshedResults){
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

    if(!refreshedResults){
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
    } else divLinkOptions.append(linkA)

    

    


    let resultTitleA=document.createElement('a')
    resultTitleA.setAttribute('href',link)
    let resultTitleH2=document.createElement('h2')
    console.log(title)
    resultTitleH2.textContent=title==undefined ? 'Untitled webpage' : title
    resultTitleA.append(resultTitleH2)
    let highlightP=document.createElement('p')
    highlightP.innerHTML=highlight
    
    outerDiv.append(divLinkOptions)
    outerDiv.append(resultTitleA)
    outerDiv.append(highlightP)

    searchResultsContainer.appendChild(outerDiv)

}

function parseResults(resultsJson,refreshedResults){
	const timeSolrMilliseconds=resultsJson['responseHeader']['QTime']
	const response=resultsJson['response']
	const numberOfResults=response['numFound']
	const numberFoundExact=response['numFoundExact']
	const resultDocs=response['docs']
	const resultHighlights=resultsJson['highlighting']
    
    let resultsAndTimeH5=document.getElementById("results-time");
    resultsAndTimeH5.textContent= (numberFoundExact ? 'Exactly ' : 'About ') +numberOfResults.toLocaleString()+ ' results ('+timeSolrMilliseconds/1000.0+' seconds)'

    
	resultDocs.forEach(result => {
        let highlighted =resultHighlights[result['id']]['text'][0]
        if(highlighted==undefined){
            highlighted=result['text']
        }
        highlighted=highlighted.substring(0,(highlighted.length<400 ? highlighted.length : 400)) + '...'
        let link = result['link']
        let id=result['id']

		createSearchResult(id,result['title'],highlighted,link,refreshedResults)
	});

    let previousPage=document.getElementById('previous-page-button')
    let separator = document.getElementById('page-selector-sep')
    let nextPage=document.getElementById('next-page-button')
    if(!refreshedResults){

        if(start==null){
            previousPage.remove()
            separator.remove()
            nextPage.setAttribute('href',window.location.href+'&start=10')
            if(10>numberOfResults){
                nextPage.remove()
                separator.remove()
            }
        }
        else{
            previousURL=window.location.href.split('&start=')[0]
            let newStartValue=parseInt(start)+10
            if(newStartValue>numberOfResults){
                nextPage.remove()
                separator.remove()
            }
            else{
                nextPage.setAttribute('href',previousURL+'&start='+newStartValue)
            }
            newStartValue=parseInt(start)-10
            previousPage.setAttribute('href',start==10 ? previousURL : previousURL+'&start='+newStartValue)
        }
    }
    else{
        if(previousPage!=null)
            previousPage.remove()
        if(nextPage!=null)
            nextPage.remove()
        if(separator!=null)
            separator.remove()
    }
    return true

}


requestSolr(searchInput.value).then(resultsJson=>{
	if(parseResults(resultsJson,false))
        setUpEventListeners()

})


