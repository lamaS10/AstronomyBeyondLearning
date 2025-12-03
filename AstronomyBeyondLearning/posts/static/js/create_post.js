document.addEventListener("DOMContentLoaded", () => {

    const svg = document.querySelector(".border-anim");
    if (svg) {
        const rects = svg.querySelectorAll("rect");
        const width = svg.clientWidth;
        const height = svg.clientHeight;
        const perimeter = 2 * (width + height);

        rects.forEach(rect => {
            rect.setAttribute("width", width);
            rect.setAttribute("height", height);
            rect.style.setProperty("--perimeter", perimeter);
            rect.style.strokeDasharray = perimeter;
            rect.style.strokeDashoffset = perimeter;
        });
    }

    const dropZone = document.getElementById("mediaDropZone");
    const fileInput = document.getElementById("mediaFile");
    const preview = document.getElementById("mediaPreview");

    if (!dropZone) return;

    dropZone.addEventListener("click", () => fileInput.click());

    ["dragenter", "dragover"].forEach(eventName => {
        dropZone.addEventListener(eventName, e => {
            e.preventDefault();
            dropZone.classList.add("highlight");
        });
    });

    ["dragleave", "drop"].forEach(eventName => {
        dropZone.addEventListener(eventName, e => {
            e.preventDefault();
            dropZone.classList.remove("highlight");
        });
    });

    dropZone.addEventListener("drop", e => {
        let files = e.dataTransfer.files;
        handleFiles(files);
    });

    fileInput.addEventListener("change", e => {
        handleFiles(e.target.files);
    });

    function handleFiles(files) {
        preview.innerHTML = "";
        [...files].forEach(file => {
            const url = URL.createObjectURL(file);
            const elem = document.createElement(file.type.startsWith("image") ? "img" : "video");
            if (file.type.startsWith("video")) elem.controls = true;
            elem.src = url;
            preview.appendChild(elem);
        });
    }
});
