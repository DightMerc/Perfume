//Django basic setup for accepting ajax requests.
// Cookie obtainer Django

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
// Setup ajax connections safetly

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function addToCart(product_num){
    var option = document.getElementById("color").innerText;
    console.log(option)

    $.ajax({
        url : "/addToCart/", // the endpoint
        type : "POST", // http method
        data : { product: product_num, option: option}, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json);
            location.replace("/")
        },
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    }
    );
}

function kick(product_num){

    $.ajax({
        url : "/kickProduct/", // the endpoint
        type : "POST", // http method
        data : { product: product_num}, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json);
            location.reload();

        },
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    }
    );
}

function checkout(){
    var firstName = document.getElementById("first_name").value;
    var lastName = document.getElementById("last_name").value;
    var address = document.getElementById("street_address").value;
    var phone = document.getElementById("phone_number").value;
    var comment = document.getElementById("comment").value;


    $.ajax({
        url : "/checkout/", // the endpoint
        type : "POST", // http method
        data : { firstName: firstName, lastName: lastName, address: address, phone: phone, comment: comment }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json);
            location.replace("/");

        },
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    }
    );
}

function changeColor(title){

    var id = title.split(" ")[0];
    var title = title.split(" ")[1];

    var element = document.getElementById("color");
    element.innerText = title;
    var holder = document.getElementById("optionButtons");
    $("#optionButtons").children().css( "border", "0" );
    var button= document.getElementById(id).style.border ="2px solid black";

    var photo = document.getElementById(title);
    $(photo).parent().parent().children().removeClass("active");
    // $(photo).parent().parent().children().toggleClass("active")
    $(photo).parent().toggleClass("active");


    // console.log()]


}