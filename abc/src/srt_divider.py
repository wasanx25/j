import re
from pathlib import Path
from typing import List, Tuple

class SRTDivider:
    def __init__(self, max_chunk_size: int = 10):
        self.max_chunk_size = max_chunk_size
        self.entry_pattern = re.compile(
            r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)',
            re.DOTALL
        )

    def divide(self, input_file: Path, output_dir: Path) -> None:
        """Divide a large SRT file into smaller chunks."""
        try:
            # Read input file
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse SRT entries
            entries = self._parse_entries(content)

            # Divide into chunks
            chunks = self._create_chunks(entries)

            # Write chunks to separate files
            self._write_chunks(chunks, output_dir)
        except Exception as e:
            print(f"Error dividing SRT file: {e}")

    def _parse_entries(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Parse SRT content into list of entries."""
        entries = []
        matches = self.entry_pattern.finditer(content)

        for match in matches:
            index = int(match.group(1))
            start_time = match.group(2)
            end_time = match.group(3)
            text = match.group(4).strip()
            entries.append((index, start_time, end_time, text))

        return entries

    def _create_chunks(self, entries: List[Tuple[int, str, str, str]]) -> List[List[Tuple[int, str, str, str]]]:
        """Divide entries into chunks of specified size."""
        chunks = []
        current_chunk = []

        for entry in entries:
            current_chunk.append(entry)
            if len(current_chunk) >= self.max_chunk_size:
                chunks.append(current_chunk)
                current_chunk = []

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _write_chunks(self, chunks: List[List[Tuple[int, str, str, str]]], output_dir: Path) -> None:
        """Write chunks to separate SRT files."""
        output_dir.mkdir(parents=True, exist_ok=True)

        for i, chunk in enumerate(chunks, 1):
            output_file = output_dir / f"chunk_{i:03d}.srt"
            with open(output_file, 'w', encoding='utf-8') as f:
                for j, (_, start_time, end_time, text) in enumerate(chunk, 1):
                    f.write(f"{j}\n{start_time} --> {end_time}\n{text}\n\n")
