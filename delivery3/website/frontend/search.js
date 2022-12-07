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

    searchButton.addEventListener('click', (event) => {
        event.preventDefault();
        const searchInputValue = searchInput.value;
        const partyInputValue = partyInput.options[partyInput.selectedIndex].value;
        const dateFromInputValue = dateFromInput.value;
        const dateToInputValue = dateToInput.value;
        const partyParam= partyInputValue=='' ? '' : "&party="+partyInputValue
        const dateFromParam = (dateFromInputValue=='') ? '' : "&from="+dateFromInputValue
        const dateToParam = (dateToInputValue=='') ? '' : "&to="+dateToInputValue
    
        window.location.href="http://localhost:8080/search-results.html?q="+searchInputValue+partyParam+dateFromParam+dateToParam
    });

    let optionButtons = document.getElementsByClassName('options-button');
    console.log(optionButtons.length)
    for (let index = 0; index < optionButtons.length; index++) {
        const optionButton = optionButtons[index];

        optionButton.addEventListener('click',(event)=>{
            let hiddenMenu = event.target.parentElement.getElementsByClassName('relevant-menu-hidden')[0]
            console.log(hiddenMenu.style.display)
            hiddenMenu.style.display= (hiddenMenu.style.display=='' || hiddenMenu.style.display=='none') ? 'flex' : 'none'
        })
    }

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

function createSearchResult(id,title,highlight,link){
    let searchResultsContainer = document.getElementById('search-results');

    let outerDiv=document.createElement('div');
    outerDiv.setAttribute('class','search-result-item');
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
    optionsIcon.setAttribute('id',id)


    let divRelevantMenuHidden=document.createElement('div')
    divRelevantMenuHidden.setAttribute('class','relevant-menu-hidden')
    let relevantMenuH4=document.createElement('h4')
    relevantMenuH4.textContent="This result isn't relevant"
    divRelevantMenuHidden.append(relevantMenuH4)

    
    divRelevantMenu.append(optionsIcon)
    divRelevantMenu.append(divRelevantMenuHidden)

    divLinkOptions.append(linkA)
    divLinkOptions.append(divRelevantMenu)


    let resultTitleA=document.createElement('a')
    resultTitleA.setAttribute('href',link)
    let resultTitleH2=document.createElement('h2')
    resultTitleH2.textContent=title
    resultTitleA.append(resultTitleH2)
    let highlightP=document.createElement('p')
    highlightP.innerHTML=highlight
    
    outerDiv.append(divLinkOptions)
    outerDiv.append(resultTitleA)
    outerDiv.append(highlightP)

    searchResultsContainer.appendChild(outerDiv)

}

function parseResults(resultsJson){
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

		createSearchResult(id,result['title'],highlighted,link)
	});


    let previousPage=document.getElementById('previous-page-button')
    let separator = document.getElementById('page-selector-sep')
    let nextPage=document.getElementById('next-page-button')
    if(start==null){
        previousPage.remove()
        separator.remove()
        nextPage.setAttribute('href',window.location.href+'&start=10')
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
    return true

}


requestSolr(searchInput.value).then(resultsJson=>{
	if(parseResults(resultsJson))
        setUpEventListeners()

})


