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

