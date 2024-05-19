
function validateUsername() {
    let input = document.getElementById("username")
    if (input.value.length > 64) {
        alert('Max username length is 64 characters');
        input.value = '';
    }
    if (input.value.length < 4) {
        alert('Min username length is 4 characters');
        input.value = '';
    }
}

function validateEmail() {
    let input = document.getElementById("email")
    if (/([^\.\s]+\.)*[^\.\s]+@[^\.\s][^\.\s]*(\.[^\.\s]*)+/.test(input.value) && input.value.length < 128) {
        return true;
    }
    else {
        alert("You have entered an invalid email address!");
        input.value = '';
    }
}

function validatePassword() {
    let input = document.getElementById("password")
    if (input.value.length > 64) {
        alert('Max password length is 64 characters');
        input.value = '';
    }
    else if (input.value.length < 6) {
        alert('Min password length is 6 characters');
        input.value = '';
    }
}

function validateAddress_line1() {
    let input = document.getElementById("address_line1")
    if (input.value.length > 64) {
        alert('Max address length is 64 characters');
        input.value = '';
    }
    if (input.value.length < 2) {
        alert('Min address length is 2 characters');
        input.value = '';
    }
}

function validateAddress_line2() {
    let input = document.getElementById("address_line2")
    if (input.value.length > 64) {
        alert('Max address length is 64 characters');
        input.value = '';
    }
}

function validateSuburb() {
    let input = document.getElementById("suburb")
    if (input.value.length > 32) {
        alert('Max suburb length is 32 characters');
        input.value = '';
    }
}

function validatePostcode() {
    let input = document.getElementById("postcode")
    if (input.value.length != 4) {
        alert('Postcode is 4 characters');
        input.value = '';
    }
}

function validateCity() {
    let input = document.getElementById("city")
    if (input.value.length > 32) {
        alert('Max city length is 32 characters');
        input.value = '';
    }
}

window.onload = () => {
    let username_input = document.getElementById("username")
    username_input.addEventListener('change',validateUsername,false)

    let email_input = document.getElementById("email")
    email_input.addEventListener('change',validateEmail,false)

    let password_input = document.getElementById("password")
    password_input.addEventListener('change',validatePassword,false)

    let address1_input = document.getElementById("address_line1")
    address1_input.addEventListener('change',validateAddress_line1,false)

    let address2_input = document.getElementById("address_line2")
    address2_input.addEventListener('change',validateAddress_line2,false)

    let postcode_input = document.getElementById("postcode")
    postcode_input.addEventListener('change',validatePostcode,false)

    let city_input = document.getElementById("city")
    city_input.addEventListener('change',validateCity,false)
}
