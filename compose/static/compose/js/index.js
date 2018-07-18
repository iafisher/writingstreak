'use strict';

let csrftoken = Cookies.get("csrftoken");

// Call the onload function when the document is ready.
if (document.readyState === "complete" || (document.readyState !== "loading" &&
        !document.documentElement.doScroll)) {
    onload();
} else {
    document.addEventListener("DOMContentLoaded", onload);
}

function onload() {
    countWords();
    setInterval(uploadText, 1000);
    document.querySelector("textarea").addEventListener("keyup", countWords);
}

let lastSaved = "";
function uploadText() {
    let text = document.querySelector("textarea").value;
    if (lastSaved != text) {
        fetch("/upload", {
            method: "post",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({text: text})
        }).then(() => lastSaved = text);
    }
}

function countWords() {
    let text = document.querySelector("textarea").value;
    text = text.replace(/\s+/g, " ");
    let count = text.split(" ").filter(word => word.length > 0).length;
    if (count == 1) {
        document.querySelector("#wordCount").innerHTML = count + " word";
    } else {
        document.querySelector("#wordCount").innerHTML = count + " words";
    }
}
