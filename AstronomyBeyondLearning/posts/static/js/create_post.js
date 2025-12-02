document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('mediaDropZone');
    const fileInput = document.getElementById('mediaFile');
    const previewContainer = document.getElementById('mediaPreview');
    const browseLink = document.querySelector('.browse-link');

    browseLink.addEventListener('click', () => {
        fileInput.click();
    });

    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropZone.classList.add('highlight'); 
    }

    function unhighlight() {
        dropZone.classList.remove('highlight');
    }

    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        let dt = e.dataTransfer;
        let files = dt.files;
        
        handleFiles(files);
    }

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });


    function handleFiles(files) {

        previewContainer.innerHTML = ''; 

        [...files].forEach(file => {
            const fileURL = URL.createObjectURL(file);
            const mediaElement = document.createElement(file.type.startsWith('image/') ? 'img' : 'video');
            
            if (file.type.startsWith('video/')) {
                mediaElement.controls = true; 
            }
            
            mediaElement.src = fileURL;
            mediaElement.style.maxWidth = '100px';
            mediaElement.style.maxHeight = '100px';
            mediaElement.style.margin = '5px'; 
            mediaElement.style.borderRadius = '4px'; 
            mediaElement.style.objectFit = 'cover';
            
            previewContainer.appendChild(mediaElement);
        });
    }

   

});