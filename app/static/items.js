/*
// show item information when image is clicked
document.getElementById('item-image').addEventListener('click', function() {
    var itemInfo = document.getElementById('item-info');
    if (itemInfo.style.display === 'none') {
        itemInfo.style.display = 'block';
    } else {
        itemInfo.style.display = 'none';
    }
});
*/


// Add onclick method that redirects user to the item's page
function openItemPage(event, nID) {
    var ref = "./item/" + nID;
    if(event.ctrlKey || event.metaKey){
        window.open(ref, "_blank");
    } else {
        window.location.href = ref;   
    }
}

// When user starts typing in the search box in the navbar
function typingStarted() {
    document.getElementById('navbarsearch').classList.add("w-75");
}

// When user stops typing in the search box in the navbar
function doneTyping() {
    document.getElementById('navbarsearch').classList.remove("w-75");
}

// When the search box is focused
function onFocus() {
    document.getElementById('navbarsearch').classList.add("w-75");
}

function expandSearchBar() {
    const searchInput = document.getElementById('navbarsearchbox');

    let typingTimer;
    const doneTypingInterval = 3000;


    // Event listener for input event (typing)
    searchInput.addEventListener('input', function() {
        clearTimeout(typingTimer);
        typingStarted(); // Perform action when user starts typing
        typingTimer = setTimeout(doneTyping, doneTypingInterval);
    });

    // Event listener for blur event (unfocused)
    searchInput.addEventListener('blur', function() {
        clearTimeout(typingTimer);
        doneTyping(); // Perform action when the search box is unfocused
        typingTimer = setTimeout(doneTyping, doneTypingInterval);
    });

    // Event listener for focus event
    searchInput.addEventListener('focus', function() {
        clearTimeout(typingTimer);
        onFocus();
        typingTimer = setTimeout(doneTyping, doneTypingInterval);
    });
}

$( document ).ready(function() {
    expandSearchBar();
});