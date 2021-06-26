const date_form = document.getElementById("date-form");
const date = document.getElementById("date");
const name_form = document.getElementById("name-form");
const title = document.getElementById("title");
const diary_button = document.getElementById("diary-button");
const error = document.getElementById("error");
const snack = document.getElementById("snackbar")


//Some constatnts
const user_id = "8148363d-d5d7-11eb-bcdf-405bd84ec4ce";
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

//Search by date

async function searchByDate(date) {
    const response = await fetch(`${api}/search-by/date/${user_id}`, {
        method: "POST",
        body: JSON.stringify({
            created_date: date
        }),
        headers: {
            "Content-type": "application/json",
        },
    })
    //Getting json data from response
    const data = await response.json();
    if (response.status === 200) {
        diary_button.innerHTML = data.diary.map(
            (diary, index) => `
            <div class="row">
                            <div class="col diary-text">
                                <h5>${diary.name} </h5>
                                <p>${truncateString(diary.description, 150)}</p>
                            </div>
                            <button class="col-auto mt-3 ml-5 delete" onClick = "deleteButtonClicked('${diary.note_id}')">
                                <i class="far fa-trash-alt fa-2x"></i>
                            </button>
                        </div>
                      <hr>
            `
        ).join(" ")
        error.innerHTML ="";

    } else if (response.status === 400) {
        diary_button.innerHTML = ""
        error.innerHTML = "<h6>No match found</h6> "

    }
}

//Search by name

async function searchByName(name) {
    const response = await fetch(`${api}/search-by/name/${user_id}`, {
        method: "POST",
        body: JSON.stringify({
            name: name
        }),
        headers: {
            "Content-type": "application/json",
        },
    });
    //Getting json data from response
    const data = await response.json();
    if (response.status === 200) {
        diary_button.innerHTML = data.diary.map(
            (diary, index) => `
            <div class="row">
                            <div class="col diary-text">
                                <h5>${diary.name} </h5>
                                <p>${truncateString(diary.description, 150)}</p>
                            </div>
                            <button class="col-auto mt-3 ml-5 delete" onClick = "deleteButtonClicked('${diary.note_id}')">
                                <i class="far fa-trash-alt fa-2x"></i>
                            </button>
                        </div>
                      <hr>
            `
        ).join(" ");
        error.innerHTML ="";
    } else if (response.status === 400) {
        diary_button.innerHTML = ""
        error.innerHTML = "<h6>No match found</h6> "
    }
}

//Delete button event listner

async function deleteButtonClicked(note_id) {
    console.log(`${api}/delete-diary/${note_id}/${user_id}`)
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


//Search by date event listner
date_form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (date.value === "") {
    } else {
        console.log(date.value);
        searchByDate(date.value)
    }
})

//Search by name/title of diary event listner
name_form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (title.value === "") {

    } else {
        searchByName(title.value);
    }
})