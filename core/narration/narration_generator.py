#!/usr/bin/env python3
"""
Narration Generator (Extended to support 3 dialogue modes)
Generates contextual narration, monologue, and dialogue for video storyboard cuts using Claude API

Modes:
1. Narration: Narrator voiceover (existing functionality)
2. Monologue: Single character speaking
3. Dialogue: Two characters conversing
"""
import os
from typing import List, Optional, Dict, Any

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class NarrationGenerator:
    """
    Generate contextual narration, monologue, and dialogue for video storyboard cuts

    Supports 3 modes:
    - narration: Narrator voiceover
    - monologue: Single character speaking
    - dialogue: Two characters conversing
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize narration generator

        Args:
            api_key: Anthropic API key (defaults to env ANTHROPIC_API_KEY)
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.use_claude = ANTHROPIC_AVAILABLE and self.api_key is not None

        if self.use_claude:
            self.client = Anthropic(api_key=self.api_key)
            self.model = "claude-3-5-sonnet-20241022"

    def analyze_narration_needs(
        self,
        cuts: List[Any],
        story_context: str,
        style: str = "documentary"
    ) -> List[bool]:
        """
        Analyze which cuts need narration

        Args:
            cuts: List of cut data
            story_context: Overall story description
            style: Narration style

        Returns:
            List of boolean flags indicating narration need
        """
        if not self.use_claude:
            print("Claude API not available, skipping narration analysis")
            return [False] * len(cuts)

        # Build analysis prompt
        cuts_summary = "\n".join([
            f"Cut {cut.cut_number} ({cut.duration}s): {cut.scene_description} - {cut.action}"
            for cut in cuts
        ])

        prompt = f"""You are analyzing a video storyboard to determine which cuts would benefit from narration/voiceover.

Story Context:
{story_context}

Narration Style: {style}

Cuts:
{cuts_summary}

For each cut, determine if narration would add value. Narration is typically helpful for:
- Establishing shots (setting context, location, time)
- Emotional moments (internal thoughts, feelings)
- Explanatory scenes (complex actions, technical details)
- Transitions (connecting scenes, time jumps)
- Opening/closing cuts

Narration is typically NOT needed for:
- Dialogue scenes (action/dialogue is self-explanatory)
- Pure action (fast-paced movement)
- Very short cuts (< 3 seconds)

