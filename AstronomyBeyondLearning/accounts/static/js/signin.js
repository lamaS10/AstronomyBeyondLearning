document.addEventListener("DOMContentLoaded", function () {

    // ---------- BORDER ANIMATION SETUP ----------
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
