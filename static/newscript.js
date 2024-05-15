console.log('Script Loaded!');

function loadDoc(url, func) {
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if (xhttp.status != 200){
            console.log("Error");
        }else{
            func(xhttp.response);
        }
    }
    xhttp.open("GET" , url);
    xhttp.send();
}
function signup(){
    let email = document.getElementById('txtEmail').value;
    let username = document.getElementById('txtName').value;
    let password = document.getElementById('txtPassword').value;
    //let URL = "/signup?email=" + email + "&username=" + username + "&password=" + password;
    if (username === '' || password === '') {
        alert("Username and password cannot be blank");
        return;
    }
    let URL= `/signup?email=${email}&username=${username}&password=${password}`;


    loadDoc(URL, signup_response);
}


function signup_response(response) {
    console.log("Response:", response); // Log the response data
    let data = JSON.parse(response);
    let result = data["result"];
    console.log("Result:", result); // Log the result value

    if (result === "OK") {
        let username = data["username"];
        console.log("Redirecting to profile for username:", username); // Log the username for redirection
        window.location.href = "/profile/" + username;
    }
    else {
        alert(result);
    }
}



function login() {
    let username = document.getElementById('txtName').value;
    let password = document.getElementById('txtPassword').value;
    let URL = "/login?username=" + username + "&password=" + password;

    loadDoc(URL, login_response);
}


function login_response(response) {
    console.log("Response:", response); // Log the response data
    let data = JSON.parse(response);
    console.log("Parsed Data:", data); // Log the parsed JSON data
    let result = data["result"];
    console.log("Result:", result); // Log the result value

    if (result === "OK") {
        let username = data["username"];
        console.log("Redirecting to profile for username:", username); // Log the username for redirection
        window.location.href = "/profile/" + username;
    } else if(result === "Missing username or password"){
        alert("Fill all text fields");
    }
    else if(result === "Username not found"){
        alert("Login failed. Username not found.");
    }
    else{
        alert("Login failed. Incorrect password");
    }
}
function postReply(){

    let text = document.getElementById('text').value;
    let pid = document.getElementById('pid').value;
    let URL = "/post_reply?text=" + text + "&pid=" + pid;

    loadDoc(URL, post_reply_response);
}

function  post_reply_response(response){
    let data = JSON.parse(response);
    let result = data["result"];

    location.reload();
}
function list_replies(post_id) {
    let url = '/list_replies?parent_id=' + post_id; // Adjust the URL to include the post_id
    loadDoc(url, list_post_replies_response);
}
function list_post_replies_response(response) {
    let data = JSON.parse(response);
    let results = data['result'];
    //let parent_id = data['parent_id'];
    console.log(data);
    let divResults = document.getElementById("results");

    let temp = "";
    for (let i = 0; i < results.length; i++) {
        let item = results[i];
        //temp += '<p>' + item["text"] + '</p><br>';
        temp += '<p><strong>' + item["username"] + '</strong>: ' + item["text"] + '</p><br>';

    }
    divResults.innerHTML = temp;
}




function postEntry(){
    let text = document.getElementById('text').value;
    let URL = "/post_entry?text=" + text;

    loadDoc(URL, post_entry_response);
}
function  post_entry_response(response){
    let data = JSON.parse(response);
    let result = data["result"];

    location.reload();
}
function list_post_files(username) {
    let url = '/list_post/' + username; // Adjust the URL to include the username
    loadDoc(url, list_post_response);
}

function list_post_response(response) {
    let data = JSON.parse(response);
    let results = data['result'];
    let username = data['username'];
    console.log('Username:', username);
    let divResults = document.getElementById("divResults");

    let temp = "";
    for (let i = 0; i < results.length; i++) {
        let item = results[i];
        temp += '<div class="listposts">';
        temp += '<p>' + item["text"] + '</p> <br>';
        temp += '</div>'
    }
    divResults.innerHTML = temp;
}


function list_recent_posts() {
    let url = '/list_recent_posts';
    loadDoc(url, list_recent_posts_response);
}

function list_recent_posts_response(response) {
    let data = JSON.parse(response);
    let results = data['result'];
    let divResults = document.getElementById("divResults");

    let temp = "";
    for (let i = 0; i < results.length; i++) {
        let item = results[i];
        // Create a card-like structure for each post
        temp += '<div class="post-card-post-container">';
        temp += '<div class="post-card-post">';
        temp += '<img src="' + item["image_url"] + '" style="width:100px;text-align:left;"/>';
        temp += '<h3><a href="#" onclick="loadProfile(\'' + item["username"] + '\')">' + '@' + item["username"] + '</a></h3>'; // Display username with link
        temp += '<p>' + item["text"] + '</p>'; // Display text
        temp += '<a href =/post/' + item["post_id"]  + '>reply</a>';
        temp += '</div>'; // Close post-card div
        temp +='</div>'
    }
    divResults.innerHTML = temp;
}


function loadProfile(username) {
    let url = '/profile/' + username; // Construct the URL for the user's profile page
    window.location.href = url; // Redirect the user to the profile page
}



function list_files(){
    let url ='/listfiles';
    loadDoc(url,list_files_response);
}

function list_files_response(response){
    let data = JSON.parse(response);
    let items = data["items"];
    let url = data["url"];

    let temp = "";
    for (let i = 0; i <items.length; i++){
        temp += "<a href=\"" + url + "/" +items[i] + "\">" + items[i] + "</a><br>";
    }

    let divResults = document.getElementById("divResults");
    divResults.innerHTML = temp;
}

function upload_photo() {
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if (xhttp.status != 200) {
            console.log("Error");
        } else {
            upload_photo_response(xhttp.response);
        }
    }

    xhttp.open('POST','/uploadfile',true);
    var formData = new FormData();
    formData.append("file", document.getElementById('file').files[0]);
    xhttp.send(formData);
}

function upload_photo_response(response) {
    let data = JSON.parse(response);
    if (data.results === 'OK') {
        // Get the URL of the uploaded image
        let imageUrl = data.image_url;

        // Update the src attribute of the profile picture
        document.getElementById('profilePic').src = imageUrl;
        document.getElementById('file').value = "";
    }
}
function upload_file() {
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if (xhttp.status != 200) {
            console.log("Error");
        } else {
            upload_file_response(xhttp.response);
        }
    }
    // Provide the condition and body for the if statement
}




/*signup repsonse
 console.log("Response:", response); // Log the response data
    let data = JSON.parse(response);
    console.log("Parsed Data:", data); // Log the parsed JSON data
    let result = data["result"];
    console.log("Result:", result); // Log the result value
    if (result === "BAD") {
        alert("Email is already in use. Try again with a different email.");
    } else if (result === "Invalid email") {
        alert("Email is invalid. Try again.");
    } else if (result === "blank") {
        alert("Fill all text fields.");
    } else if (result === "OK") {
        let username = data["username"];
        console.log("Redirecting to profile for username:", username); // Log the username for redirection
        window.location.href = "/profile?username=" + username;
    }
*/
