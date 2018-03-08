console.log("Load #1");

function registerNewMember(formID) {
    var elements = document.getElementById(formID).elements;
    var missingElements = new Set();
    var requiredElements = ["first_name", "last_name", "email_address", "password"]
    
    requiredElements.forEach(function(name) {
        if (elements[name].value.strip() === "") {
            missingElements.add(name);
        }
    });

    console.log(missingElements);

    missingElements.forEach(function(elementName) {
        
    });
}
