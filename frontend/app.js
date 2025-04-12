
function showTab(id) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    event.target.classList.add('active');
}

function sendChat() {
    const input = document.getElementById('chat-input').value;
    fetch('/generate-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: input })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('chat-response').innerText = data.response;
    });
}

function generateImage() {
    const input = document.getElementById('image-prompt').value;
    fetch('/generate-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: input })
    })
    .then(res => res.json())
    .then(data => {
        const img = `<img src="data:image/png;base64,${data.image_base64}" alt="Generated Image" />`;
        document.getElementById('image-result').innerHTML = img;
    });
}


function uploadImage() {
    const fileInput = document.getElementById('upload-file');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload-image', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        const img = `<p>Обработанное изображение:</p><img src="data:image/png;base64,${data.processed_image_base64}" />`;
        document.getElementById('upload-result').innerHTML = img;
    });
}
