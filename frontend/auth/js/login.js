const register = document.getElementById("register");
const form = document.getElementById("form");
const email = document.getElementById("email");
const password = document.getElementById("password");
const error = document.getElementById("error");

let isError = false;

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

//Get fieldname
function getFieldName(input) {
  return input.id.charAt(0).toUpperCase() + input.id.slice(1);
}

//POST request
async function doRequest(mail, pass) {
  const response = await fetch("http://127.0.0.1:5000/user/login", {
    method: "POST",
    body: JSON.stringify({
      email: mail.value,
      password: pass.value,
    }),
    headers: {
      "Content-type": "application/json",
    },
  });
  var data = await response.json();
  if (response.status == 200) {
    error.innerText = "";
    //Implementing local storage
    // localStorage.setItem('key',"value")
    localStorage.setItem('user_id', data["user_id"])
    window.location.assign("../../diary/main_screen/html/main.html");
    console.log(data["user_id"]);
  } else if (response.status == 403) {
    error.innerText = data["message"];
    console.log(data["message"]);
  } else if (response.status == 404) {
    error.innerText = data["message"];
    console.log(data["message"]);
  }
}

//on click to submit
form.addEventListener("submit", function (e) {
  e.preventDefault();
  checkRequired([email, password]);
  if (!isError) {
    doRequest(email, password);
  }
});

//on click on register
register.addEventListener("click", function (e) {
  e.preventDefault();
  window.location.assign("../html/register.html");
});
