import os
from pathlib import Path
from dotenv import load_dotenv
from textgrid_converter import TextGridConverter
from srt_divider import SRTDivider
from openai_processor import OpenAIProcessor
from srt_to_json import SRTToJSON
from whisper_processor import WhisperProcessor

def main():
    # Load environment variables
    load_dotenv()

    # Get project name from environment or use default
    project_name = os.getenv("PROJECT_NAME", "default")

    # Setup paths
    input_dir = Path("input") / project_name
    output_dir = Path("output") / project_name

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize processors
    whisper_processor = WhisperProcessor(
        output_dir=os.path.join("output", project_name)
    )

    # Step 0: Convert WAV to TextGrid using Whisper
    input_wav = input_dir / f"{project_name}.wav"
    output_textgrid = output_dir / f"{project_name}.TextGrid"
    whisper_processor.transcribe_to_textgrid(input_wav, output_textgrid)

    # Step 1: Convert TextGrid to SRT
    converter = TextGridConverter()
    output_srt = output_dir / f"{project_name}.srt"
    converter.convert(output_textgrid, output_srt)

    # Step 2: Divide SRT into smaller chunks
    divider = SRTDivider()
    split_dir = output_dir / "split"
    split_dir.mkdir(exist_ok=True)
    divider.divide(output_srt, split_dir)

    # Step 3: Process each chunk with OpenAI
    processor = OpenAIProcessor()
    divided_output_dir = output_dir / "divided_output"
    divided_output_dir.mkdir(exist_ok=True)
    processor.process_directory(split_dir, divided_output_dir)

    # Step 4: Merge processed chunks
    final_output = output_dir / "merged_output.srt"
    processor.merge_files(divided_output_dir, final_output)

    # Step 5: Convert final SRT to JSON
    json_converter = SRTToJSON()
    json_output = output_dir / "merged_output.json"
    json_converter.convert(final_output, json_output)

    print(f"Processing complete. Final outputs:")
    print(f"- TextGrid: {output_textgrid}")
    print(f"- SRT: {final_output}")
    print(f"- JSON: {json_output}")

if __name__ == "__main__":
    main()
