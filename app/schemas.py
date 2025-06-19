from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class TranscriptInput(BaseModel):
    text: str = Field(...,
                      description="Optional input text to supplement or guide the transcript.")
    image_urls: List[str] = Field(
        default_factory=list, description="List of image URLs to assist with content generation.")
    source_urls: List[str] = Field(
        default_factory=list, description="List of source URLs (e.g., articles, videos) for transcript generation.")


class Line(BaseModel):
    id: str = Field(...,
                    description="Unique identifier for the transcript line.")
    speaker_id: str = Field(
        ..., description="Identifier for the speaker (e.g., '1' for teacher, '2' for student).")
    text: str = Field(..., description="Text content spoken by the speaker.")


class TranscriptOutput(BaseModel):
    transcript: List[Line] = Field(
        ..., description="Generated transcript as a list of dialogue lines.")


class AudioInput(BaseModel):
    transcript: List[Line] = Field(...,
                                   description="Transcript to be converted into audio.")
    voice_map: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optional mapping of speaker_id to voice name (e.g., {'0': 'vi-VN-NamMinhNeural'})."
    )


class AudioFile(BaseModel):
    id: str = Field(..., description="Unique identifier for the audio file.")
    url: str = Field(...,
                     description="URL pointing to the generated audio file.")


class AudioOutput(BaseModel):
    audio_files: List[AudioFile] = Field(...,
                                         description="List of generated audio files.")
