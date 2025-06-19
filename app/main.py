from fastapi import FastAPI
from app.endpoints import transcript, audio

app = FastAPI(
    title="vi-podcast",
    version="1.0.0"
)

app.include_router(transcript.router, prefix="/api")
app.include_router(audio.router, prefix="/api")
