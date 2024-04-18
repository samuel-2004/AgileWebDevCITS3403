    /*
    This JavaScript code defines a class called Item, which represents items on offer.
    These items are retreieved with a get request from the server.
    The JSON provided by the server is parsed into these objects for easier manipulation.
    The class method `displayItem` creates an HTML element to be displayed.

    Also contained in this file is a method to sort the items based on an input order.
    This saves the server from doing this, reducing the load.

    The code also includes a window onload event listener that displays the items onto the page.

    Note: The code uses jQuery for DOM manipulation.
    */

class Item {
    constructor(nID, name, who, suburb, ref, timestamp) {
        this.nID = nID;
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

        //Add a link to go to the item's page
        elemDiv.addEventListener('click', (e) => {
            var ref = "./item.html?" + this.nID;
            if(e.ctrlKey || e.metaKey){
                window.open(ref, "_blank");
            } else {
                location.href = ref;   
            }
        });

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
    //Get page name
    var path = window.location.pathname;
    var page = path.split("/").pop();

    //var where=document.getElementById("where").value

    //The following code is temporary and used for debugging
    //Create a generic list of items
    //this will need to change to GET information from server
    const itemsList = [];
    li = JSON.parse('[{"nID":87241,"name":"Rice Cooker","who":"John Smith","suburb":"Downtown","imageref":"","timestamp":1679776345},{"nID":52379,"name":"Smartphone","who":"Emily Johnson","suburb":"Midtown","imageref":"","timestamp":1679818345},{"nID":10294,"name":"Laptop","who":"Michael Brown","suburb":"Uptown","imageref":"","timestamp":1679762345},{"nID":40957,"name":"Bicycle","who":"Sarah Davis","suburb":"Eastside","imageref":"","timestamp":1679790345},{"nID":78526,"name":"Television","who":"DavnID Wilson","suburb":"Westside","imageref":"","timestamp":1679720345},{"nID":63081,"name":"Coffee Maker","who":"Jessica Martinez","suburb":"Downtown","imageref":"","timestamp":1679804345},{"nID":21789,"name":"Headphones","who":"Christopher Lee","suburb":"Midtown","imageref":"","timestamp":1679748345},{"nID":95873,"name":"Backpack","who":"Jennifer Thompson","suburb":"Uptown","imageref":"","timestamp":1679734345},{"nID":37402,"name":"Digital Camera","who":"Daniel Garcia","suburb":"Eastside","imageref":"","timestamp":1679822345},{"nID":69023,"name":"Printer","who":"Olivia Hernandez","suburb":"Westside","imageref":"","timestamp":1679706345},{"nID":18396,"name":"Blender","who":"William Rodriguez","suburb":"Downtown","imageref":"","timestamp":1679692345},{"nID":54127,"name":"Smart Watch","who":"Ava Wilson","suburb":"Midtown","imageref":"","timestamp":1679678345},{"nID":76258,"name":"Gaming Console","who":"Ethan Moore","suburb":"Uptown","imageref":"","timestamp":1679664345},{"nID":89501,"name":"Tablet","who":"Sophia Anderson","suburb":"Eastside","imageref":"","timestamp":1679650345},{"nID":32095,"name":"Microwave Oven","who":"James Taylor","suburb":"Westside","imageref":"","timestamp":1679636345},{"nID":61478,"name":"Fitness Tracker","who":"Mia Thomas","suburb":"Downtown","imageref":"","timestamp":1679622345},{"nID":94602,"name":"Portable Speaker","who":"Benjamin White","suburb":"Midtown","imageref":"","timestamp":1679608345},{"nID":25814,"name":"Vacuum Cleaner","who":"Isabella Martinez","suburb":"Uptown","imageref":"","timestamp":1679594345},{"nID":70183,"name":"Kitchen Scale","who":"Alexander Johnson","suburb":"Eastside","imageref":"","timestamp":1679580345},{"nID":18347,"name":"Digital Watch","who":"Charlotte Brown","suburb":"Westside","imageref":"","timestamp":1679566345}]');
    for (var i = 0; i < 20; i++) {
        itemsList.push(new Item(li[i].nID, li[i].name, li[i].who, li[i].suburb, li[i].imageref, li[i].timestamp));
    }

    //Sort the list
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