Respond with ONLY a JSON array of boolean values, one for each cut, in order.
Example: [true, false, true, false, false, true]
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse response
            content = response.content[0].text.strip()
            # Extract JSON array from response
            import json
            import re
            json_match = re.search(r'\[.*\]', content)
            if json_match:
                needs = json.loads(json_match.group())
                return needs if len(needs) == len(cuts) else [False] * len(cuts)
            else:
                return [False] * len(cuts)

        except Exception as e:
            print(f"Error analyzing narration needs: {e}")
            return [False] * len(cuts)

    def generate_narration_text(
        self,
        cut: Any,
        story_context: str,
        previous_cuts: List[Any],
        style: str = "documentary"
    ) -> Optional[str]:
        """
        Generate narration text for a single cut

        Args:
            cut: Cut data
            story_context: Overall story description
            previous_cuts: Previous cuts for context
            style: Narration style

        Returns:
            Generated narration text or None
        """
        if not self.use_claude:
            return None

        # Build context from previous cuts
        prev_context = ""
        if previous_cuts:
            last_few = previous_cuts[-2:] if len(previous_cuts) > 2 else previous_cuts
            prev_context = "\n".join([
                f"Cut {c.cut_number}: {c.scene_description}"
                for c in last_few
            ])

        # Calculate max characters based on duration (Japanese: ~300 chars/min)
        max_chars = int((cut.duration / 60) * 300)

        prompt = f"""You are creating narration for a video storyboard.

Story Context:
{story_context}

Previous Cuts:
{prev_context if prev_context else "None (this is the first cut)"}

Current Cut (Cut {cut.cut_number}, {cut.duration}s):
- Scene: {cut.scene_description}
- Action: {cut.action}
- Mood: {cut.mood}
- Camera: {cut.camera_angle}, {cut.camera_movement}

Generate a {style} narration that:
1. Fits within {cut.duration}s (approximately {max_chars} Japanese characters)
2. Complements the visual without being redundant
3. Maintains narrative flow from previous cuts
4. Matches the {cut.mood} mood
5. Is written in Japanese (日本語)

Respond with ONLY the narration text, nothing else.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            narration = response.content[0].text.strip()
            # Remove any markdown formatting or quotes
            narration = narration.strip('"').strip("'").strip('`')
            return narration

        except Exception as e:
            print(f"Error generating narration for Cut {cut.cut_number}: {e}")
            return None

    def calculate_narration_timing(
        self,
        narration_text: str,
        cut_duration: int,
        scene_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Calculate optimal timing for narration

        Args:
            narration_text: Narration text
            cut_duration: Cut duration in seconds
            scene_type: Type of scene

        Returns:
            Dictionary with timing, duration, and placement info
        """
        # Estimate duration for Japanese text (~300 chars/min)
        char_count = len(narration_text)
        estimated_duration = (char_count / 300) * 60  # seconds

        # Adjust for punctuation (add pauses)
        pause_time = narration_text.count('。') * 0.5 + narration_text.count('、') * 0.3
        estimated_duration += pause_time

        # Determine optimal timing
        if estimated_duration >= cut_duration * 0.8:
            timing = "throughout"
        elif scene_type in ['opening', 'establishing']:
            timing = "start"
        elif scene_type in ['closing', 'conclusion']:
            timing = "end"
        else:
            timing = "start"

        return {
            'duration': round(estimated_duration, 1),
            'timing': timing,
            'char_count': char_count,
            'fits_in_cut': estimated_duration <= cut_duration
        }

    def generate_narrations_for_storyboard(
        self,
        cuts: List[Any],
        story_context: str,
        style: str = "documentary"
    ) -> List[Any]:
        """
        Generate narrations for entire storyboard

        Args:
            cuts: List of cut data
            story_context: Overall story description
            style: Narration style

        Returns:
            Updated cuts with narrations
        """
        if not self.use_claude:
            print("⚠️  Claude API not available, skipping narration generation")
            return cuts

        print(f"\n🎙️  Analyzing narration needs (style: {style})...")

        # Analyze which cuts need narration
        narration_needs = self.analyze_narration_needs(cuts, story_context, style)

        print(f"  ✓ {sum(narration_needs)}/{len(cuts)} cuts identified for narration")

        # Generate narrations for selected cuts
        print("\n🎙️  Generating narration text...")
        previous_cuts = []

        for i, (cut, needs_narration) in enumerate(zip(cuts, narration_needs)):
            cut.narration_needed = needs_narration

            if needs_narration:
                print(f"  Generating narration for Cut {cut.cut_number}...")

                narration = self.generate_narration_text(
                    cut,
                    story_context,
                    previous_cuts,
                    style
                )

                if narration:
                    cut.narration_text = narration
                    cut.narration_style = style

                    # Calculate timing
                    timing_info = self.calculate_narration_timing(
                        narration,
                        cut.duration
                    )

                    cut.narration_duration = timing_info['duration']
                    cut.narration_timing = timing_info['timing']

                    if not timing_info['fits_in_cut']:
                        print(f"    ⚠️  Warning: Narration ({timing_info['duration']}s) exceeds cut duration ({cut.duration}s)")
                    else:
                        print(f"    ✓ Generated ({timing_info['duration']}s, {timing_info['char_count']} chars)")

            previous_cuts.append(cut)

        narration_count = sum(1 for cut in cuts if cut.narration_text)
        print(f"\n✅ Generated {narration_count} narrations")

        return cuts

    def generate_monologue_text(
        self,
        cut: Any,
        story_context: str,
        character_name: str,
        character_context: str,
        previous_cuts: List[Any]
    ) -> Optional[str]:
        """
        Generate monologue text for a single character

        Args:
            cut: Cut data
            story_context: Overall story description
            character_name: Name of the character speaking
            character_context: Character background/personality
            previous_cuts: Previous cuts for context

        Returns:
            Generated monologue text or None
        """
        if not self.use_claude:
            return None

        # Build context from previous cuts
        prev_context = ""
        if previous_cuts:
            last_few = previous_cuts[-2:] if len(previous_cuts) > 2 else previous_cuts
            prev_context = "\n".join([
                f"Cut {c.cut_number}: {c.scene_description}"
                for c in last_few
            ])

        # Calculate max characters based on duration (Japanese: ~300 chars/min)
        max_chars = int((cut.duration / 60) * 300)

        prompt = f"""You are writing a monologue for a character in a video storyboard.

Story Context:
{story_context}

Character: {character_name}
Character Context: {character_context}

Previous Cuts:
{prev_context if prev_context else "None (this is the first cut)"}

Current Cut (Cut {cut.cut_number}, {cut.duration}s):
- Scene: {cut.scene_description}
- Action: {cut.action}
- Mood: {cut.mood}
- Camera: {cut.camera_angle}, {cut.camera_movement}

Generate a monologue where {character_name} speaks their thoughts that:
1. Fits within {cut.duration}s (approximately {max_chars} Japanese characters)
2. Reflects {character_name}'s personality and perspective
3. Advances the story or reveals character emotions
4. Matches the {cut.mood} mood
5. Is written in Japanese (日本語)
6. Uses natural, spoken language (not narration style)

Respond with ONLY the monologue text, nothing else.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            monologue = response.content[0].text.strip()
            # Remove any markdown formatting or quotes
            monologue = monologue.strip('"').strip("'").strip('`')
            return monologue

        except Exception as e:
            print(f"Error generating monologue for Cut {cut.cut_number}: {e}")
            return None

    def generate_dialogue_text(
        self,
        cut: Any,
        story_context: str,
        character1_name: str,
        character1_context: str,
        character2_name: str,
        character2_context: str,
        previous_cuts: List[Any]
    ) -> Optional[List[Dict]]:
        """
        Generate dialogue between two characters

        Args:
            cut: Cut data
            story_context: Overall story description
            character1_name: Name of first character
            character1_context: First character background
            character2_name: Name of second character
            character2_context: Second character background
            previous_cuts: Previous cuts for context

        Returns:
            List of dialogue lines [{'speaker': '...', 'text': '...'}] or None
        """
        if not self.use_claude:
            return None

        # Build context from previous cuts
        prev_context = ""
        if previous_cuts:
            last_few = previous_cuts[-2:] if len(previous_cuts) > 2 else previous_cuts
            prev_context = "\n".join([
                f"Cut {c.cut_number}: {c.scene_description}"
                for c in last_few
            ])

        # Calculate max characters based on duration
        max_chars = int((cut.duration / 60) * 300)

        prompt = f"""You are writing dialogue for two characters in a video storyboard.

