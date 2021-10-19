const message = document.getElementById("message");
const messageText = document.getElementById("message_text");
const email = document.getElementById("id_email");
const underline = document.getElementById("underline");
const register = document.getElementById("register");
const password = document.getElementById("id_password");

checkEmail = false;
checkPassword = false;

const moveRight = () => {
    message.classList.add("move_right");
    setTimeout(() => {
        message.classList.add("d-none");
    }, 1000)
}

message.addEventListener("click", moveRight);

email.addEventListener('keyup', () => {
    message.classList.remove('d-none');
    if (email.value) {
        if(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email.value))
        {
            checkEmail = true;
            messageText.innerText = "Valid Email Address.";
            messageText.style.color = "chartreuse";
            underline.style.background = "chartreuse";
        }
        else{
            checkEmail = false;
            messageText.innerText = "Invalid Email Address.";
            messageText.style.color = "red";
            underline.style.background = "red";
        }
    }
    else{
        checkEmail = false;
        messageText.innerText = "Email Address can't be Empty.";
        messageText.style.color = "red";
        underline.style.background = "red";
    }
});

password.addEventListener('keyup', () => {
    message.classList.remove('d-none');
    if (password.value) {
        checkPassword = true;
        message.classList.add('d-none');
    }
    else{
        messageText.innerText = "Password can't be Empty.";
        messageText.style.color = "red";
        underline.style.background = "red";
        checkPassword = false;
    }
});

document.addEventListener('keyup', () => {
    (checkEmail && checkPassword) ? register.removeAttribute('disabled') : register.setAttribute('disabled', true);
})