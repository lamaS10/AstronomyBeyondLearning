document.addEventListener("DOMContentLoaded", function () {
    let title = "About Us";
    let desc = "ABL Galaxy is a modern and immersive experience designed to let you explore the Solar System like never before — with planets, verses, interactive posts, quizzes, and intelligent suggestions.";

    let titleEl = document.getElementById("typing-title");
    let descEl = document.getElementById("typing-desc");

    let i = 0;

    function typeTitle() {
        if (i < title.length) {
            titleEl.textContent += title.charAt(i);
            i++;
            setTimeout(typeTitle, 60);
        } else {
            setTimeout(typeDesc, 300);
        }
    }

    let j = 0;
    function typeDesc() {
        if (j < desc.length) {
            descEl.textContent += desc.charAt(j);
            j++;
            setTimeout(typeDesc, 20);
        }
    }

    typeTitle();
});
