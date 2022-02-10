//Get current year
const getCurrentTimeDate = () => {
    //create variable with current date
    let currentTimeDate = new Date();

    //create variable with year
    var year = currentTimeDate.getFullYear();

    //get HTML tag with id and assign year to it
    document.getElementById("year").innerHTML = year;

    //run the function
    setTimeout(getCurrentTimeDate, 500);

}
getCurrentTimeDate();