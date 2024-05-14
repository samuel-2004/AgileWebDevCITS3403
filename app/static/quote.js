// Adapted from https://www.w3schools.com/js/js_ajax_intro.asp
function getQuote() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        let result = JSON.parse(this.responseText);
        loadQuote(result[0]);
    }
    xhttp.open("GET", "https://api.quotable.io/quotes/random?tags=inspirational&maxLength=100", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();

}

async function loadQuote(quote){
    while (document.readyState != "complete"){} // Ensures window is loaded
    let quoteText = quote.content+"<br>- "+quote.author;
    let quoteElement = $("<h3></h3>").html(quoteText);
    $("#content").prepend(quoteElement);
}

getQuote(); // Can run before window.onload for faster retrieval
