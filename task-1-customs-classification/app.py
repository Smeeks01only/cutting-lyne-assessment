import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Add project root to sys.path to allow importing from src
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.predictor import classify_product

app = FastAPI(title="Customs Classification API")

# Setup Jinja2 templates for the frontend
templates_dir = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


class ClassificationRequest(BaseModel):
    description: str


@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    """
    Serves the main HTML interface.
    """
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.post("/api/classify")
async def api_classify_product(req: ClassificationRequest):
    """
    API endpoint to classify a product description.
    """
    result = classify_product(req.description)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
