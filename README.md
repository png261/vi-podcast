# vi-podcast

## How to run

1. **Clone the repository:**
   ```sh
   git clone https://github.com/png261/vi-podcast.git
   cd vi-podcast
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**

   Create a `.env` file in the project root with the following content:

   ```
   GEMINI_API_KEY=
   R2_ENDPOINT_URL=
   R2_ACCESS_KEY_ID=
   R2_SECRET_ACCESS_KEY=
   R2_BUCKET_NAME=
   R2_REGION=
   BASE_URL_S3=

   ```


4. **Run the application:**
   ```sh
   uvicorn app.main:app --reload
   ```

## API Endpoints

### 1. Generate Podcast Transcript

- **Endpoint:** `POST /api/transcript`
- **Request Body:**
  ```json
  {
    "text": "Your podcast topic content here.",
    "image_urls": [],
    "source_urls": [],
  }
  ```
- **Response Example:**
  ```json
  {
    "transcript": [
      { "id": "0", "speaker_id": "1", "text": "Chào mừng các bạn nhỏ!" },
      { "id": "1", "speaker_id": "2", "text": "Chúng ta hãy khám phá thế giới xung quanh nhé!" }
    ]
  }
  ```

### 2. Generate Audio from Transcript

- **Endpoint:** `POST /api/audio`
- **Request Body:**
  ```json
  {
    "transcript": [
      { "id": "0", "speaker_id": "1", "text": "Chào mừng các bạn nhỏ!" },
      { "id": "1", "speaker_id": "2", "text": "Chúng ta hãy khám phá thế giới xung quanh nhé!" }
    ],
    "voice_map": {
      "1": "vi-VN-HoaiMyNeural",
      "2": "vi-VN-NamMinhNeural"
    }
  }
  ```
- **Response Example:**
  ```json
  {
    podcast_id: "20250619102000_abcd1234", 
    transcript_url: "data/audio/20250619102000_abcd1234/transcript.txt", 
    "audio_files": [
      { "id": "0", "url": "data/audio/20250619102000_abcd1234/0_speaker1.mp3" },
      { "id": "1", "url": "data/audio/20250619102000_abcd1234/1_speaker2.mp3" }
    ]
  }
  ```
