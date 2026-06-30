import pathlib

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.core.database import Base, engine
from app.api.router import api_router

ROOT = pathlib.Path(__file__).resolve().parent.parent

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Customer Support Agent",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")
_templates = Jinja2Templates(directory=str(ROOT / "templates"))

app.include_router(api_router)


@app.get("/")
def chat_page(request: Request):
    return _templates.TemplateResponse("chat.html", {"request": request})


@app.get("/dashboard")
def dashboard_page(request: Request):
    return _templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "env": settings.environment,
    }
