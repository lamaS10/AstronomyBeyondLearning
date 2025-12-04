function calculateWeight() {
    const gravity = parseFloat(document.getElementById("planetGravity").value);
    const earthGravity = 9.8;

    const w = parseFloat(document.getElementById("earthWeight").value);

    if (isNaN(w) || w <= 0) {
        document.getElementById("weightResult").innerText = "Please enter a valid weight.";
        return;
    }

    const result = w * (gravity / earthGravity);

    document.getElementById("weightResult").innerText =
        "Your weight on this planet: " + result.toFixed(2) + " kg";
}
