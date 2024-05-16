/*
 * This js file gets the client's location (permission required of course)
 * and adds it to the hidden fields in search forms.
 */

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    }
}
  
function showPosition(position) {
    $("input[name=lat]").val(position.coords.latitude);
    $("input[name=lng]").val(position.coords.longitude);
}

getLocation();
