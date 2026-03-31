from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from support_bot.bot import get_response
from support_bot.logger import get_logger

log = get_logger(__name__)
app = FastAPI(title="Support Bot API", version="0.1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


class ChatResponse(BaseModel):
    answer: str
    source: str


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    log.info(f"Message: {req.message[:60]}")
    result = get_response(req.message, req.history)
    return ChatResponse(**result)


@app.get("/health")
def health():
    return {"status": "ok"}