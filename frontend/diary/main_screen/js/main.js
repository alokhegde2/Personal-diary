const addDiary = document.getElementById("add");
const searchDiary = document.getElementById("search");
const user = document.getElementById("user");
const diary_button = document.getElementById("diary-button");
const error_msg = document.getElementById("error")

const user_id = "8148363d-d5d7-11eb-bcdf-405bd84ec4ce";

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
    const response = await fetch(`http://127.0.0.1:5000/diary/all-diary/${user_id}`);
    var data = await response.json();
    console.log(data.diary)
    if (response.status === 200) {
        diary_button.innerHTML = data.diary.map(
            diary => `
            <div class="row">
                            <div class="col diary-text">
                                <h4>${diary.name} </h4>
                                <p>${truncateString(diary.description, 150)}</p>
                            </div>
                            <div class="col-auto mt-3 ml-4">
                                <i class="far fa-trash-alt fa-3x"></i>
                            </div>
                        </div>
                        <hr>
            `
        ).join(" ")
    } else if (response.status = 400) {
        error_msg.innerHTML = `<spam>${data.message}</spam>`
    }

}