class Item {
    constructor(name, who, suburb, ref) {
        this.name = name;
        this.who = who;
        this.suburb = suburb;
        this.imageref = ref;
        this.timestamp = timestamp;
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
        if (this.imageref != "") {
            img.src = this.imageref;
        } else {
            img.src = "book.jpg";
        }

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

window.onload = (event) => {
    //The following code is temporary and used for debugging
    //Create a generic list of items
    //this will need to change to GET information from server
    const itemsList = [];
    for (var i = 0; i < 20; i++) {
        console.log(i);
        console.log(li[i]);
        itemsList.push(new Item(li[i].name, li[i].who, li[i].suburb, li[i].imageref, li[i].timestamp));
    }

    //If home page: display all
    //If search page: only display items that fit the search criteria
    $.each(itemsList, function( index, item ) {
        item.displayItem();
    });
};