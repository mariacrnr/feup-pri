const searchButton = document.getElementById('search-button');
const searchInput = document.getElementById('search-input');
searchButton.addEventListener('click', (event) => {
    event.preventDefault()
    const inputValue = searchInput.value;
    window.location.href="http://localhost:8080/search-results.html?q="+inputValue
});