
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


function generateExtra() {
    const mode = document.getElementById('extra-mode').value;
    const input = document.getElementById('extra-input').value;
    const endpoint = mode === 'article' ? '/generate-article' : '/generate-code';

    fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: input })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('extra-output').innerText = data.response;
    });
}


function changeLanguage() {
    const lang = document.getElementById('language').value;
    document.documentElement.lang = lang;
    alert(lang === 'ru' ? 'Язык переключён на русский' : 'Language switched to English');
}

function startVoiceInput() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = document.getElementById('language').value === 'ru' ? 'ru-RU' : 'en-US';
    recognition.start();
    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        document.getElementById('text-input').value = text;
    };
    recognition.onerror = function(event) {
        alert("Ошибка распознавания: " + event.error);
    };
}


function generateVideo() {
    const prompt = document.getElementById('video-prompt').value;
    const video = document.getElementById('video-output');

    // Заглушка: показываем демонстрационное видео
    video.src = "https://samplelib.com/lib/preview/mp4/sample-5s.mp4";
    video.load();
    video.play();
}

function speakText() {
    const text = document.getElementById('speak-text').value;
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = document.getElementById('language').value === 'ru' ? 'ru-RU' : 'en-US';
    synth.speak(utterance);
}
