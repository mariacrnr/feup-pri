const searchButton = document.getElementById('search-button');
const randomButton = document.getElementById('random-query');
const searchInput = document.getElementById('search-input');
const partyInput = document.getElementById('party-filter');
const dateFromInput = document.getElementById('start-date-filter');
const dateToInput = document.getElementById('end-date-filter');


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

randomButton.addEventListener('click', (event) => {
    event.preventDefault();
});
