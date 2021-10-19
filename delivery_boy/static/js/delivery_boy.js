const DOB = document.getElementById('date');
const city = document.getElementById('city');
const address = document.getElementById('address');
const code = document.getElementById('code');
const experience1 = document.getElementById('experience1');
const experience2 = document.getElementById('experience2');
const license1 = document.getElementById('license1');
const license2 = document.getElementById('license2');
const work1 = document.getElementById('work1');
const work2 = document.getElementById('work2');
const money = document.getElementById('money');
const range = document.getElementById('range');
const vehicle = document.getElementById('vehicle');
const gender = document.getElementById('gender');
const from = document.getElementById('from');
const to = document.getElementById('to');
const button = document.getElementById('submit');

const formFill = () => {
    if (DOB.value && city.value && address.value && code.value && money.value && range.value && vehicle.value && from.value && to.value && gender.value && (experience1.checked || experience2.checked) && (license1.checked || license2.checked) && (work1.checked || work2.checked)) {
        button.disabled = false;
    }
    else{
        button.disabled = true;
    }
};

addEventListener('change', formFill);
addEventListener('keyup', formFill);