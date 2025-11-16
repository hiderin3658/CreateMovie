#!/usr/bin/env python3
"""
Subtitle Generator
Automatically generates subtitle lines for storyboard based on dialogue mode
"""
from typing import List, Optional, Any
import re


class SubtitleGenerator:
    """
    Generate subtitle lines for storyboard cuts

    Supports 3 dialogue modes with different subtitle styles:
    - narration: Optional full subtitles (often no subtitles in documentary)
    - monologue: Full subtitles without speaker name
    - dialogue: Subtitles with or without speaker names
    """

    # Maximum characters per subtitle line (Japanese)
    MAX_CHARS_PER_LINE = 40

    # Characters per second for Japanese reading speed
    CHARS_PER_SECOND = 5.0  # Slower reading speed for comfortable viewing

    def __init__(self):
        """Initialize subtitle generator"""
        pass

    def split_text_into_lines(self, text: str, max_chars: int = MAX_CHARS_PER_LINE) -> List[str]:
        """
        Split long text into multiple subtitle lines

        Args:
            text: Text to split
            max_chars: Maximum characters per line

        Returns:
            List of subtitle line texts
        """
        if len(text) <= max_chars:
            return [text]

        lines = []
        current_line = ""

        # Split by punctuation marks (。、！？)
        segments = re.split(r'([。、！？])', text)

        for i in range(0, len(segments), 2):
            segment = segments[i]
            punct = segments[i+1] if i+1 < len(segments) else ""
            full_segment = segment + punct

            if len(current_line) + len(full_segment) <= max_chars:
                current_line += full_segment
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = full_segment
                else:
                    # Segment itself is too long, split by characters
                    words = list(full_segment)
                    temp_line = ""
                    for word in words:
                        if len(temp_line) + 1 <= max_chars:
                            temp_line += word
                        else:
                            lines.append(temp_line)
                            temp_line = word
                    if temp_line:
                        current_line = temp_line

        if current_line:
            lines.append(current_line)

        return lines if lines else [text]

    def calculate_timing(
        self,
        text: str,
        total_duration: float,
        num_lines: int = 1,
        line_index: int = 0
    ) -> tuple:
        """
        Calculate start and end times for a subtitle line

        Args:
            text: Subtitle text
            total_duration: Total duration available for all lines
            num_lines: Total number of subtitle lines
            line_index: Index of this line (0-based)

        Returns:
            (start_time, end_time) in seconds
        """
        # Calculate duration based on text length
        min_duration = len(text) / self.CHARS_PER_SECOND

        # Distribute time evenly among lines, but respect minimum duration
        if num_lines == 1:
            duration = max(min_duration, total_duration)
            return (0.0, duration)

        # For multiple lines, divide time proportionally
        time_per_line = total_duration / num_lines
        start_time = line_index * time_per_line
        end_time = start_time + max(min_duration, time_per_line)

        # Clamp end_time to total_duration
        end_time = min(end_time, total_duration)

        return (start_time, end_time)

    def generate_narration_subtitles(
        self,
        cut: Any,
        style: str = 'auto'
    ) -> List[Any]:
        """
        Generate subtitles for narration mode

        Args:
            cut: CutData object
            style: 'auto', 'none', or 'full'

        Returns:
            List of SubtitleLine objects
        """
        from .storyboard_generator import SubtitleLine

        # Auto mode: No subtitles for documentary-style narration
        if style == 'auto':
            style = 'none' if cut.narration_style == 'documentary' else 'full'

        if style == 'none' or not cut.narration_text:
            return []

        # Generate full subtitles
        text_lines = self.split_text_into_lines(cut.narration_text)
        subtitle_lines = []

        duration = cut.narration_duration or cut.duration

        for i, text in enumerate(text_lines):
            start_time, end_time = self.calculate_timing(
                text, duration, len(text_lines), i
            )

            subtitle_lines.append(SubtitleLine(
                text=text,
                start_time=start_time,
                end_time=end_time,
                speaker=None
            ))

        return subtitle_lines

    def generate_monologue_subtitles(
        self,
        cut: Any,
        style: str = 'auto'
    ) -> List[Any]:
        """
        Generate subtitles for monologue mode

        Args:
            cut: CutData object
            style: 'auto' or 'without_speaker' (speaker name not shown for monologue)

        Returns:
            List of SubtitleLine objects
        """
        from .storyboard_generator import SubtitleLine

        if not cut.monologue_text:
            return []

        # Monologue: No speaker name in subtitles (viewer can see who's speaking)
        text_lines = self.split_text_into_lines(cut.monologue_text)
        subtitle_lines = []

        duration = cut.monologue_duration or cut.duration

        for i, text in enumerate(text_lines):
            start_time, end_time = self.calculate_timing(
                text, duration, len(text_lines), i
            )

            subtitle_lines.append(SubtitleLine(
                text=text,
                start_time=start_time,
                end_time=end_time,
                speaker=None  # No speaker name for monologue
            ))

        return subtitle_lines

    def generate_dialogue_subtitles(
        self,
        cut: Any,
        style: str = 'auto'
    ) -> List[Any]:
        """
        Generate subtitles for dialogue mode

        Args:
            cut: CutData object
            style: 'auto', 'with_speaker', or 'without_speaker'

        Returns:
            List of SubtitleLine objects
        """
        from .storyboard_generator import SubtitleLine

        if not cut.dialogue_lines:
            return []

        # Auto mode: Include speaker names for clarity
        include_speaker = (style == 'auto' or style == 'with_speaker')

        subtitle_lines = []
        cumulative_time = 0.0

        for dialogue_line in cut.dialogue_lines:
            # Format text with or without speaker
            if include_speaker:
                text = f"{dialogue_line.speaker}: {dialogue_line.text}"
            else:
                text = dialogue_line.text

            # Split if too long
            text_segments = self.split_text_into_lines(text)

            # Calculate duration for this dialogue line
            line_duration = dialogue_line.duration or 3.0

            for i, segment in enumerate(text_segments):
                start_time, end_time = self.calculate_timing(
                    segment, line_duration, len(text_segments), i
                )

                subtitle_lines.append(SubtitleLine(
                    text=segment,
                    start_time=cumulative_time + start_time,
                    end_time=cumulative_time + end_time,
                    speaker=dialogue_line.speaker if include_speaker else None
                ))

            cumulative_time += line_duration

        return subtitle_lines

    def generate_subtitles_for_cut(
        self,
        cut: Any,
        style: Optional[str] = None
    ) -> List[Any]:
        """
        Generate subtitles for a single cut based on dialogue mode

        Args:
            cut: CutData object
            style: Override subtitle style (if None, uses cut.subtitle_style)

        Returns:
            List of SubtitleLine objects
        """
        if not cut.subtitle_enabled:
            return []

        # Use provided style or default to cut's style
        subtitle_style = style or cut.subtitle_style

        # Generate based on dialogue mode
        if cut.dialogue_mode == 'narration':
            return self.generate_narration_subtitles(cut, subtitle_style)
        elif cut.dialogue_mode == 'monologue':
            return self.generate_monologue_subtitles(cut, subtitle_style)
        elif cut.dialogue_mode == 'dialogue':
            return self.generate_dialogue_subtitles(cut, subtitle_style)
        else:
            return []

    def generate_subtitles_for_storyboard(
        self,
        cuts: List[Any],
        default_style: str = 'auto'
    ) -> List[Any]:
        """
        Generate subtitles for entire storyboard

        Args:
            cuts: List of CutData objects
            default_style: Default subtitle style for all cuts

        Returns:
            List of CutData objects with subtitles added
        """
        print(f"\n📝 Generating subtitles for storyboard...")

        for i, cut in enumerate(cuts):
            # Skip if subtitles disabled
            if not cut.subtitle_enabled:
                print(f"  Cut {cut.cut_number}: Subtitles disabled")
                continue

            # Generate subtitles
            subtitle_lines = self.generate_subtitles_for_cut(cut, default_style)

            # Assign to cut
            cut.subtitle_lines = subtitle_lines

            # Report
            if subtitle_lines:
                mode_emoji = {
                    'narration': '🎙️',
                    'monologue': '💭',
                    'dialogue': '💬'
                }
                emoji = mode_emoji.get(cut.dialogue_mode, '📝')
                print(f"  Cut {cut.cut_number} {emoji}: {len(subtitle_lines)} subtitle lines")
            else:
                print(f"  Cut {cut.cut_number}: No subtitles")

        print(f"✅ Subtitle generation complete!\n")
        return cuts

    def format_subtitle_srt(self, cut: Any, cut_start_time: float = 0.0) -> str:
        """
        Format subtitles as SRT (SubRip) format

        Args:
            cut: CutData object with subtitle_lines
            cut_start_time: Start time of this cut in the full video (seconds)

        Returns:
            SRT formatted string
        """
        if not cut.subtitle_lines:
            return ""

        srt_lines = []
        for i, subtitle in enumerate(cut.subtitle_lines, 1):
            # Calculate absolute times
            start = cut_start_time + subtitle.start_time
            end = cut_start_time + subtitle.end_time

            # Format time as HH:MM:SS,mmm
            start_str = self._format_srt_time(start)
            end_str = self._format_srt_time(end)

            # SRT entry
            srt_lines.append(f"{i}")
            srt_lines.append(f"{start_str} --> {end_str}")
            srt_lines.append(subtitle.text)
            srt_lines.append("")  # Blank line between entries

        return "\n".join(srt_lines)

    def _format_srt_time(self, seconds: float) -> str:
        """Format seconds as SRT time (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def export_srt(self, cuts: List[Any], output_path: str) -> bool:
        """
        Export all subtitles as SRT file

        Args:
            cuts: List of CutData objects
            output_path: Output SRT file path

        Returns:
            True if successful
        """
        try:
            cumulative_time = 0.0
            all_srt = []

            for cut in cuts:
                if cut.subtitle_lines:
                    srt_text = self.format_subtitle_srt(cut, cumulative_time)
                    all_srt.append(srt_text)

                cumulative_time += cut.duration

            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(all_srt))

            print(f"✅ Exported subtitles to {output_path}")
            return True

        except Exception as e:
            print(f"❌ Failed to export SRT: {e}")
            return False
