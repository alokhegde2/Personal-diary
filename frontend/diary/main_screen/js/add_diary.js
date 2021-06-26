const form = document.getElementById("form");
const title = document.getElementById("title");
const description = document.getElementById("description");
const error = document.getElementById("error");
const snack = document.getElementById("snackbar");


var isError = false;

const user_id = localStorage.getItem("user_id");
const api = "http://127.0.0.1:5000/diary";

//Show input error message
function showError(input, message) {
    const formControl = input.parentElement;
    formControl.className = "form-control error";
    const small = formControl.querySelector("small");
    small.innerText = message;
}

//Show success outline
function showSuccess(input) {
    const formControl = input.parentElement;
    formControl.className = "form-control success";
    const small = formControl.querySelector("small");
    small.innerText = "";
}

//Get fieldname
function getFieldName(input) {
    return input.id.charAt(0).toUpperCase() + input.id.slice(1);
}


//check required fields
function checkRequired(inputArr) {
    inputArr.forEach((input) => {
        if (input.value.trim() === "") {
            showError(input, `${getFieldName(input)} is required`);
            isError = true;
        } else {
            showSuccess(input);
            isError = false;
        }
    });
}

//creating new diary
async function createDiary(title, description) {
    const response = await fetch(`${api}/new-diary`, {
        method: "POST",
        body: JSON.stringify({
            title: title.value,
            description: description.value,
            user_id: user_id
        }),
        headers: {
            "Content-type": "application/json",
        },
    });
    const data = await response.json();
    if (response.status === 200) {
        error.innerText = "";
        snack.className = "show";
        snack.innerText = "Diary Created Successfully"
        // After 3 seconds, remove the show class from DIV
        setTimeout(function () { snack.className = snack.className.replace("show", ""); }, 3000);
        window.location.assign("../html/main.html");
        // location.reload();
    } else if (response.status === 400) {
        error.innerText = "";
        snack.className = "show";
        snack.innerText = `${data.message}`
        console.log(data);
        // After 3 seconds, remove the show class from DIV
        setTimeout(function () { snack.className = snack.className.replace("show", ""); }, 3000);
    } else {
        error.innerText = "";
        snack.className = "show";
        snack.innerText = "Diary is not created"
        // After 3 seconds, remove the show class from DIV
        setTimeout(function () { snack.className = snack.className.replace("show", ""); }, 3000);

    }
}

//handling form submit
form.addEventListener("submit", function (e) {
    e.preventDefault();
    checkRequired([title, description]);
    if (!isError) {
        createDiary(title, description);
    }
})