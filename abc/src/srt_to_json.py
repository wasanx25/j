import re
import json
from pathlib import Path
from typing import List, Dict

class SRTToJSON:
    def __init__(self):
        self.entry_pattern = re.compile(
            r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)',
            re.DOTALL
        )

    def convert(self, input_file: Path, output_file: Path) -> None:
        """Convert SRT file to JSON format."""
        try:
            # Read input file
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse SRT entries
            entries = self._parse_entries(content)

            # Convert to JSON format
            json_data = self._create_json(entries)

            # Write to output file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error converting SRT to JSON: {e}")

    def _parse_entries(self, content: str) -> List[Dict]:
        """Parse SRT content into list of entries."""
        entries = []
        matches = self.entry_pattern.finditer(content)

        for match in matches:
            entry = {
                'index': int(match.group(1)),
                'start_time': match.group(2),
                'end_time': match.group(3),
                'text': match.group(4).strip()
            }
            entries.append(entry)

        return entries

    def _create_json(self, entries: List[Dict]) -> Dict:
        """Create JSON structure from entries."""
        return {
            'subtitles': entries
        }
