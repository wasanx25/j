# Audio Transcription Project

This project transcribes audio files using OpenAI's Whisper API and saves the output as SRT files.

## Prerequisites

- Python 3.6 or higher
- OpenAI API key

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd abc
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Place your audio file (e.g., `new-type.wav`) in the `input/new-type/` directory.

2. Run the transcription script with the project name:
   ```bash
   PROJECT_NAME=new-type python3 src/main.py
   ```

3. The transcribed SRT file will be saved in the `output/new-type/` directory as `new-type-1.srt`.

## Notes

- Ensure your audio file is in a supported format (e.g., WAV).
- The project name should match the directory name under `input/`.
