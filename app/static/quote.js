//Adapted from https://www.w3schools.com/js/js_ajax_intro.asp
function getQuote() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        let result = JSON.parse(this.responseText);
        loadQuote(result[0])
        console.log(result[0])
    }
    xhttp.open("GET", "https://api.quotable.io/quotes/random?tags=inspirational&maxLength=100", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
}

function loadQuote(quote){
    //let quoteText = quote.content+"<br>- "+quote.author
    let quoteText = $("<h3></h3>").html(quote.content);
    quoteText.addClass("quote");

    let quoteAuthor = $("<h5></h5>").html("- "+ quote.author);
    quoteAuthor.addClass("quote");

    let quoteTextDiv = $("<div></div>")
    quoteTextDiv.addClass("d-flex justify-content-center");
    let quoteAuthorDiv = $("<div></div>")
    quoteAuthorDiv.addClass("d-flex justify-content-center");

    $("#content").prepend(quoteAuthorDiv);
    $("#content").prepend(quoteTextDiv);
    quoteTextDiv.append(quoteText);
    quoteAuthorDiv.append(quoteAuthor);
}

window.onload = () => {getQuote();};