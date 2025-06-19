import os
import uuid
from datetime import datetime
from app.schemas import AudioInput, AudioOutput, AudioFile
from podcastfy.text_to_speech import TextToSpeech


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

    audio_paths = []
    provider_config = text_to_speech._get_provider_config()

    for line in data.transcript:
        temp_file = os.path.join(temp_dir, f"{line.id}_speaker{
                                 line.speaker_id}.mp3")
        voice = data.voice_map.get(line.speaker_id)
        model = provider_config.get("model")

        audio_data = text_to_speech.provider.generate_audio(
            line.text, voice, model)
        with open(temp_file, "wb") as f:
            f.write(audio_data)
        audio_paths.append(temp_file)

    audio_files = [AudioFile(id=str(idx), url=path)
                   for idx, path in enumerate(audio_paths)]
    return AudioOutput(audio_files=audio_files)
