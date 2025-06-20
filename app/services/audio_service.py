import os
import uuid
from datetime import datetime
from app.schemas import AudioInput, AudioOutput, AudioFile
from podcastfy.text_to_speech import TextToSpeech
from app.services.storage_service import upload_file


def generate_audio(data: AudioInput) -> AudioOutput:
    text_to_speech = TextToSpeech(model="edge")

    if data.voice_map is None:
        data.voice_map = {
            "1": "vi-VN-HoaiMyNeural",
            "2": "vi-VN-NamMinhNeural"
        }

    # Generate a unique folder using timestamp + UUID
    unique_folder_name = datetime.now().strftime(
        "%Y%m%d%H%M%S") + "_" + uuid.uuid4().hex[:8]
    temp_dir = os.path.join("data/audio", unique_folder_name)
    os.makedirs(temp_dir, exist_ok=True)

    audio_files = []
    provider_config = text_to_speech._get_provider_config()

    for line in data.transcript:
        filename = f"{line.id}_speaker{
            line.speaker_id}.mp3"
        temp_file = os.path.join(temp_dir, filename)
        voice = data.voice_map.get(line.speaker_id)
        model = provider_config.get("model")

        audio_data = text_to_speech.provider.generate_audio(
            line.text, voice, model)
        with open(temp_file, "wb") as f:
            f.write(audio_data)
        r2_key = f"vipodcast/{unique_folder_name}/{filename}"
        r2_url = upload_file(audio_data, r2_key)

        audio_files.append(AudioFile(id=str(line.id), url=r2_url))

    return AudioOutput(audio_files=audio_files)
