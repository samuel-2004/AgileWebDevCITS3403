class Item {
    constructor(name, who, suburb, ref, timestamp) {
        this.name = name;
        this.who = who;
        this.suburb = suburb;
        this.imageref = ref;
        this.timestamp = timestamp;
    }
    isItem() {
        return true;
    }
    getTimeStamp() {
        return this.timestamp;
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
            img.src = "book.jpg"; //default
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

function sortItems(itemsList, order) {
    //Check itemsList is a valid list
    if (!Array.isArray(itemsList)) {
        return false;
    }
    $.each(itemsList, function( index, item ) {
        if (!item.isItem()) {
            return false;
        }
    });

    //Sort the list by the order given
    order = order.toLowerCase();
    switch (order) {
        case "newest":
            itemsList = itemsList.sort(function(a, b) {
                return a.getTimeStamp() - b.getTimeStamp();
            });
            break;
        case "oldest":
            itemsList = itemsList.sort(function(a, b) {
                return b.getTimeStamp() - a.getTimeStamp();
            });
            break;
        case "closest":
            // to implement
            break;
        case "vendor+rating":
            // to implement
            break;
        default: // Order is not an acceptable value
            return false;
    }

    return true;
}

window.onload = (event) => {
    //The following code is temporary and used for debugging
    //Create a generic list of items
    //this will need to change to GET information from server
    const itemsList = [];
    for (var i = 0; i < 20; i++) {
        itemsList.push(new Item(li[i].name, li[i].who, li[i].suburb, li[i].imageref, li[i].timestamp));
    }

    //Sort the list
    var path = window.location.pathname;
    var page = path.split("/").pop();
    console.log(page);
    var order = "newest"
    if (page == "index.html") {
        order = "newest";
    }
    sortItems(itemsList, order);

    //If home page: display all
    //If search page: only display items that fit the search criteria
    $.each(itemsList, function( index, item ) {
        item.displayItem();
    });
};