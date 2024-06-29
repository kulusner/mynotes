document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("question-form");
    const answerDiv = document.getElementById("answer");
    const loadingSpinner = document.getElementById("loading-spinner");
    const copyButton = document.getElementById("copy-button");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const question = document.getElementById("question").value;

        if (!question.trim()) {
            alert("Please enter a question.");
            return;
        }

        // Show the loading spinner
        loadingSpinner.style.display = "block";
        answerDiv.style.display = "none";
        copyButton.style.display = "none";

        fetch("/get_answer", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: question })
        })
        .then(response => response.json())
        .then(data => {
            // Hide the loading spinner
            loadingSpinner.style.display = "none";

            answerDiv.style.display = "block";
            answerDiv.style.opacity = 0;
            if (data.answer) {
                answerDiv.classList.remove("alert-danger");
                answerDiv.classList.add("alert-secondary");
                answerDiv.textContent = data.answer;

                // Show the copy button
                copyButton.style.display = "block";
                setTimeout(() => { answerDiv.style.opacity = 1; }, 50);
            } else {
                answerDiv.classList.remove("alert-secondary");
                answerDiv.classList.add("alert-danger");
                answerDiv.textContent = "Error: Could not generate an answer.";
                setTimeout(() => { answerDiv.style.opacity = 1; }, 50);
            }
        })
        .catch(error => {
            // Hide the loading spinner
            loadingSpinner.style.display = "none";

            answerDiv.style.display = "block";
            answerDiv.style.opacity = 0;
            answerDiv.classList.remove("alert-secondary");
            answerDiv.classList.add("alert-danger");
            answerDiv.textContent = "Error: Could not generate an answer.";
            setTimeout(() => { answerDiv.style.opacity = 1; }, 50);
            console.error("Error:", error);
        });
    });

    copyButton.addEventListener("click", function () {
        const answerText = answerDiv.textContent;
        navigator.clipboard.writeText(answerText).then(() => {
            copyButton.textContent = "Copied!";
            setTimeout(() => { copyButton.textContent = "Copy"; }, 2000);
        }).catch(err => {
            console.error("Could not copy text: ", err);
        });
    });
});
