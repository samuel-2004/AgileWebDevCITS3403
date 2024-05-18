
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

function validatePassword() {
    let input = document.getElementById("password")
    if (input.value.length > 64) {
        alert('Max password length is 64 characters');
        input.value = '';
    }
}

window.onload = () => {
    let username_input = document.getElementById("username")
    username_input.addEventListener('change',validateUsername,false)

    let password_input = document.getElementById("password")
    password_input.addEventListener('change',validatePassword,false)
}