Story Context:
{story_context}

Character 1: {character1_name}
Context: {character1_context}

Character 2: {character2_name}
Context: {character2_context}

Previous Cuts:
{prev_context if prev_context else "None (this is the first cut)"}

Current Cut (Cut {cut.cut_number}, {cut.duration}s):
- Scene: {cut.scene_description}
- Action: {cut.action}
- Mood: {cut.mood}
- Camera: {cut.camera_angle}, {cut.camera_movement}

Generate a natural dialogue between {character1_name} and {character2_name} that:
1. Fits within {cut.duration}s (approximately {max_chars} Japanese characters total)
2. Reflects each character's personality
3. Advances the story or reveals emotions/conflict
4. Matches the {cut.mood} mood
5. Is written in Japanese (日本語)
6. Has 2-4 back-and-forth exchanges

Respond in this exact JSON format:
[
  {{"speaker": "{character1_name}", "text": "..."}},
  {{"speaker": "{character2_name}", "text": "..."}},
  ...
]

Respond with ONLY the JSON array, nothing else.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text.strip()

            # Extract JSON array from response
            import json
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                dialogue_lines = json.loads(json_match.group())
                return dialogue_lines
            else:
                print(f"Warning: Could not parse dialogue JSON for Cut {cut.cut_number}")
                return None

        except Exception as e:
            print(f"Error generating dialogue for Cut {cut.cut_number}: {e}")
            return None

    def generate_dialogue_for_storyboard(
        self,
        cuts: List[Any],
        story_context: str,
        dialogue_mode: str = 'narration',
        character_info: Optional[Dict] = None,
        style: str = "documentary"
    ) -> List[Any]:
        """
        Generate dialogue/narration for entire storyboard with mode selection

        Args:
            cuts: List of cut data
            story_context: Overall story description
            dialogue_mode: 'narration', 'monologue', or 'dialogue'
            character_info: Dict with character information for monologue/dialogue modes
                           {'character1': {'name': '...', 'context': '...'},
                            'character2': {'name': '...', 'context': '...'}}
            style: Narration style (for narration mode only)

        Returns:
            Updated cuts with dialogue/narration
        """
        if not self.use_claude:
            print("⚠️  Claude API not available, skipping dialogue generation")
            return cuts

        print(f"\n🎙️  Generating dialogue (mode: {dialogue_mode})...")

        if dialogue_mode == 'narration':
            # Use existing narration generation
            return self.generate_narrations_for_storyboard(cuts, story_context, style)

        # Validate character_info for monologue/dialogue modes
        if not character_info:
            print("⚠️  Character info required for monologue/dialogue mode")
            return cuts

        previous_cuts = []

        for i, cut in enumerate(cuts):
            cut.dialogue_mode = dialogue_mode

            if dialogue_mode == 'monologue':
                # Generate monologue
                char1 = character_info.get('character1', {})
                char_name = char1.get('name', '主人公')
                char_context = char1.get('context', '')

                print(f"  Generating monologue for Cut {cut.cut_number} ({char_name})...")

                monologue = self.generate_monologue_text(
                    cut,
                    story_context,
                    char_name,
                    char_context,
                    previous_cuts
                )

                if monologue:
                    cut.monologue_character = char_name
                    cut.monologue_text = monologue

                    # Calculate duration
                    timing_info = self.calculate_narration_timing(
                        monologue,
                        cut.duration
                    )
                    cut.monologue_duration = timing_info['duration']

                    if not timing_info['fits_in_cut']:
                        print(f"    ⚠️  Warning: Monologue ({timing_info['duration']}s) exceeds cut duration ({cut.duration}s)")
                    else:
                        print(f"    ✓ Generated ({timing_info['duration']}s, {timing_info['char_count']} chars)")

            elif dialogue_mode == 'dialogue':
                # Generate dialogue
                char1 = character_info.get('character1', {})
                char2 = character_info.get('character2', {})

                char1_name = char1.get('name', 'キャラA')
                char1_context = char1.get('context', '')
                char2_name = char2.get('name', 'キャラB')
                char2_context = char2.get('context', '')

                print(f"  Generating dialogue for Cut {cut.cut_number} ({char1_name} & {char2_name})...")

                dialogue_lines = self.generate_dialogue_text(
                    cut,
                    story_context,
                    char1_name,
                    char1_context,
                    char2_name,
                    char2_context,
                    previous_cuts
                )

                if dialogue_lines:
                    # Import DialogueLine class
                    from ..video.storyboard_generator import DialogueLine

                    # Convert to DialogueLine objects with duration estimates
                    dialogue_objs = []
                    total_chars = sum(len(line['text']) for line in dialogue_lines)
                    total_duration = cut.duration

                    for line in dialogue_lines:
                        # Estimate duration based on character count proportion
                        line_chars = len(line['text'])
                        line_duration = (line_chars / total_chars) * total_duration if total_chars > 0 else 0

                        dialogue_objs.append(DialogueLine(
                            speaker=line['speaker'],
                            text=line['text'],
                            duration=round(line_duration, 1)
                        ))

                    cut.dialogue_lines = dialogue_objs
                    cut.dialogue_characters = [char1_name, char2_name]

                    total_duration_calc = sum(d.duration for d in dialogue_objs if d.duration)
                    print(f"    ✓ Generated {len(dialogue_objs)} lines ({total_duration_calc:.1f}s total)")

            previous_cuts.append(cut)

        # Count generated dialogues
        dialogue_count = 0
        if dialogue_mode == 'monologue':
            dialogue_count = sum(1 for cut in cuts if cut.monologue_text)
        elif dialogue_mode == 'dialogue':
            dialogue_count = sum(1 for cut in cuts if cut.dialogue_lines)

        print(f"\n✅ Generated {dialogue_count} {dialogue_mode}s")

        return cuts
