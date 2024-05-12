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

// Calculates the time since posting, and returns a formatted string
function calcTimeAgo(timestamp) {
    const secondsAgo = Math.floor((Date.now() / 1000) - timestamp);
    
    const intervals = [
        { label: 'year', seconds: 31536000 },
        { label: 'month', seconds: 2592000 },
        { label: 'day', seconds: 86400 },
        { label: 'hour', seconds: 3600 },
        { label: 'minute', seconds: 60 }
    ];

    for (let i = 0; i < intervals.length; i++) {
        const interval = intervals[i];
        const count = Math.floor(secondsAgo / interval.seconds);

        if (count > 0) {
            return count === 1 ? `1 ${interval.label} ago` : `${count} ${interval.label}s ago`;
        }
    }

    return 'Just now';
}
// Example usage:
const unixTimestamp = 1619499000; // Replace this with your Unix timestamp
console.log(timeAgo(unixTimestamp));
