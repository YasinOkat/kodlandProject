let currentQuestion = 1;
let totalTime = 10; // Total time for each question in seconds
let timerInterval;

function nextQuestion(next) {
    document.getElementById(`question${currentQuestion}`).style.display = 'none';
    currentQuestion = next;
    document.getElementById(`question${currentQuestion}`).style.display = 'block';

    clearInterval(timerInterval); // Clear the previous timer
    startTimer();
}

function startTimer() {
    let remainingTime = totalTime;
    const timerElement = document.getElementById(`timer${currentQuestion}`);
    timerElement.textContent = remainingTime;

    timerInterval = setInterval(() => {
        remainingTime--;
        timerElement.textContent = remainingTime;

        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            nextQuestion(currentQuestion + 1);
        }
    }, 1000);
}

// Start the timer for the first question
startTimer();
