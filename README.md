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

   This project requires a Gemini API key.  
   Create a `.env` file in the project root with the following content:

   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   Replace `your_gemini_api_key_here` with your actual Gemini API key.

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
    "language": "vi"
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
    "audio_files": [
      { "id": "0", "url": "data/audio/20250619102000_abcd1234/0_speaker1.mp3" },
      { "id": "1", "url": "data/audio/20250619102000_abcd1234/1_speaker2.mp3" }
    ]
  }
  ```
