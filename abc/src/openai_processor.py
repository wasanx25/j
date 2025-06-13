import os
from pathlib import Path
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

class OpenAIProcessor:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def process_directory(self, input_dir: Path, output_dir: Path) -> None:
        """Process all SRT files in the input directory."""
        for input_file in sorted(input_dir.glob("*.srt")):
            output_file = output_dir / f"{input_file.stem}_processed.srt"
            self.process_file(input_file, output_file)

    def process_file(self, input_file: Path, output_file: Path) -> None:
        """Process a single SRT file using OpenAI API."""
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Create prompt for OpenAI
        prompt = self._create_prompt(content)

        # Get response from OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=1000
        )

        # Write processed content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.choices[0].message.content)

    def merge_files(self, input_dir: Path, output_file: Path) -> None:
        """Merge all processed SRT files into a single file."""
        all_entries = []
        current_index = 1

        # Read and process all files
        for input_file in sorted(input_dir.glob("*_processed.srt")):
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse entries and update indices
            entries = self._parse_srt(content)
            for entry in entries:
                all_entries.append((current_index, entry[1], entry[2], entry[3]))
                current_index += 1

        # Write merged file
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in all_entries:
                f.write(f"{entry[0]}\n{entry[1]} --> {entry[2]}\n{entry[3]}\n\n")

    def _create_prompt(self, content: str) -> str:
        """Create a prompt for OpenAI to process the SRT content."""
        return f"""以下のSRTファイルの内容を処理してください。以下の点に注意して修正してください：

1. 文章の自然さを改善
2. 句読点の適切な配置
3. 改行位置の最適化
4. 字幕として読みやすい長さへの調整

入力SRT:
{content}

出力は同じSRTフォーマットで、タイムスタンプは保持してください。"""

    def _parse_srt(self, content: str) -> List[tuple]:
        """Parse SRT content into list of entries."""
        entries = []
        pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)'
        import re
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            index = int(match.group(1))
            start_time = match.group(2)
            end_time = match.group(3)
            text = match.group(4).strip()
            entries.append((index, start_time, end_time, text))

        return entries
