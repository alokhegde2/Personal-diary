const addDiary = document.getElementById("add");
const searchDiary = document.getElementById("search");
const user = document.getElementById("user");
const diary_button = document.getElementById("diary-button");
const error_msg = document.getElementById("error")
const delete_button = document.getElementById("delete");
const developer = document.getElementById("developer");
const snack = document.getElementById("snackbar")
const spinner = document.getElementById("spinner");

const user_id = localStorage.getItem("user_id");
const api = "http://127.0.0.1:5000/diary";

//To truncate the description
function truncateString(str, num) {
    // If the length of str is less than or equal to num
    // just return str--don't truncate it.
    if (str.length <= num) {
        return str
    }
    // Return str truncated with '...' concatenated to the end of str.
    return str.slice(0, num) + '...'
}

//to get fetch the diary when page is loaded

window.onload = async function fetchDiary() {
    const response = await fetch(`${api}/all-diary/${user_id}`);
    var data = await response.json();
    console.log(data.diary)
    if (response.status === 200) {
        spinner.className = "d-none";
        diary_button.innerHTML = data.diary.map(
            (diary) => `
            <div class="row">
                            <div class="col diary-text">
                                <a href="../html/diary_details.html?${diary.note_id}"><h5>${diary.name} </h5></a>
                                <p>${truncateString(diary.description, 150)}</p>
                            </div>
                            <button class="col-auto mt-3 ml-5 delete" onClick = "deleteButtonClicked('${diary.note_id}')">
                                <i class="far fa-trash-alt fa-2x"></i>
                            </button>
                        </div>
                      <hr>
            `
        ).join(" ")
    } else if (response.status = 400) {
        error_msg.innerHTML = `<spam>${data.message}</spam>`
    }

}

//Handling delete button

async function deleteButtonClicked(note_id) {
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
        location.reload();

        // After 3 seconds, remove the show class from DIV
        setTimeout(function () { snack.className = snack.className.replace("show", ""); }, 3000);
    }
}

//Search diary event listner

searchDiary.addEventListener('click', function (e) {
    e.preventDefault();
    window.location.assign("../html/search.html");

});

//Add diary event listner

addDiary.addEventListener('click', function (e) {
    e.preventDefault();
    window.location.assign("../html/add_diary.html");
});

//Page load 
window.addEventListener( "pageshow", function ( event ) {
    var historyTraversal = event.persisted || ( typeof window.performance != "undefined" && window.performance.navigation.type === 2 );
    if ( historyTraversal ) {
      // Handle page restore.
      //alert('refresh');
      window.location.reload();
    }
  });