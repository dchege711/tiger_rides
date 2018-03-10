function registerNewMember(formName) {
    var elements = document.getElementById(formName).elements;

    // Ensure that all fields have been filled
    console.log(typeof (elements));
    for (var key in elements) {
        console.log(elements[key]);
    }
}
