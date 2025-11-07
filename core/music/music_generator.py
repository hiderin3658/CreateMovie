#!/usr/bin/env python3
"""
Music Generator
Core music generation functionality
"""
from typing import Dict, List, Optional
from enum import Enum


class MoodType(Enum):
    """Emotional mood categories"""
    PEACEFUL = "peaceful"
    HOPEFUL = "hopeful"
    ENERGETIC = "energetic"
    TENSE = "tense"
    DRAMATIC = "dramatic"
    MYSTERIOUS = "mysterious"
    JOYFUL = "joyful"
    MELANCHOLIC = "melancholic"
    TRIUMPHANT = "triumphant"
    ROMANTIC = "romantic"
    NEUTRAL = "neutral"


class MusicGenerator:
    """Generate music prompts for video storyboards"""

    MOOD_MUSIC_MAP = {
        MoodType.PEACEFUL: {
            'tempo_range': (60, 80),
            'energy': (2, 4),
            'descriptors': ['calm', 'serene', 'tranquil', 'gentle']
        },
        MoodType.HOPEFUL: {
            'tempo_range': (70, 100),
            'energy': (4, 6),
            'descriptors': ['uplifting', 'optimistic', 'bright', 'inspiring']
        },
        MoodType.ENERGETIC: {
            'tempo_range': (120, 140),
            'energy': (7, 9),
            'descriptors': ['dynamic', 'vibrant', 'exciting', 'powerful']
        },
        MoodType.NEUTRAL: {
            'tempo_range': (90, 110),
            'energy': (5, 6),
            'descriptors': ['balanced', 'moderate', 'steady']
        }
    }

    def __init__(self):
        """Initialize music generator"""
        pass

    def generate_music_plan(self, storyboard: Dict) -> Dict:
        """
        Generate music plan for storyboard

        Args:
            storyboard: Storyboard data

        Returns:
            Music plan with sections
        """
        cuts = storyboard.get('cuts', [])

        sections = []
        section_id = 1

        for i, cut in enumerate(cuts):
            mood = self._detect_cut_mood(cut)
            music_data = self.MOOD_MUSIC_MAP.get(
                mood,
                self.MOOD_MUSIC_MAP[MoodType.NEUTRAL]
            )

            section = {
                'section_id': section_id,
                'cuts': f"{i+1}",
                'duration': cut.get('duration', 8),
                'mood': mood.value,
                'energy': music_data['energy'][0],
                'tempo': music_data['tempo_range'][0],
                'suno_prompt': self._create_suno_prompt(mood, music_data)
            }

            sections.append(section)
            section_id += 1

        return {
            'total_duration': storyboard.get('duration', 60),
            'num_sections': len(sections),
            'sections': sections
        }

    def _detect_cut_mood(self, cut: Dict) -> MoodType:
        """Detect mood from cut data"""
        mood_str = cut.get('mood', 'neutral').lower()

        for mood_type in MoodType:
            if mood_type.value == mood_str:
                return mood_type

        return MoodType.NEUTRAL

    def _create_suno_prompt(self, mood: MoodType, music_data: Dict) -> str:
        """Create Suno prompt"""
        descriptors = ', '.join(music_data['descriptors'])
        tempo = music_data['tempo_range'][0]

        return f"{descriptors}, {tempo} BPM, {mood.value} mood"
