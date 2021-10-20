const content = document.getElementById("content");
const message = document.getElementById("message");
const messageText = document.getElementById("message_text");
const fullName = document.getElementById("id_name");
const email = document.getElementById("id_email");
const number = document.getElementById("id_number");
const city = document.getElementById("id_city");
const password1 = document.getElementById("id_password1");
const password2 = document.getElementById("id_password2");
const underline = document.getElementById("underline");
const register = document.getElementById("register");

let checkName = false;
let checkEmail = false;
let checkNumber = false;
let checkCity = false;
let checkPassword1 = false;
let checkPassword2 = false;
password2.setAttribute('disabled', true);

const moveRight = () => {
    message.classList.add("move_right");
    setTimeout(() => {
        message.classList.add("d-none");
    }, 1000)
}

message.addEventListener("click", moveRight);

fullName.addEventListener('keyup', () => {
    message.classList.remove('d-none');
    if(fullName.value){ 
        messageText.innerText = "Valid Name.";
        messageText.style.color = "chartreuse";
        underline.style.background = "chartreuse"; 
        checkName = true;
    }
    else{
        checkName = false;
        messageText.innerText = "Name can't be Empty.";
        messageText.style.color = "red";
        underline.style.background = "red";
    }
});

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

number.addEventListener('keyup', () => {
    message.classList.remove('d-none');
    if (number.value) {
        if(number.value.length == 10)
        {
            checkNumber = true;
            messageText.innerText = "Valid Mobile Number.";
            messageText.style.color = "chartreuse";
            underline.style.background = "chartreuse";
        }
        else{
            checkNumber = false;
            messageText.innerText = "Mobile Number must have 10 digits.";
            messageText.style.color = "red";
            underline.style.background = "red";
        }
    }
    else{
        checkNumber = false;
        messageText.innerText = "Mobile Number can't be Empty.";
        messageText.style.color = "red";
        underline.style.background = "red";
    }
});

password1.addEventListener('keyup', () => {
    message.classList.remove('d-none');
    if (password1.value) {
        var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
        if(strongRegex.test(password1.value))
        {
            password2.removeAttribute('disabled');
            messageText.innerText = "Valid Password.";
            messageText.style.color = "chartreuse";
            underline.style.background = "chartreuse";
            checkPassword1 = true;
        }
        else{
            messageText.innerText = "Password must contain at least 8 digits, 1 numeric, 1 uppercase, 1 Symbolic character.";
            messageText.style.color = "red";
            underline.style.background = "red";
            checkPassword1 = false;
        }
    }
    else{
        messageText.innerText = "Password can't be Empty.";
        messageText.style.color = "red";
        underline.style.background = "red";
        checkPassword1 = false;
    }
});

password2.addEventListener('keyup', () => {
    if(password2.value == password1.value)
    {
        messageText.innerText = "Password Confirm.";
        messageText.style.color = "chartreuse";
        underline.style.background = "chartreuse";
        checkPassword2 = true;
    }
    else{
        messageText.innerText = "Password are not same.";
        messageText.style.color = "red";
        underline.style.background = "red";
        checkPassword2 = false;
    }
});

city.addEventListener('keyup', () => {
    message.classList.remove('d-none');
    if(city.value){ 
        messageText.innerText = "Valid city.";
        messageText.style.color = "chartreuse";
        underline.style.background = "chartreuse"; 
        checkCity = true;
    }
    else{
        checkCity = false;
        messageText.innerText = "City can't be Empty.";
        messageText.style.color = "red";
        underline.style.background = "red";
    }
});

document.addEventListener('keyup', () => {
    (checkEmail && checkName && checkNumber && checkCity && checkPassword1 && checkPassword2) ? register.removeAttribute('disabled') : register.setAttribute('disabled', true);
})