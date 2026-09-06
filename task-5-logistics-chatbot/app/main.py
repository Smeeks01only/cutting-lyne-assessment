from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routes import chat

description = """
Logistics Chatbot API is a **technical-assessment prototype** for Cutting Lyne Freight & Logistics.
"""

app = FastAPI(
    title="Cutting Lyne - Task 5 Chatbot API",
    description=description,
    version="1.0.0"
)

# Mount frontend assets
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Register the chat endpoints
app.include_router(chat.router)

@app.get("/")
async def serve_frontend(request: Request):
    """Serves the Chatbot HTML UI."""
    return templates.TemplateResponse(request=request, name="index.html")
