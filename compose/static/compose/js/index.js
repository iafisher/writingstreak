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
    cumulativeWordCount = parseInt(
        document.getElementById("cumulativeWordCount").textContent);

    setTextareaHeight();
    countWords();

    // Upload the text every 300 milliseconds. A POST request is only actually
    // sent when the text has been changed from the saved version.
    setInterval(uploadText, 300);

    textarea.oninput = () => {
        setTextareaHeight();
        countWords();
    };

    const editButton = document.getElementById("editButton");
    const saveButton = document.getElementById("saveButton");
    const cancelButton = document.getElementById("cancelButton");
    const goalWordCount = document.getElementById("goalWordCount");
    const goalWordCountInput = document.getElementById("goalWordCountInput");

    editButton.onclick = () => {
        editButton.style.display = "none";
        saveButton.style.display = "inline-block";
        cancelButton.style.display = "inline-block";

        goalWordCountInput.value = goalWordCount.innerHTML;

        goalWordCount.style.display = "none";
        goalWordCountInput.style.display = "inline-block";
    };

    saveButton.onclick = () => {
        editButton.style.display = "inline-block";
        saveButton.style.display = "none";
        cancelButton.style.display = "none";

        let newWordCount = goalWordCountInput.value;
        updateWordCount(newWordCount);
        goalWordCount.innerHTML = newWordCount;

        goalWordCount.style.display = "inline-block";
        goalWordCountInput.style.display = "none";
    };

    cancelButton.onclick = () => {
        editButton.style.display = "inline-block";
        saveButton.style.display = "none";
        cancelButton.style.display = "none";

        goalWordCount.style.display = "inline-block";
        goalWordCountInput.style.display = "none";
    };

    // Confirm before closing page if there are unsaved changes.
    window.onbeforeunload = function (e) {
        if (lastSaved !== textarea.value) {
            // I don't think the contents of this message actually matters:
            // Firefox doesn't seem to display it.
            return 'You have unsaved changes.';
        }
    }
}

function setTextareaHeight() {
    let textarea = document.getElementById("textInput");
    // Courtesy of https://stackoverflow.com/questions/454202/
    textarea.style.height = "auto";
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
        let errorMsg = document.getElementById("errorMsg");

        fetch("/upload", {
            method: "post",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({text: text}),
            credentials: 'include',
        }).then(response => {
            const errno = response.status;
            if (errno >= 200 && errno < 300) {
                lastSaved = text;
                errorMsg.innerHTML = "";
            } else {
                console.error('Fetch error: status code', errno);
                errorMsg.innerHTML = "Error: could not save changes. " +
                    "The server returned error code " + errno + ".";
            }
        })
        .catch(error => {
            console.error('Fetch error: ', error);
            errorMsg.innerHTML = "Error: could not save changes. " +
                "Is the server running?";
        });
    }
}


function updateWordCount(newCount) {
    fetch("/update_wc", {
        method: "post",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({wordCount: newCount}),
        credentials: 'include',
    }).then(response => {
        const errno = response.status;
        if (errno >= 200 && errno < 300) {
            errorMsg.innerHTML = "";
        } else {
            console.error('Fetch error: status code', errno);
            errorMsg.innerHTML = "Error: could not save changes. " +
                "The server returned error code " + errno + ".";
        }
    })
    .catch(error => {
        console.error('Fetch error: ', error);
        errorMsg.innerHTML = "Error: could not save changes. " +
            "Is the server running?";
    });
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
