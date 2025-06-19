from fastapi import APIRouter
from app.schemas import AudioInput, AudioOutput
from app.services.audio_service import generate_audio

router = APIRouter()


@router.post("/audio",
             response_model=AudioOutput,
             summary="Generate audio from transcript",
             tags=["Audio Generation"])
async def audio_endpoint(data: AudioInput) -> AudioOutput:
    return generate_audio(data)
