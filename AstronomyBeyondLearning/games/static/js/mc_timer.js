document.addEventListener("DOMContentLoaded", function () {
    let timerSpan = document.getElementById("timer");

    if (!timerSpan) return; // لو الصفحة ما فيها تايمر خلاص

    let countdownSound = new Audio("/static/sounds/countdown.wav");
    countdownSound.preload = "auto"; // تحميل مسبق

    let timeLeft = 10;

    let countdown = setInterval(() => {
        timeLeft--;
        timerSpan.textContent = timeLeft;

        // 🔥 يشغّل الصوت إذا بقي 3 – 2 – 1 ثانية
        if (timeLeft <= 3 && timeLeft > 0) {
            countdownSound.currentTime = 0; // يعيد الصوت للبداية
            countdownSound.play();
        }

        // إذا انتهى الوقت — Submit تلقائي
        if (timeLeft <= 0) {
            clearInterval(countdown);

            let autoForm = document.getElementById("autoNextForm");
            if (autoForm) autoForm.submit();
        }

    }, 1000);
});
