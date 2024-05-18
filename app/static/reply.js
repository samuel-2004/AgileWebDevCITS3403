// Enlarges the post when clicked
function enlargepost(img) {
    img.style.width = "50%";
    img.style.height = "auto";
    img.style.transition = "width 0.5s ease";
}
// Function to handle the request button click
function requestItem(button) {
    // Toggle button text
    if (button.innerText === "I want this item!") {
        button.innerText = "Item requested! Please wait for uploader to respond";
    }
}

// validate user reply so that it is not exceeding 256 characters
function validateReply() {
    let input = document.getElementById("message")
    if (input.value.length > 256) {
        alert('Max description length is 256 characters');
        input.value = '';
     }
}

window.onload = () => {
    let reply_input = document.getElementById("message")
    desc_input.addEventListener('change',validateReply,false)
}