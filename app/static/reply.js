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