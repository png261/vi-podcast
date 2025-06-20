from app.schemas import AudioInput, AudioOutput, AudioFile
from podcastfy.text_to_speech import TextToSpeech
from app.services.storage_service import upload_file
import uuid
import json
from datetime import datetime


def generate_audio(data: AudioInput) -> AudioOutput:
    podcast_id = datetime.now().strftime(
        "%Y%m%d%H%M%S") + "_" + uuid.uuid4().hex[:8]
    des_folder = f"vipodcast/{podcast_id}"

    transcript_json = json.dumps(
        [line.dict() for line in data.transcript], ensure_ascii=False, indent=2)
    transcript_key = f"{des_folder}/audio/transcript.txt"
    transcript_url = upload_file(transcript_json.encode("utf-8"), transcript_key,
                                 "application/json; charset=utf-8")

    text_to_speech = TextToSpeech(model="edge")

    if data.voice_map is None:
        data.voice_map = {
            "1": "vi-VN-HoaiMyNeural",
            "2": "vi-VN-NamMinhNeural"
        }

    audio_urls = []
    provider_config = text_to_speech._get_provider_config()

    for line in data.transcript:
        filename = f"{line.id}_speaker{
            line.speaker_id}.mp3"
        voice = data.voice_map.get(line.speaker_id)
        model = provider_config.get("model")

        audio_data = text_to_speech.provider.generate_audio(
            line.text, voice, model)
        r2_key = f"{des_folder}/audio/{filename}"
        r2_url = upload_file(audio_data, r2_key)

        audio_urls.append(AudioFile(id=str(line.id), url=r2_url))

    return AudioOutput(podcast_id=podcast_id, transcript_url=transcript_url, audio_urls=audio_urls)
