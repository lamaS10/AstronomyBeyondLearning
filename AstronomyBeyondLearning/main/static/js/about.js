document.addEventListener("DOMContentLoaded", function () {
    let title = "About Us";
    let desc = "ABL Galaxy is a modern and immersive platform designed to let you explore the Solar System like never before — with planets, interactive posts, educational content, and a gamified learning experience. Our goal is to transform space learning into a dynamic journey where users can explore, play, and grow their knowledge through engaging activities.";

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
