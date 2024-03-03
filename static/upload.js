function uploadFile(input) {
    var file = input.files[0];

    if (!file || file.type !== 'application/pdf') {
        alert('Il file non è un PDF');
        input.value = '';
        return;
    }

    var progressBarContainer = document.getElementById('progressBarContainer');
    var progressBar = document.getElementById('progressBar');
    var progressText = document.getElementById('progressText');

    progressBarContainer.style.display = 'block';
    progressText.innerText = 'Caricamento...';

    var formData = new FormData();
    formData.append('file', file);

    var request = new XMLHttpRequest();
    request.open('POST', '/upload');

    request.upload.onprogress = function(event) {
        if (event.lengthComputable) {
            var percentComplete = (event.loaded / event.total) * 100;
            progressBar.value = percentComplete;
            progressText.innerText = 'Caricamento... ' + Math.floor(percentComplete) + '%';
        }
    };

    request.onload = function() {
        if (request.status === 200) {
            console.log('File uploaded');
            progressBar.value = 100;
            progressText.innerText = 'Caricamento completato';
            setTimeout(function() {
                progressBarContainer.style.display = 'none';
            }, 1000);
        } else {
            console.error('Upload error');
        }
    };

    request.send(formData);
}
