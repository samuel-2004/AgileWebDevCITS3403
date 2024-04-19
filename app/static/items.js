// show item information when image is clicked
document.getElementById('item-image').addEventListener('click', function() {
    var itemInfo = document.getElementById('item-info');
    if (itemInfo.style.display === 'none') {
        itemInfo.style.display = 'block';
    } else {
        itemInfo.style.display = 'none';
    }
});
