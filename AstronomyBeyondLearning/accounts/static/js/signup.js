document.addEventListener("DOMContentLoaded", function () {

    const passwordInput = document.getElementById("id_password");
    const confirmInput = document.getElementById("id_confirm_password");
    const matchText = document.getElementById("password-match");

    function checkPasswordMatch() {
        const pass = passwordInput.value;
        const confirm = confirmInput.value;

        if (confirm.length === 0) {
            matchText.textContent = "";
            matchText.className = "match-text";
            return;
        }

        if (pass === confirm) {
            matchText.textContent = "✔ Passwords match";
            matchText.className = "match-text valid";
        } else {
            matchText.textContent = "✘ Passwords do not match";
            matchText.className = "match-text invalid";
        }
    }

    if (passwordInput) {
        passwordInput.addEventListener("input", function () {
            const value = passwordInput.value;

            document.getElementById("rule-length").className =
                value.length >= 8 ? "valid" : "invalid";

            document.getElementById("rule-upper").className =
                /[A-Z]/.test(value) ? "valid" : "invalid";

            document.getElementById("rule-lower").className =
                /[a-z]/.test(value) ? "valid" : "invalid";

            document.getElementById("rule-number").className =
                /[0-9]/.test(value) ? "valid" : "invalid";

            document.getElementById("rule-special").className =
                /[@$!%*?&#^+\-]/.test(value) ? "valid" : "invalid";

            checkPasswordMatch();
        });
    }

    if (confirmInput) {
        confirmInput.addEventListener("input", checkPasswordMatch);
    }


    const card = document.querySelector(".auth-card");
    const svg = document.querySelector(".border-anim");
    const blue = document.querySelector(".path-blue");
    const purple = document.querySelector(".path-purple");

    if (card && svg && blue && purple) {

        const w = card.offsetWidth;
        const h = card.offsetHeight;
        const r = 14;

        svg.setAttribute("width", w);
        svg.setAttribute("height", h);

        [blue, purple].forEach(rect => {
            rect.setAttribute("x", 0);
            rect.setAttribute("y", 0);
            rect.setAttribute("width", w);
            rect.setAttribute("height", h);
            rect.setAttribute("rx", r);
            rect.setAttribute("ry", r);

            const perimeter = 2 * (w + h);
            rect.style.strokeDasharray = perimeter;
            rect.style.setProperty("--perimeter", perimeter);
        });
    }

});
