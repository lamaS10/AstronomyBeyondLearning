document.addEventListener("DOMContentLoaded", function () {
    let timerSpan = document.getElementById("timer");

    if (!timerSpan) return;

    let countdownSound = new Audio("/static/sounds/countdown.wav");
    countdownSound.preload = "auto"; 

    let timeLeft = 30;

    let countdown = setInterval(() => {
        timeLeft--;
        timerSpan.textContent = timeLeft;

        if (timeLeft <= 3 && timeLeft > 0) {
            countdownSound.currentTime = 0; 
            countdownSound.play();
        }

        if (timeLeft <= 0) {
            clearInterval(countdown);

            let autoForm = document.getElementById("autoNextForm");
            if (autoForm) autoForm.submit();
        }

    }, 1000);
});
