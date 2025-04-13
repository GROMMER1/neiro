from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Абсолютный путь к папке frontend/dist
frontend_path = Path(__file__).parent.parent / "frontend" / "dist"
app.mount("/static", StaticFiles(directory=frontend_path, html=True), name="static")

# Отдача index.html на любые пути (SPA)
@app.get("/{path:path}")
async def serve_spa():
    return FileResponse(frontend_path / "index.html")
