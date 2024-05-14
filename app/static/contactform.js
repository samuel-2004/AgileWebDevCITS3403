function validateEmail() {
    const email_input = document.forms.contactform.email.value;
    if (/([^\.\s]+\.)*[^\.\s]+@[^\.\s][^\.\s]*(\.[^\.\s]*)+/.test(email_input))
    {
        return true;
    }
    alert("You have entered an invalid email address!");
    return false;
}
