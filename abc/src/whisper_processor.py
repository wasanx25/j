import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

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
                    model="whisper-1",
                    file=audio,
                    response_format="srt"
                )

            # Save the SRT content to a file
            # TODO: この SRT ファイルの出力時点で、句切れのない SRT ファイルになっている
            srt_output_path = os.path.join(self.output_dir, f"{os.path.splitext(os.path.basename(audio_file))[0]}-1.srt")
            with open(srt_output_path, "w", encoding="utf-8") as f:
                f.write(transcript)

            print(f"SRT file saved to: {srt_output_path}")

        except Exception as e:
            print(f"Error processing audio file {audio_file}: {e}")

    def _create_textgrid(self, transcript) -> str:
        """Create TextGrid content from Whisper transcript."""
        # TextGridのヘッダー部分
        textgrid = """File type = "ooTextFile"
Object class = "TextGrid"

xmin = 0
xmax = {duration}
tiers? <exists>
size = 1
item []:
    item [1]:
        class = "IntervalTier"
        name = "transcript"
        xmin = 0
        xmax = {duration}
        intervals: size = {num_segments}
""".format(
            duration=transcript.duration,
            num_segments=len(transcript.segments)
        )

        # 各セグメントをTextGrid形式に変換
        for i, segment in enumerate(transcript.segments, 1):
            textgrid += f"""        intervals [{i}]:
            xmin = {segment.start}
            xmax = {segment.end}
            text = "{segment.text}"
"""

        return textgrid

    def process_directory(self, input_dir: Path, output_dir: Path) -> None:
        """Process all WAV files in a directory."""
        output_dir.mkdir(parents=True, exist_ok=True)

        for input_file in input_dir.glob("*.wav"):
            output_file = output_dir / f"{input_file.stem}.TextGrid"
            self.transcribe_to_textgrid(input_file, output_file)
