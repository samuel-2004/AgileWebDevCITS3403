//Adapted from https://www.w3schools.com/js/js_ajax_intro.asp
function loadQuote() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
      let result = JSON.parse(this.responseText);
      console.log(result[0].content);
    }
   /*  xhttp.open("GET","https://quotesondesign.com/wp-json/wp/v2/posts/?orderby=rand");
    //xhttp.setRequestHeader('Content-Type', 'application/json'); */

    xhttp.open("GET", "https://api.quotable.io/quotes/random", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
  }

window.onload = () => {loadQuote()}