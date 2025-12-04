let index = 0;
let cards = document.querySelectorAll(".planet-card");

function showPlanet(i) {
    cards.forEach(c => c.classList.remove("active"));
    cards[i].classList.add("active");
}

function nextPlanet() {
    index = (index + 1) % cards.length;
    showPlanet(index);
}

function prevPlanet() {
    index = (index - 1 + cards.length) % cards.length;
    showPlanet(index);
}

document.addEventListener("DOMContentLoaded", () => showPlanet(0));
