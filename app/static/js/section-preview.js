document.getElementById('custom-label').addEventListener('click', function() {
    document.getElementById('input_cover-proj').click();
});

document.getElementById('input_cover-proj').addEventListener('change', function(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];
    const fileNameSpan = document.getElementById('file-name');
    const imgPreview = document.getElementById('preview-img');

    if (file) {
        fileNameSpan.textContent = file.name;

        const reader = new FileReader();
        reader.onload = function(e) {
            imgPreview.src = e.target.result;
            imgPreview.style.display = 'block';
        }
        reader.readAsDataURL(file);
    } else {
        fileNameSpan.textContent = '';
        imgPreview.style.display = 'none';
    }
});
