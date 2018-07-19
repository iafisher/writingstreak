/**
 * A small JavaScript module to control the various operations on the composer
 * page, including
 *
 *   - Saving text to the back-end.
 *   - Displaying the word count.
 *   - Resizing the textarea.
 */

'use strict';

let cumulativeWordCount;

// Call the onload function when the document is ready.
if (document.readyState === "complete" || (document.readyState !== "loading" &&
        !document.documentElement.doScroll)) {
    onload();
} else {
    document.addEventListener("DOMContentLoaded", onload);
}

function onload() {
    let textarea = document.getElementById("textInput");
    lastSaved = textarea.value;
    cumulativeWordCount = parseInt(document.getElementById("cumulativeWordCount").textContent);

    setTextareaHeight();
    countWords();

    // Upload the text once every second.
    setInterval(uploadText, 1000);

    textarea.oninput = function () {
        setTextareaHeight();
        countWords();
    };
}

function setTextareaHeight() {
    let textarea = document.getElementById("textInput");
    // Courtesy of https://stackoverflow.com/questions/7745741/
    textarea.style.height = "";
    textarea.style.height = Math.min(window.innerHeight * 0.8,
            textarea.scrollHeight) + "px";
}

// Store the last saved version of the text, to avoid unnecessary re-uploads of
// the same text.
let lastSaved = "";
let csrftoken = Cookies.get("csrftoken");

/**
 * Upload the contents of the textarea to the back-end server.
 */
function uploadText() {
    let text = document.getElementById("textInput").value;
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

/**
 * Count the number of words in the textarea and update the word count display.
 */
function countWords() {
    let text = document.getElementById("textInput").value;
    text = text.replace(/\s+/g, " ");
    let count = text.split(" ").filter(word => word.length > 0).length;

    let wordCountElem = document.getElementById("wordCount");
    if (count == 1) {
        wordCountElem.innerHTML = count + " word";
    } else {
        wordCountElem.innerHTML = count + " words";
    }

    document.getElementById("cumulativeWordCount").innerHTML =
        cumulativeWordCount + count;
}
