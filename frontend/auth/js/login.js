const register = document.getElementById('register')
const form = document.getElementById('form');
const email = document.getElementById('email');
const password = document.getElementById('password');



//Show input error message
function showError(input,message){
    const formControl = input.parentElement;
    formControl.className = 'form-control error';
    const small = formControl.querySelector('small');
    small.innerText = message
}

//Show success outline
function showSuccess(input) {
    const formControl = input.parentElement;
    formControl.className = 'form-control success'
}

//check required fields
function checkRequired(inputArr) {
    inputArr.forEach(input => {
        if (input.value.trim() === "") {
            showError(input,`${getFieldName(input)} is required`)
        } else {
            showSuccess(input)
        }
    });
}

//Get fieldname
function getFieldName(input) {
    return input.id.charAt(0).toUpperCase()+input.id.slice(1);
}

//on click to submit
form.addEventListener('submit',function(e) {
    e.preventDefault();
    checkRequired([email,password]);
    console.log("Submited")
});

//on click on register 
register.addEventListener('click',function(e) {
    e.preventDefault();
    window.location.assign("../html/register.html")
})