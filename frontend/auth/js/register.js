const form = document.getElementById("form");
const username = document.getElementById("username");
const email = document.getElementById("email");
const password = document.getElementById("password");
const password2 = document.getElementById("password2");
const login = document.getElementById("login");
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

//check input length
function checkLength(input, min, max) {
  if (input.value.length < min) {
    showError(
      input,
      `${getFieldName(input)} must be atleast ${min} characters`
    );
    isError = true;
  } else if (input.value.length > max) {
    showError(
      input,
      `${getFieldName(input)} must be less than ${max} characters`
    );
    isError = true;
  } else {
    showSuccess(input);
    isError = false;
  }
}

//Check password match
function checkPasswordsMatch(input1, input2) {
  if (input1.value !== input2.value) {
    showError(input2, "Passwords do not match");
    isError = true;
  } else {
    showSuccess(input1);
    isError = false;
  }
}


//POST request
function doRequest(username, mail, pass) {
  fetch("http://127.0.0.1:5000/user/register", {
    method: "POST",
    body: JSON.stringify({
      email: mail.value,
      name: username.value,
      password: pass.value,
    }),
    headers: {
      "Content-type": "application/json",
    },
  })
    .then(function (response) {
      if (response.ok) {
        error.innerText = "";
        window.location.assign("../html/login.html");  
        return response.json();
      }
      if (response.status == 409) {
        console.log("Email is already registered");
        error.innerText = "Email is already registered";
      }
      return Promise.reject(response);
    })
    .catch(function (error) {
      console.warn("Something went wrong.", error);
    });
}

//Get fieldname
function getFieldName(input) {
  return input.id.charAt(0).toUpperCase() + input.id.slice(1);
}

//Event Listners
form.addEventListener("submit", function (e) {
  e.preventDefault();
  checkRequired([username, email, password, password2]);
  checkLength(username, 3, 15);
  checkLength(password, 6, 15);
  checkPasswordsMatch(password, password2);
  if (!isError) {
    doRequest(username, email, password);
  }
});

//on click on login
login.addEventListener("click", function (e) {
  e.preventDefault();
  window.location.assign("../html/login.html");
});
