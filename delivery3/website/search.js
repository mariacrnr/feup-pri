const url = window.location.search;
const urlParams = new URLSearchParams(url);

const query = urlParams.get('q')
alert(query);
// shirt
