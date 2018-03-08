// Keep track of the different fields required for different forms
var requiredFields = {
    "registration_form": ["first_name", "last_name", "email_address", "password"]
}

/**
 * @description Process the form and send the data to the appropriate url, then execute the callback.
 * 
 * @param {string} formID The document id of the form element
 * @param {string} url The url to which the form data should be sent
 * @param {function} callBack The function to be called on success
 */
function processForm(formID, url) {
    var elements = document.getElementById(formID).elements;
    var missingElements = checkRequired(elements, formID);

    if (missingElements.size >= 1) {
        missingElements.forEach(function (elementName) {
            document.getElementById(elementName).style.border = "thin solid red";
        });
        alert("Please fill in the required fields.");
        return false;
    } else {

        // REGEX obtained from https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/email#Validation
        var emailRegex = /[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*/;
        var emailIsValid = emailRegex.exec(elements["email_address"].value);
        console.log(emailIsValid);

        if (!emailIsValid) {
            alert(elements["email_address"].value + " is not a valid email address...");
            document.getElementById("email_address").style.border = "thin solid red";
            return false;
        } else {

            var payload = {};
            for (var i = 0; i < elements.length; i++) {
                payload[elements[i].name] = elements[i].value;
            }
            delete payload[""];

            sendHTTPRequest("POST", url, payload, function (results) {
                if (results["registration_status"] == true) {
                    alert("Successful registration. Now log in with your email address and password");
                    window.location = "/login";
                } else {
                    alert(results["registration_message"]);
                }
            });
        }
    }

}

/**
 * @returns {boolean} true if the element's value is blank, false otherwise.
 * @param {string} elementValue The element to be checked
 */
function isBlank(elementValue) {
    return elementValue.trim() === "";
}

/**
 * @description Check whether all required fields have been completed.
 * 
 * @param {HTMLFormElement} elements The contents of the form element
 * @param {string} formID The document ID of the form
 */
function checkRequired(elements, formID) {
    var requiredElements = requiredFields[formID];
    var missingElements = new Set();
    requiredElements.forEach(function (name) {
        if (isBlank(elements[name].value)) {
            missingElements.add(name);
        }
    });
    return missingElements;
}

/**
 * 
 * @param {string} method The method to be used, e.g. "POST"
 * @param {string} url The url to which the payload will be sent
 * @param {JSON} payload The payload that will be sent.
 * @param {function} callBack The callback function once the request is successful
 */
function sendHTTPRequest(method, url, payload, callBack) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            callBack(JSON.parse(this.responseText));
        }
    }
    xhttp.open(method, url, true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(payload));
}