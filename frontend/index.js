const login = document.getElementById('login');
const register = document.getElementById('register');

//Handling login button click event
login.addEventListener('click',function(e) {
    e.preventDefault();
    window.location.assign("./auth/html/login.html")
})

//Handling login button click event
register.addEventListener('click',function(e) {
    e.preventDefault();
    window.location.assign("./auth/html/register.html")
})