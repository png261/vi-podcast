from fastapi import APIRouter
from app.schemas import TranscriptInput, TranscriptOutput
from app.services.transcript_service import generate_transcript

router = APIRouter()


@router.post("/transcript",
             response_model=TranscriptOutput,
             summary="Generate podcast transcript for sources",
             tags=["Transcript Generation"])
async def transcript_endpoint(data: TranscriptInput) -> TranscriptOutput:
    return generate_transcript(data)
