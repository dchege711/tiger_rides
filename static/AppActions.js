/**
 * @description Reload information about the user's trips and display them on 
 * the current page.
 * 
 * @param {string} userID The id associated with this user
 * @param {boolean} get_user_owned If true, fetch only the trips
 * that the user owns, otherwise, fetch all the trips associated with the user
 */
function refreshTrips(userId, get_user_owned) {
    var mainBody = document.getElementById("logged_in_contents");
    mainBody.innerHTML = `<p>These are your trips</p>
                <div class='w3-responsive'> <table class='w3-table-all' id="user_owned_trips"> <tr>
                <th>Trip ID</th><th>Origin</th><th>Destination</th><th>Date of Departure</th>
                <th>Time of Departure</th><th>Num Seats Still Available</th><th>Edit</th></tr></table></div>`;

    var payload = { "user_id": userId, "get_user_owned": get_user_owned }

    makeHttpRequest("POST", "/read_trips/", payload, function (results) {
        var tableElement = document.getElementById("user_owned_trips");
        for (let i = 0; i < results.length; i++) {
            tableElement.insertAdjacentHTML("beforeend", results[i]["html_version"]);
        }
    });

    return false;
}


