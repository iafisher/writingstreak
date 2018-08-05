/**
 * A small React module to control the various operations on the composer page,
 * including
 *
 *   - Saving text to the back-end.
 *   - Displaying the word count.
 *   - Editing the word count goal.
 *   - Resizing the textarea.
 */

import React from 'react';
import ReactDOM from 'react-dom';


let csrftoken = Cookies.get("csrftoken");


function WordCount(props) {
    return (
        <p>
          {quantify(props.count, "word")} ({props.count + props.total} to date)
        </p>
    );
}


function WordCountGoal(props) {
    const wordsLeft = Math.max(props.goal - props.count, 0);
    if (props.editing) {
        return (
            <p>
              You need {quantify(wordsLeft, "more word")} to meet your
              daily goal of
              <input type="number" id="goal-input" step="10" min="10"
                value={props.value}
                onChange={props.handleChange} 
              />
              words.

              <button onClick={props.handleSave} id="save-button">
                Save
              </button>
              <button onClick={props.handleCancel} id="cancel-button">
                Cancel
              </button>
            </p>
        );
    } else {
        return (
            <p>
              You need {quantify(wordsLeft, "more word")} to meet your
              daily goal of {props.goal} words.

              <button onClick={props.handleEdit} id="edit-button">
                Edit
              </button>
            </p>
        );
    }
}


function StreakLength(props) {
    let realLength = props.length;
    if (props.count >= props.goal) {
        realLength = realLength + 1;
    }
    return (
        <p>You are on a {realLength} day streak.</p>
    );
}


function TextInput(props) {
    return (
        <textarea
          id="text-input"
          value={props.text}
          onInput={props.onInput}
        >
        </textarea>
    );
}


function ErrorMessage(props) {
    if (props.message !== "") {
        return <p id="error-message">{props.message}</p>;
    } else {
        return null;
    }
}


class Window extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            editing: false,
            editValue: 0,
            errorMessage: "",
            lastSaved: "",
            streakLength: 0,
            text: "",
            totalWordCount: 0,
            wordCount: 0,
            wordCountGoal: 100,
        };
        fetchEntry(entry => this.onFetch(entry));

        this.handleChange = this.handleChange.bind(this);
        this.saveTextIfUnsaved = this.saveTextIfUnsaved.bind(this);

        setInterval(this.saveTextIfUnsaved, 300);
        window.onbeforeunload = () => this.beforeUnload();
    }

    onFetch(entry) {
        this.setState({
            editValue: entry['word_count_goal'],
            lastSaved: entry['text'],
            streakLength: entry['streak_length'],
            text: entry['text'],
            totalWordCount: entry['total_word_count'],
            wordCountGoal: entry['word_count_goal'],
            wordCount: entry['word_count'],
        });
        setTextareaHeight();
    }

    render() {
        return (
            <div>
              <TextInput
                text={this.state.text}
                onInput={() => this.handleInput()}
              />
              <ErrorMessage message={this.state.errorMessage} />
              <WordCount
                count={this.state.wordCount}
                total={this.state.totalWordCount}
              />
              <WordCountGoal
                count={this.state.wordCount}
                goal={this.state.wordCountGoal}
                editing={this.state.editing}
                value={this.state.editValue}

                handleEdit={() => this.handleEdit()}
                handleSave={() => this.handleSave()}
                handleCancel={() => this.handleCancel()}
                handleChange={this.handleChange}
              />
              <StreakLength
                length={this.state.streakLength}
                count={this.state.wordCount}
                goal={this.state.wordCountGoal}
              />
            </div>
        );
    }

    handleEdit() {
        this.setState({editing: true});
    }

    handleSave() {
        saveEntry({word_count_goal: this.state.editValue}, () => {
            /* Success */
            this.setState({
                editing: false,
                errorMessage: "",
                wordCountGoal: this.state.editValue,
            });
        }, () => {
            /* Error */
            this.setState({
                editing: false,
                errorMessage: "Error: could not save changes. " +
                    "Is the server running?",
            });
        });
    }

    handleCancel() {
        this.setState({
            editing: false,
            editValue: this.state.wordCountGoal,
        });
    }

    handleChange(event) {
        this.setState({editValue: event.target.value});
    }

    handleInput() {
        setTextareaHeight();

        const text = document.getElementById("text-input").value;
        this.setState({
            text: text,
            wordCount: countWords(text)
        });
    }

    saveTextIfUnsaved() {
        if (this.state.lastSaved !== this.state.text) {
            saveEntry({text: this.state.text}, () => {
                /* Success */
                this.setState({
                    errorMessage: "",
                    lastSaved: this.state.text,
                });
            }, () => {
                /* Error */
                this.setState({
                    errorMessage: "Error: could not save changes. " +
                        "Is the server running?",
                });
            });
        }
    }

    beforeUnload() {
        if (this.state.lastSaved !== this.state.text) {
            // I don't think the contents of this message actually matters:
            // Firefox doesn't seem to display it.
            return 'You have unsaved changes.';
        }
    }
}


function countWords(text) {
    return text.replace(/\s+/g, " ").split(" ").filter(
        word => word.length > 0).length;
}


function quantify(n, s) {
    return n + " " + s + (n === 1 ? "" : "s");
}


function fetchEntry(onSuccess) {
    fetch("/api/fetch", {
        method: "get",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json"
        },
        credentials: 'include',
    }).then(response => {
        const errno = response.status;
        if (errno >= 200 && errno < 300) {
            if (onSuccess) {
                response.json().then(entry => onSuccess(entry));
            }
        }
    })
    .catch(error => {
        console.error('Fetch error: ', error);
    });
}


/**
 * Save the plain object `entry` to the back-end database. If the function
 * `onSuccess` is provided, it is invoked with no arguments if the request
 * succeeds. Similarly, `onError` is invoked with no arguments on failure.
 *
 * `entry` may have a `text` field and/or a `word_count_goal` field.
 */
function saveEntry(entry, onSuccess, onError) {
    fetch("/api/update", {
        method: "post",
        headers: {
            "X-CSRFToken": csrftoken,
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
        } else {
            if (onError) {
                onError();
            }
        }
    })
    .catch(error => {
        if (onError) {
            onError();
        }
    });
}


/**
 * Resize the textarea once it's filled to the bottom.
 */
function setTextareaHeight() {
    const textarea = document.getElementById("text-input");
    // Courtesy of https://stackoverflow.com/questions/454202/
    textarea.style.height = "auto";
    textarea.style.height = Math.min(window.innerHeight * 0.8,
            textarea.scrollHeight) + "px";
}


ReactDOM.render(
    <Window />,
    document.getElementById("react-root")
)
