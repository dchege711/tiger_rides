function loadSplash(){

    var username = getCookie("username");
    if (username != "") {
        alert("Welcome Back " + username);
    } else {
        username = prompt("Please enter your name:", "");
        if (username != "" && username != null) {
            setCookie("username", username, 365);
        }
    }
}
