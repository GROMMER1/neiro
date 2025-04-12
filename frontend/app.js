function setTheme(theme) {
  document.body.className = theme;
}

async function sendPrompt() {
  const prompt = document.getElementById("prompt").value;
  const responseDiv = document.getElementById("response");
  responseDiv.innerHTML = "Генерация ответа...";

  try {
    const res = await fetch("/generate-text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });

    const data = await res.json();
    responseDiv.innerHTML = `<pre>${data.response}</pre>`;
  } catch (err) {
    responseDiv.innerHTML = "Ошибка при обращении к API.";
  }
}
