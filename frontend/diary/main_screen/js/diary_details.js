const main_body = document.getElementById("main-body");
const snack = document.getElementById("snackbar")


const user_id = localStorage.getItem("user_id");
const api = "http://127.0.0.1:5000/diary";
const note_id = window.location.href.split("?")[1];

window.onload = async function fetchSingleDiary() {
    const response = await fetch(`${api}/single-diary/${note_id}/${user_id}`);
    const data = await response.json();
    console.log(data)
    if (response.status === 200) {
        main_body.innerHTML = `
        <div class="header">
        <ul>
            <li class="p-3 "><button onClick = updateDiary()><i class="far fa-edit fa-2x"></i></button></li>
            <li class="p-3"><button onClick = deleteDiary()><i class="far fa-trash-alt fa-2x"></i></button></li>
        </ul>
    </div>
    <small>${data.created_date}</small>
    <h5  class="my-3">${data.name}</h5>
    <hr>
    <p>${data.description}</p>
        `
    }
}

function updateDiary() {
    window.location.assign(`../html/update_diary.html?${note_id}`);
}

async function deleteDiary() {
    var response = await fetch(`${api}/delete-diary/${note_id}/${user_id}`, {
        method: "DELETE"
    })

    if (response.status === 400) {
        snack.className = "show";
        snack.innerText = "Unable to delete diary";
        // After 3 seconds, remove the show class from DIV
        setTimeout(function () { snack.className = snack.className.replace("show", ""); }, 3000);
    } else if (response.status === 200) {
        snack.className = "show";
        snack.innerText = "Diary Deleted Successfully"
        window.location.assign("../html/main.html");

        // After 3 seconds, remove the show class from DIV
        setTimeout(function () { snack.className = snack.className.replace("show", ""); }, 3000);
    }
}

//Page load 
window.addEventListener( "pageshow", function ( event ) {
    var historyTraversal = event.persisted || ( typeof window.performance != "undefined" && window.performance.navigation.type === 2 );
    if ( historyTraversal ) {
      // Handle page restore.
      //alert('refresh');
      window.location.reload();
    }
  });