import re
from pathlib import Path
from typing import List, Tuple

class TextGridConverter:
    def __init__(self):
        self.time_pattern = re.compile(r'xmin = (\d+\.?\d*)')
        self.text_pattern = re.compile(r'text = "(.*?)"')

    def convert(self, input_file: Path, output_file: Path) -> None:
        """Convert TextGrid file to SRT format."""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract intervals
            intervals = self._extract_intervals(content)

            # Convert to SRT format
            srt_content = self._create_srt(intervals)

            # Write to output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(srt_content)
        except Exception as e:
            print(f"Error converting TextGrid to SRT: {e}")

    def _extract_intervals(self, content: str) -> List[Tuple[float, float, str]]:
        """Extract intervals from TextGrid content."""
        intervals = []
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith('intervals ['):
                start_time = None
                end_time = None
                text = None
                # Get start time
                i += 1
                while i < len(lines) and 'xmin =' not in lines[i].strip():
                    i += 1
                if i < len(lines):
                    start_match = self.time_pattern.search(lines[i].strip())
                    if start_match:
                        start_time = float(start_match.group(1))
                # Get end time
                i += 1
                while i < len(lines) and 'xmax =' not in lines[i].strip():
                    i += 1
                if i < len(lines):
                    end_match = re.search(r'xmax = (\d+\.?\d*)', lines[i].strip())
                    if end_match:
                        end_time = float(end_match.group(1))
                # Get text
                i += 1
                while i < len(lines) and 'text =' not in lines[i].strip():
                    i += 1
                if i < len(lines):
                    text_match = self.text_pattern.search(lines[i].strip())
                    if text_match:
                        text = text_match.group(1)
                if start_time is not None and end_time is not None and text is not None:
                    intervals.append((start_time, end_time, text))
            i += 1
        return intervals

    def _create_srt(self, intervals: List[Tuple[float, float, str]]) -> str:
        """Create SRT content from intervals."""
        srt_entries = []

        for i, (start, end, text) in enumerate(intervals, 1):
            # Convert times to SRT format (HH:MM:SS,mmm)
            start_time = self._format_time(start)
            end_time = self._format_time(end)

            # Create SRT entry
            entry = f"{i}\n{start_time} --> {end_time}\n{text}\n"
            srt_entries.append(entry)

        return "\n".join(srt_entries)

    def _format_time(self, seconds: float) -> str:
        """Format seconds to SRT time format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        milliseconds = int((seconds - int(seconds)) * 1000)

        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"
