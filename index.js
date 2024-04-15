var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.7.1.min.js';
document.getElementsByTagName('head')[0].appendChild(script);

class Item {
    constructor(name, who, suburb, ref) {
        this.name = name;
        this.who = who;
        this.suburb = suburb;
        this.imageref = ref;
    }
    displayItem() {
        // Create a div element
        var elemDiv = document.createElement("div");
        elemDiv.id = "someid";
        elemDiv.classList.add("anItem");
        elemDiv.classList.add("col-lg-2");
        elemDiv.classList.add("col-md-3");
        elemDiv.classList.add("col-sm-5");
        elemDiv.classList.add("col-xs-6");

        // Create an image element
        const img = document.createElement("img");
        img.src = this.imageref;

        // Create paragraph elements for name, suburb, and who
        const text = document.createElement("p");
        text.textContent = `Name: ${this.name}\nSuburb: ${this.suburb}\nWho: ${this.who}`

        // Append image and paragraphs to the div
        elemDiv.appendChild(img);
        elemDiv.appendChild(text);
        
        // Append the div to the document body
        //document.body.appendChild(elemDiv);
        $('#mainContent').append(elemDiv);
    }
}
