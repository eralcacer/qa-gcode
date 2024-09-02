const dropArea = document.getElementById('dropArea');
const fileInput = document.getElementById('fileInput');
const selectedFile = document.getElementById('selectedFile');
const submitButton = document.getElementById('submitButton');
const chooseFile = document.getElementById('chooseFile')

dropArea.addEventListener('dragover', function (e) {
    e.preventDefault();
});

dropArea.addEventListener('drop', function (e) {
    e.preventDefault();
    const file = e.dataTransfer.files[0];

    if (file) {
        selectedFile.textContent = file.name;
        submitButton.style.display = 'block';
        fileInput.files = e.dataTransfer.files;
    } else {
        selectedFile.textContent = 'No file selected';
        submitButton.style.display = 'none';
    }
});

fileInput.addEventListener('change', function () {
    if (fileInput.files.length > 0) {
        selectedFile.textContent = fileInput.files[0].name;
        submitButton.style.display = 'block';
    } else {
        selectedFile.textContent = 'No file selected';
        submitButton.style.display = 'none';
    }
});
