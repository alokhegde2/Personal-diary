const register = document.getElementById('register')



//on click on register 
register.addEventListener('click',function(e) {
    e.preventDefault();
    window.location.assign("../html/register.html")
})