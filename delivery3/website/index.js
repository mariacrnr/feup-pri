const searchButton = document.getElementById('search-button');
const randomButton = document.getElementById('random-query');
const searchInput = document.getElementById('search-input');
searchButton.addEventListener('click', (event) => {
    event.preventDefault();
    const inputValue = searchInput.value;
    window.location.href="http://localhost:8080/search-results.html?q="+inputValue;
});

randomButton.addEventListener('click', (event) => {
    event.preventDefault();
});
