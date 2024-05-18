
//Adapted from https://www.tutorialspoint.com/file-type-validation-while-uploading-it-using-javascript
function validateImage() {
    let input = document.getElementById("image")
    let allowedTypes = ['image/jpeg', 'image/png','image/svg'];
    let file = input.files[0]
    if (!allowedTypes.includes(file.type)) {
        alert('Invalid file type. Please upload a JPEG, PNG, or SVG file.');
        input.value = '';
     }
}

function validateName() {
    let input = document.getElementById("item_name")
    if (input.value.length > 32) {
        alert('Max item name length is 32 characters');
        input.value = '';
     }
}

function validateDesc() {
    let input = document.getElementById("desc")
    if (input.value.length > 256) {
        alert('Max description length is 256 characters');
        input.value = '';
     }
}

window.onload = () => {
    let image_input = document.getElementById("image")
    image_input.addEventListener('change',validateImage,false)

    let item_input = document.getElementById("item_name")
    item_input.addEventListener('change',validateName,false)

    let desc_input = document.getElementById("desc")
    desc_input.addEventListener('change',validateDesc,false)
}
