let allTextContents = document.querySelectorAll('p');
let width = document.querySelector('nav').offsetWidth;

// user type
let user_type = document.getElementById('acc_type').textContent;
if (user_type=="Teacher"){
    document.getElementById('teacher').style.visibility = "visible";
    document.getElementById("student").remove();
}
else{
    document.getElementById('teacher').remove();
    document.getElementById('student').style.visibility = "visible";
}