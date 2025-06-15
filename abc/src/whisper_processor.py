import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import json

class WhisperProcessor:
    def __init__(self, output_dir: str = "output"):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def transcribe_to_textgrid(self, audio_file: Path, output_file: Path) -> None:
        """Convert audio file to TextGrid format using Whisper."""
        try:
            # 音声ファイルを読み込む
            with open(audio_file, "rb") as audio:
                # Whisper APIを使用して文字起こし
                transcript = self.client.audio.transcriptions.create(
                    model="gpt-4o-transcribe",
                    file=audio,
                    response_format="json"
                )

            # Save the SRT content to a file
            # TODO: この SRT ファイルの出力時点で、句切れのない SRT ファイルになっている
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(transcript.to_dict(), f, ensure_ascii=False, indent=2)

            print(f"JSON file saved to: {output_file}")

        except Exception as e:
            print(f"Error processing audio file {audio_file}: {e}")


    def process_directory(self, input_dir: Path, output_dir: Path) -> None:
        """Process all WAV files in a directory."""
        output_dir.mkdir(parents=True, exist_ok=True)

        for input_file in input_dir.glob("*.wav"):
            output_file = output_dir / f"{input_file.stem}.TextGrid"
            self.transcribe_to_textgrid(input_file, output_file)
