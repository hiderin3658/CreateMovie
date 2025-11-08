#!/usr/bin/env python3
"""
Narration Generator
Generates contextual narration text for video storyboard cuts using Claude API
"""
import os
from typing import List, Optional, Dict, Any

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class NarrationGenerator:
    """Generate contextual narration text for video storyboard cuts"""

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
