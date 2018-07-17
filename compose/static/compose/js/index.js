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
    countWords();
    setInterval(uploadText, 5000);

    $("textarea").keyup(countWords);
});

function uploadText() {
    var text = $("textarea").val();
    $.post("/compose/upload", {"text": text});
}

function countWords() {
    var text = $("textarea").val();
    text = text.replace(/\s+/g, " ");
    console.log(text);
    var count = text.split(" ").filter(word => word.length > 0).length;
    if (count == 1) {
        $("#wordCount").html(count + " word");
    } else {
        $("#wordCount").html(count + " words");
    }
}
