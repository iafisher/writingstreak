/**
 * A small JavaScript module to control the various operations on the composer
 * page, including
 *
 *   - Saving text to the back-end.
 *   - Displaying the word count.
 *   - Resizing the textarea.
 */

'use strict';

// Store the last saved version of the text, to avoid unnecessary re-uploads of
// the same text.
let gLastSaved = "";
// The number of words written to date, as an integer.
let gCumulativeWordCount;
// The goal word count for the day, as an integer.
let gGoalWordCount;
// The length of the active streak, not including today.
let gStreakLength;
let gCsrftoken = Cookies.get("csrftoken");

// Elements that the JS manipulates.
let eTextInput;
let eCumulativeWordCount;
let eEditButton;
let eSaveButton;
let eCancelButton;
let eGoal;
let eGoalInput;
let eErrorMessage;
let eWordCount;
let eWordsToGoal;
let eStreakLength;

// Call the onload function when the document is ready.
if (document.readyState === "complete" || (document.readyState !== "loading" &&
        !document.documentElement.doScroll)) {
    onload();
} else {
    document.addEventListener("DOMContentLoaded", onload);
}

function onload() {
    // Set the global element constants.
    eTextInput = document.getElementById("text-input");
    eCumulativeWordCount = document.getElementById("cumulative-word-count");
    eEditButton = document.getElementById("edit-button");
    eSaveButton = document.getElementById("save-button");
    eCancelButton = document.getElementById("cancel-button");
    eGoal = document.getElementById("goal");
    eGoalInput = document.getElementById("goal-input");
    eErrorMessage = document.getElementById("error-message");
    eWordCount = document.getElementById("word-count");
    eWordsToGoal = document.getElementById("words-to-goal");
    eStreakLength = document.getElementById("streak-length");

    // Set global variables.
    gLastSaved = eTextInput.value;
    gCumulativeWordCount = parseInt(eCumulativeWordCount.textContent);
    gGoalWordCount = parseInt(eGoal.textContent);
    gStreakLength = parseInt(eStreakLength.textContent);

    setTextareaHeight();
    countWords();

    // Save the text every 300 milliseconds.
    setInterval(saveTextIfUnsaved, 300);

    eTextInput.oninput = () => {
        setTextareaHeight();
        countWords();
    };

    eEditButton.onclick = () => {
        eEditButton.style.display = "none";
        eSaveButton.style.display = "inline-block";
        eCancelButton.style.display = "inline-block";

        eGoalInput.value = goal.textContent;

        eGoal.style.display = "none";
        eGoalInput.style.display = "inline-block";
    };

    eSaveButton.onclick = () => {
        eEditButton.style.display = "inline-block";
        eSaveButton.style.display = "none";
        eCancelButton.style.display = "none";

        let newWordCount = eGoalInput.value;
        if (newWordCount !== "" && newWordCount >= 10) {
            gGoalWordCount = newWordCount;
            countWords();
            saveEntry({word_count_goal: newWordCount})
            eGoal.textContent = newWordCount;
        }
        eGoal.style.display = "inline-block";
        eGoalInput.style.display = "none";
    };

    eCancelButton.onclick = () => {
        eEditButton.style.display = "inline-block";
        eSaveButton.style.display = "none";
        eCancelButton.style.display = "none";

        eGoal.style.display = "inline-block";
        eGoalInput.style.display = "none";
    };

    // Confirm before closing page if there are unsaved changes.
    window.onbeforeunload = function (e) {
        if (gLastSaved !== eTextInput.value) {
            // I don't think the contents of this message actually matters:
            // Firefox doesn't seem to display it.
            return 'You have unsaved changes.';
        }
    }
}


/**
 * Resize the textarea once it's filled to the bottom.
 */
function setTextareaHeight() {
    // Courtesy of https://stackoverflow.com/questions/454202/
    eTextInput.style.height = "auto";
    eTextInput.style.height = Math.min(window.innerHeight * 0.8,
            eTextInput.scrollHeight) + "px";
}


/**
 * Upload the contents of the textarea to the back-end server, if there have
 * been changes since the last save.
 */
function saveTextIfUnsaved() {
    let text = eTextInput.value;
    if (gLastSaved != text) {
        saveEntry({text: text}, () => {
            gLastSaved = text;
        });
    }
}


/**
 * Save the plain object `entry` to the back-end database. If the function
 * `onSuccess` is provided, it is invoked with no arguments if the request
 * succeeds.
 *
 * `entry` may have a `text` field and/or a `word_count_goal` field.
 */
function saveEntry(entry, onSuccess) {
    fetch("/api/update", {
        method: "post",
        headers: {
            "X-CSRFToken": gCsrftoken,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(entry),
        credentials: 'include',
    }).then(response => {
        const errno = response.status;
        if (errno >= 200 && errno < 300) {
            if (onSuccess) {
                onSuccess();
            }
            eErrorMessage.textContent = "";
        } else {
            console.error('Fetch error: status code', errno);
            eErrorMessage.textContent = "Error: could not save changes. " +
                "The server returned error code " + errno + ".";
        }
    })
    .catch(error => {
        console.error('Fetch error: ', error);
        eErrorMessage.textContent = "Error: could not save changes. " +
            "Is the server running?";
    });
}


/**
 * Count the number of words in the textarea and update the word count display.
 */
function countWords() {
    let text = eTextInput.value;
    text = text.replace(/\s+/g, " ");
    let count = text.split(" ").filter(word => word.length > 0).length;

    redrawWordCounter(count);
    redrawWordsToGoal(count);
    redrawCumulativeWordCounter(count);
    redrawStreakLength(count);
}


/**
 * Redraw the words-to-goal element with the new word count.
 */
function redrawWordsToGoal(newCount) {
    let wordsToGoal = Math.max(gGoalWordCount - newCount, 0);
    eWordsToGoal.textContent = wordsToGoal + pluralize(" more word", wordsToGoal);
}


/**
 * Redraw the word-counter element with the new word count.
 */
function redrawWordCounter(newCount) {
    eWordCount.textContent = newCount + pluralize(" word", newCount);
}


/**
 * Redraw the cumulative-word-counter element with the new word count.
 */
function redrawCumulativeWordCounter(newCount) {
    eCumulativeWordCount.textContent = gCumulativeWordCount + newCount;
}


/**
 * Redraw the streak-length element with the new word count.
 */
function redrawStreakLength(newCount) {
    if (newCount >= gGoalWordCount) {
        eStreakLength.textContent = gStreakLength + 1;
    } else {
        eStreakLength.textContent = gStreakLength;
    }
}


/**
 * Pluralize the string, or not, depending on the count.
 */
function pluralize(word, count) {
    return word + ((count === 1) ? "" : "s");
}
