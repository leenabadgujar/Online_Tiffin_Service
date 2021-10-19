const city = document.getElementById('city');
const address = document.getElementById('address');
const code = document.getElementById('code');
const cuisine = document.getElementById('cuisine');
const cost = document.getElementById('cost');
const from = document.getElementById('from');
const till = document.getElementById('till');
const delivery1 = document.getElementById('delivery1');
const delivery2 = document.getElementById('delivery2');
const loc = document.getElementById('loc');
const open_status1 = document.getElementById('open_status1');
const open_status2 = document.getElementById('open_status2');
const img1 = document.getElementById('img1');
const img2 = document.getElementById('img2');
const choose_img1 = document.getElementById('choose_img1');
const choose_img2 = document.getElementById('choose_img2');
const button = document.getElementById('submit');

const formFill = () => {
    if (img1.value) {
        choose_img1.classList.remove('d-none');
        choose_img1.src = URL.createObjectURL(img1.files[0]);
    }
    if (img2.value) {
        choose_img2.classList.remove('d-none');
        choose_img2.src = URL.createObjectURL(img2.files[0]);
    }
    if (city.value && address.value && code.value && cuisine.value && cost.value && loc.value && from.value && till.value && img1.value && img2.value && (delivery1.checked || delivery2.checked) && (open_status1.checked || open_status2.checked) ) 
    {
        button.disabled = false;
    }
    else{
        button.disabled = true;
    }
};

addEventListener('change', formFill);
addEventListener('keyup', formFill);