'use strict';

/* CSRF set-up courtesy of https://docs.djangoproject.com/en/2.0/ref/csrf/ */

var csrftoken = Cookies.get("csrftoken");

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).ready(function () {
    setInterval(uploadText, 5000);
});

function uploadText() {
    var text = $("textarea").val();
    console.log(text);
    $.post("/compose/upload", {"text": text});
}
