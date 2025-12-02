const buttons = document.querySelectorAll(".planet-btn");
const panels = document.querySelectorAll(".planet-panel");

buttons.forEach(btn => {
    btn.addEventListener("click", () => {

        buttons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        let target = btn.dataset.planet;
        panels.forEach(p => {
            p.classList.remove("active");

            let audio = p.querySelector(".planet-audio");
            if (audio) {
                audio.pause();
                audio.currentTime = 0;
            }
        });

        const activePanel = document.getElementById(target);
        activePanel.classList.add("active");

        let audio = activePanel.querySelector(".planet-audio");
        if (audio) {
            audio.play();
        }

        let ayah = activePanel.querySelector(".planet-ayah");
        let text = ayah.dataset.text;

        ayah.innerHTML = "";
        let i = 0;
        let interval = setInterval(() => {
            ayah.innerHTML += text[i];
            i++;
            if (i >= text.length) clearInterval(interval);
        }, 60);
    });
});
