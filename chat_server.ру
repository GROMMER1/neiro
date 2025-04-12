
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import torch
from train_text_generator import TextGenerator, SimpleTokenizer

app = FastAPI()

tokenizer = SimpleTokenizer(["hello world", "hi there", "how are you"])
vocab_size = tokenizer.vocab_size()
model = TextGenerator(vocab_size, 128, 256)
model.load_state_dict(torch.load("text_generator.pth", weights_only=False))
model.eval()

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get():
    return """
    <html>
    <head><title>Чат</title></head>
    <body>
        <h2>Нейро-чат</h2>
        <div id='chat'></div>
        <input type='text' id='msg' placeholder='Введите сообщение...' />
        <button onclick='send()'>Отправить</button>
        <script>
        async function send() {
            let msg = document.getElementById("msg").value;
            let res = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({message: msg})
            });
            let data = await res.json();
            document.getElementById("chat").innerHTML += "<p><b>Вы:</b> " + msg + "<br/><b>Бот:</b> " + data.response + "</p>";
            document.getElementById("msg").value = "";
        }
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat(req: ChatRequest):
    tokens = tokenizer.encode(req.message)
    input_tensor = torch.tensor(tokens).unsqueeze(0)
    generated = []
    hidden = None
    with torch.no_grad():
        for _ in range(20):
            output, hidden = model(input_tensor, hidden)
            next_token = output[:, -1, :].argmax(dim=-1)
            generated.append(next_token.item())
            input_tensor = next_token.unsqueeze(0).unsqueeze(0)
    response = tokenizer.decode(generated)
    return JSONResponse(content={"response": response})
