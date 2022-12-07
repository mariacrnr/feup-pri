const url = window.location.search;
const urlParams = new URLSearchParams(url);
const query = urlParams.get('q');


const searchButton = document.getElementById('search-button');
const searchInput = document.getElementById('search-input');
searchInput.value=query

searchButton.addEventListener('click', (event) => {
    event.preventDefault();
    const inputValue = searchInput.value;
    window.location.href="http://localhost:8080/search-results.html?q="+inputValue;
});

function requestSolr(query){
    const baseRequestUrl="http://localhost:8983/solr/parties/select?defType=edismax&indent=true&";
    let rows=10;
    let date="[2019-01-01T00:00:00Z TO 2019-12-31T23:59:59Z]";
    let party="";
    let qop="AND";
    let qf="title^5 text";
    
    let requestUrl=baseRequestUrl+qop+'&q='+query+'&rows='+rows;

    fetch(requestUrl)
    .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          throw new Error('Something went wrong on API server!');
        }
    })
}

function createSearchResult(title,highlight,link){
    let searchResultsContainer = document.getElementById('search-results');

    let outerDiv=document.createElement('div');
    outerDiv.setAttribute('class','search-result-item');
    let linkH5=document.createElement('h5')
    linkH5.innerHTML=link
    let linkA=document.createElement('a')
    linkA.setAttribute('href',link)
    linkA.append(linkH5)
    let resultTitleA=document.createElement('a')
    resultTitleA.setAttribute('href',link)
    let resultTitleH2=document.createElement('h2')
    resultTitleH2.innerHTML=title
    resultTitleA.append(resultTitleH2)
    let highlightP=document.createElement('p')
    highlightP.innerHTML=highlight
    
    outerDiv.append(linkA)
    outerDiv.append(resultTitleA)
    outerDiv.append(highlightP)

    searchResultsContainer.appendChild(outerDiv)
}

createSearchResult("Ola","isto é o highlight","https://google.pt")

