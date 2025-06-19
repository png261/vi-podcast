from typing import List, Dict, Optional
from pydantic import BaseModel, HttpUrl


class TranscriptInput(BaseModel):
    text: str
    image_urls: List[HttpUrl] = []
    source_urls: List[HttpUrl] = []
    language: str


class Line(BaseModel):
    id: str
    speaker_id: str
    text: str


class TranscriptOutput(BaseModel):
    transcript: List[Line]


class AudioInput(BaseModel):
    transcript: List[Line]
    voice_map: Optional[Dict[str, str]] = None


class AudioFile(BaseModel):
    id: str
    url: str


class AudioOutput(BaseModel):
    audio_files: List[AudioFile]
