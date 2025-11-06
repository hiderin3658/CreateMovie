#!/usr/bin/env python3
"""
Music Prompt Generator for Suno
Generates optimized BGM prompts based on storyboard emotional arc
"""

import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
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


class MusicGenre(Enum):
    """Music genre categories for Suno"""
    ORCHESTRAL = "Orchestral"
    CINEMATIC = "Cinematic"
    POP = "Pop"
    ROCK = "Rock"
    ELECTRONIC = "Electronic"
    JAZZ = "Jazz"
    CLASSICAL = "Classical"
    AMBIENT = "Ambient"
    HYBRID = "Hybrid"
    WORLD = "World"


@dataclass
class MusicSection:
    """Music section for a group of cuts"""
    section_id: int
    cut_range: Tuple[int, int]  # (start_cut, end_cut)
    duration: int  # seconds
    mood: MoodType
    energy_level: int  # 1-10
    genre: MusicGenre
    tempo: int  # BPM
    instruments: List[str]
    description: str
    suno_prompt: str
    transition_type: Optional[str] = None  # How it connects to next section


class MusicPromptGenerator:
    """Generate Suno-optimized music prompts for video storyboards"""
    
    # Mood to music mapping
    MOOD_MUSIC_MAP = {
        MoodType.PEACEFUL: {
            'genres': [MusicGenre.AMBIENT, MusicGenre.CLASSICAL],
            'tempo_range': (60, 80),
            'energy': (2, 4),
            'instruments': ['piano', 'strings', 'flute', 'harp'],
            'descriptors': ['calm', 'serene', 'tranquil', 'gentle']
        },
        MoodType.HOPEFUL: {
            'genres': [MusicGenre.ORCHESTRAL, MusicGenre.POP],
            'tempo_range': (70, 100),
            'energy': (4, 6),
            'instruments': ['piano', 'strings', 'acoustic guitar', 'light percussion'],
            'descriptors': ['uplifting', 'optimistic', 'bright', 'inspiring']
        },
        MoodType.ENERGETIC: {
            'genres': [MusicGenre.POP, MusicGenre.ROCK, MusicGenre.ELECTRONIC],
            'tempo_range': (120, 140),
            'energy': (7, 9),
            'instruments': ['drums', 'electric guitar', 'bass', 'synth'],
            'descriptors': ['dynamic', 'vibrant', 'exciting', 'powerful']
        },
        MoodType.TENSE: {
            'genres': [MusicGenre.CINEMATIC, MusicGenre.HYBRID],
            'tempo_range': (80, 110),
            'energy': (5, 7),
            'instruments': ['strings staccato', 'percussion', 'brass', 'synth bass'],
            'descriptors': ['suspenseful', 'anxious', 'building', 'uncertain']
        },
        MoodType.DRAMATIC: {
            'genres': [MusicGenre.ORCHESTRAL, MusicGenre.CINEMATIC],
            'tempo_range': (70, 100),
            'energy': (7, 9),
            'instruments': ['full orchestra', 'brass', 'timpani', 'choir'],
            'descriptors': ['epic', 'intense', 'powerful', 'grand']
        },
        MoodType.MYSTERIOUS: {
            'genres': [MusicGenre.AMBIENT, MusicGenre.CINEMATIC],
            'tempo_range': (60, 90),
            'energy': (3, 5),
            'instruments': ['synth pads', 'strings', 'celesta', 'theremin'],
            'descriptors': ['enigmatic', 'ethereal', 'haunting', 'atmospheric']
        },
        MoodType.JOYFUL: {
            'genres': [MusicGenre.POP, MusicGenre.JAZZ],
            'tempo_range': (110, 130),
            'energy': (7, 9),
            'instruments': ['ukulele', 'piano', 'brass section', 'drums'],
            'descriptors': ['happy', 'cheerful', 'playful', 'celebratory']
        },
        MoodType.MELANCHOLIC: {
            'genres': [MusicGenre.CLASSICAL, MusicGenre.AMBIENT],
            'tempo_range': (60, 80),
            'energy': (2, 4),
            'instruments': ['solo piano', 'cello', 'violin', 'oboe'],
            'descriptors': ['sad', 'reflective', 'nostalgic', 'emotional']
        },
        MoodType.TRIUMPHANT: {
            'genres': [MusicGenre.ORCHESTRAL, MusicGenre.HYBRID],
            'tempo_range': (90, 120),
            'energy': (8, 10),
            'instruments': ['full orchestra', 'brass fanfare', 'drums', 'choir'],
            'descriptors': ['victorious', 'heroic', 'majestic', 'glorious']
        },
        MoodType.ROMANTIC: {
            'genres': [MusicGenre.CLASSICAL, MusicGenre.JAZZ],
            'tempo_range': (60, 90),
            'energy': (3, 5),
            'instruments': ['strings', 'piano', 'saxophone', 'harp'],
            'descriptors': ['tender', 'intimate', 'warm', 'passionate']
        }
    }
    
    def __init__(self):
        """Initialize music prompt generator"""
        pass
    
    def analyze_emotional_arc(self, storyboard: Dict) -> Dict[str, Any]:
        """
        Analyze the emotional arc of the storyboard
        
        Args:
            storyboard: Storyboard data with cuts
            
        Returns:
            Emotional arc analysis
        """
        cuts = storyboard.get('cuts', [])
        
        # Extract moods from each cut
        moods = []
        for cut in cuts:
            mood = self._detect_cut_mood(cut)
            moods.append(mood)
        
        # Identify arc pattern
        arc_type = self._identify_arc_type(moods)
        
        # Find emotional peaks and valleys
        peak_points = self._find_emotional_peaks(moods)
        
        # Identify mood transitions
        transitions = self._identify_transitions(moods)
        
        return {
            'arc_type': arc_type,
            'moods': moods,
            'peak_points': peak_points,
            'transitions': transitions,
            'overall_journey': self._describe_journey(moods)
        }
    
    def divide_music_sections(
        self,
        storyboard: Dict,
        emotional_arc: Dict
    ) -> List[Dict]:
        """
        Divide the storyboard into music sections
        
        Args:
            storyboard: Storyboard data
            emotional_arc: Emotional arc analysis
            
        Returns:
            List of music sections
        """
        cuts = storyboard.get('cuts', [])
        moods = emotional_arc['moods']
        transitions = emotional_arc['transitions']
        
        sections = []
        current_section_start = 0
        
        for i, transition in enumerate(transitions):
            if transition['significant']:
                # Create section from current_start to transition point
                section = {
                    'start_cut': current_section_start + 1,
                    'end_cut': transition['cut_index'] + 1,
                    'cuts': list(range(current_section_start + 1, transition['cut_index'] + 2)),
                    'dominant_mood': self._get_dominant_mood(
                        moods[current_section_start:transition['cut_index'] + 1]
                    )
                }
                sections.append(section)
                current_section_start = transition['cut_index'] + 1
        
        # Add final section
        if current_section_start < len(cuts):
            section = {
                'start_cut': current_section_start + 1,
                'end_cut': len(cuts),
                'cuts': list(range(current_section_start + 1, len(cuts) + 1)),
                'dominant_mood': self._get_dominant_mood(moods[current_section_start:])
            }
            sections.append(section)
        
        # If no significant transitions, create 3 sections
        if len(sections) <= 1:
            sections = self._create_default_sections(cuts, moods)
        
        # Add duration to each section
        for section in sections:
            section['duration'] = self._calculate_section_duration(
                cuts[section['start_cut']-1:section['end_cut']]
            )
        
        return sections
    
    def generate_suno_prompts(
        self,
        sections: List[Dict],
        storyboard: Dict
    ) -> List[MusicSection]:
        """
        Generate Suno-optimized prompts for each section
        
        Args:
            sections: Music sections
            storyboard: Storyboard data
            
        Returns:
            List of MusicSection objects with Suno prompts
        """
        music_sections = []
        
        for i, section in enumerate(sections):
            # Determine music parameters
            mood = section['dominant_mood']
            music_params = self.MOOD_MUSIC_MAP.get(mood, self.MOOD_MUSIC_MAP[MoodType.PEACEFUL])
            
            # Select genre
            genre = self._select_genre(section, storyboard)
            
            # Calculate tempo
            tempo = self._calculate_tempo(section, music_params['tempo_range'])
            
            # Select instruments
            instruments = self._select_instruments(section, music_params['instruments'])
            
            # Determine energy level
            energy = self._calculate_energy(section, music_params['energy'])
            
            # Generate description
            description = self._generate_section_description(i, len(sections), section)
            
            # Build Suno prompt
            suno_prompt = self._build_suno_prompt(
                genre=genre,
                tempo=tempo,
                mood=mood,
                instruments=instruments,
                energy=energy,
                descriptors=music_params['descriptors'],
                section_position=i,
                total_sections=len(sections)
            )
            
            # Create MusicSection object
            music_section = MusicSection(
                section_id=i + 1,
                cut_range=(section['start_cut'], section['end_cut']),
                duration=section['duration'],
                mood=mood,
                energy_level=energy,
                genre=genre,
                tempo=tempo,
                instruments=instruments,
                description=description,
                suno_prompt=suno_prompt,
                transition_type=self._get_transition_type(i, len(sections))
            )
            
            music_sections.append(music_section)
        
        return music_sections
    
    def _detect_cut_mood(self, cut: Dict) -> MoodType:
        """Detect mood from cut description"""
        description = cut.get('scene_description', '').lower()
        mood_str = cut.get('mood', '').lower()
        combined = f"{description} {mood_str}"
        
        # Keywords for each mood
        mood_keywords = {
            MoodType.PEACEFUL: ['calm', 'quiet', 'serene', 'tranquil', 'morning'],
            MoodType.HOPEFUL: ['hope', 'optimistic', 'bright', 'beginning', 'sunrise'],
            MoodType.ENERGETIC: ['active', 'busy', 'dynamic', 'running', 'excitement'],
            MoodType.TENSE: ['nervous', 'anxious', 'worried', 'problem', 'conflict'],
            MoodType.DRAMATIC: ['intense', 'powerful', 'critical', 'climax'],
            MoodType.MYSTERIOUS: ['unknown', 'strange', 'curious', 'mystery'],
            MoodType.JOYFUL: ['happy', 'celebration', 'fun', 'laughing', 'party'],
            MoodType.MELANCHOLIC: ['sad', 'lonely', 'loss', 'goodbye'],
            MoodType.TRIUMPHANT: ['victory', 'success', 'achievement', 'win'],
            MoodType.ROMANTIC: ['love', 'intimate', 'tender', 'couple']
        }
        
        # Score each mood
        scores = {}
        for mood, keywords in mood_keywords.items():
            score = sum(1 for keyword in keywords if keyword in combined)
            if score > 0:
                scores[mood] = score
        
        # Return mood with highest score, default to PEACEFUL
        if scores:
            return max(scores, key=scores.get)
        return MoodType.PEACEFUL
    
    def _identify_arc_type(self, moods: List[MoodType]) -> str:
        """Identify the type of emotional arc"""
        
        # Map moods to energy levels
        energy_levels = [self._mood_to_energy(mood) for mood in moods]
        
        # Analyze trend
        if len(energy_levels) < 2:
            return "static"
        
        first_third = sum(energy_levels[:len(energy_levels)//3]) / max(len(energy_levels)//3, 1)
        last_third = sum(energy_levels[-len(energy_levels)//3:]) / max(len(energy_levels)//3, 1)
        
        if last_third > first_third + 2:
            return "rising"
        elif first_third > last_third + 2:
            return "falling"
        elif max(energy_levels) - min(energy_levels) > 4:
            return "wave"
        else:
            return "steady"
    
    def _mood_to_energy(self, mood: MoodType) -> int:
        """Convert mood to energy level"""
        energy_map = {
            MoodType.PEACEFUL: 3,
            MoodType.HOPEFUL: 5,
            MoodType.ENERGETIC: 8,
            MoodType.TENSE: 6,
            MoodType.DRAMATIC: 8,
            MoodType.MYSTERIOUS: 4,
            MoodType.JOYFUL: 9,
            MoodType.MELANCHOLIC: 2,
            MoodType.TRIUMPHANT: 10,
            MoodType.ROMANTIC: 4
        }
        return energy_map.get(mood, 5)
    
    def _find_emotional_peaks(self, moods: List[MoodType]) -> List[int]:
        """Find emotional peak points in the arc"""
        energy_levels = [self._mood_to_energy(mood) for mood in moods]
        
        peaks = []
        for i in range(1, len(energy_levels) - 1):
            if (energy_levels[i] > energy_levels[i-1] and 
                energy_levels[i] > energy_levels[i+1]):
                peaks.append(i)
        
        # Always include climax if it exists
        if energy_levels:
            max_energy_idx = energy_levels.index(max(energy_levels))
            if max_energy_idx not in peaks:
                peaks.append(max_energy_idx)
        
        return sorted(peaks)
    
    def _identify_transitions(self, moods: List[MoodType]) -> List[Dict]:
        """Identify mood transitions between cuts"""
        transitions = []
        
        for i in range(len(moods) - 1):
            current = moods[i]
            next_mood = moods[i + 1]
            
            if current != next_mood:
                energy_change = abs(
                    self._mood_to_energy(next_mood) - 
                    self._mood_to_energy(current)
                )
                
                transitions.append({
                    'cut_index': i,
                    'from_mood': current,
                    'to_mood': next_mood,
                    'energy_change': energy_change,
                    'significant': energy_change >= 3
                })
        
        return transitions
    
    def _describe_journey(self, moods: List[MoodType]) -> str:
        """Describe the emotional journey"""
        if not moods:
            return "neutral journey"
        
        start_mood = moods[0]
        end_mood = moods[-1]
        
        if len(moods) > 2:
            middle_moods = moods[1:-1]
            dominant_middle = max(set(middle_moods), key=middle_moods.count)
            
            return (f"Journey from {start_mood.value} through "
                   f"{dominant_middle.value} to {end_mood.value}")
        else:
            return f"Journey from {start_mood.value} to {end_mood.value}"
    
    def _get_dominant_mood(self, moods: List[MoodType]) -> MoodType:
        """Get the dominant mood from a list"""
        if not moods:
            return MoodType.PEACEFUL
        
        return max(set(moods), key=moods.count)
    
    def _create_default_sections(
        self,
        cuts: List[Dict],
        moods: List[MoodType]
    ) -> List[Dict]:
        """Create default 3-section structure"""
        total_cuts = len(cuts)
        
        # Intro: First 30%
        intro_end = max(1, total_cuts // 3)
        
        # Main: Middle 40%
        main_end = max(intro_end + 1, 2 * total_cuts // 3)
        
        sections = [
            {
                'start_cut': 1,
                'end_cut': intro_end,
                'cuts': list(range(1, intro_end + 1)),
                'dominant_mood': self._get_dominant_mood(moods[:intro_end])
            },
            {
                'start_cut': intro_end + 1,
                'end_cut': main_end,
                'cuts': list(range(intro_end + 1, main_end + 1)),
                'dominant_mood': self._get_dominant_mood(moods[intro_end:main_end])
            },
            {
                'start_cut': main_end + 1,
                'end_cut': total_cuts,
                'cuts': list(range(main_end + 1, total_cuts + 1)),
                'dominant_mood': self._get_dominant_mood(moods[main_end:])
            }
        ]
        
        return sections
    
    def _calculate_section_duration(self, cuts: List[Dict]) -> int:
        """Calculate total duration for section cuts"""
        return sum(cut.get('duration', 10) for cut in cuts)
    
    def _select_genre(self, section: Dict, storyboard: Dict) -> MusicGenre:
        """Select appropriate genre for section"""
        mood = section['dominant_mood']
        style = storyboard.get('style_guide', {}).get('visual_style', '')
        
        # Get suggested genres for mood
        mood_params = self.MOOD_MUSIC_MAP.get(mood, {})
        suggested_genres = mood_params.get('genres', [MusicGenre.CINEMATIC])

        # Adjust based on visual style
        if style and 'anime' in style.lower():
            if MusicGenre.POP in suggested_genres:
                return MusicGenre.POP
            return MusicGenre.ORCHESTRAL
        elif style and 'realistic' in style.lower():
            return MusicGenre.CINEMATIC

        return suggested_genres[0] if suggested_genres else MusicGenre.CINEMATIC
    
    def _calculate_tempo(self, section: Dict, tempo_range: Tuple[int, int]) -> int:
        """Calculate appropriate tempo for section"""
        # Start with middle of range
        min_tempo, max_tempo = tempo_range
        base_tempo = (min_tempo + max_tempo) // 2
        
        # Adjust based on section position (slower intro, faster middle)
        if section['start_cut'] == 1:  # Intro
            return min_tempo + 10
        elif section['end_cut'] == section.get('total_cuts', 10):  # Outro
            return min_tempo + 5
        else:  # Middle sections
            return base_tempo + 10
    
    def _select_instruments(
        self,
        section: Dict,
        suggested_instruments: List[str]
    ) -> List[str]:
        """Select instruments for section"""
        # Start with suggested instruments
        instruments = suggested_instruments[:3]  # Limit to 3 main instruments
        
        # Add section-specific instruments
        if section['start_cut'] == 1:
            # Intro: Start simple
            return instruments[:2]
        elif section.get('is_climax', False):
            # Climax: Full arrangement
            instruments.append('full ensemble')
        
        return instruments
    
    def _calculate_energy(
        self,
        section: Dict,
        energy_range: Tuple[int, int]
    ) -> int:
        """Calculate energy level for section"""
        min_energy, max_energy = energy_range
        
        # Base energy on mood
        mood = section['dominant_mood']
        base_energy = self._mood_to_energy(mood)
        
        # Clamp to range
        return max(min_energy, min(max_energy, base_energy))
    
    def _generate_section_description(
        self,
        section_index: int,
        total_sections: int,
        section: Dict
    ) -> str:
        """Generate human-readable section description"""
        
        position = ""
        if section_index == 0:
            position = "Opening"
        elif section_index == total_sections - 1:
            position = "Finale"
        else:
            position = f"Development {section_index}"
        
        mood = section['dominant_mood'].value
        
        return f"{position} - {mood.capitalize()} section"
    
    def _build_suno_prompt(
        self,
        genre: MusicGenre,
        tempo: int,
        mood: MoodType,
        instruments: List[str],
        energy: int,
        descriptors: List[str],
        section_position: int,
        total_sections: int
    ) -> str:
        """Build Suno-optimized prompt"""
        
        # Position descriptor
        if section_position == 0:
            position = "intro"
        elif section_position == total_sections - 1:
            position = "finale"
        else:
            position = "main"
        
        # Energy descriptor
        if energy <= 3:
            energy_desc = "soft"
        elif energy <= 6:
            energy_desc = "moderate"
        elif energy <= 8:
            energy_desc = "energetic"
        else:
            energy_desc = "powerful"
        
        # Build prompt
        prompt_parts = [
            f"[{genre.value} {position.capitalize()}]",
            f"{tempo}bpm",
            f"{energy_desc}",
            f"{', '.join(descriptors[:2])}",
            f"{', '.join(instruments)}"
        ]
        
        # Add mood-specific elements
        if mood == MoodType.TRIUMPHANT:
            prompt_parts.append("building to climax")
        elif mood == MoodType.PEACEFUL:
            prompt_parts.append("gentle flow")
        elif mood == MoodType.ENERGETIC:
            prompt_parts.append("driving rhythm")
        
        return ", ".join(prompt_parts)
    
    def _get_transition_type(self, section_index: int, total_sections: int) -> Optional[str]:
        """Determine transition type to next section"""
        if section_index >= total_sections - 1:
            return None  # Last section
        
        if section_index == 0:
            return "build"
        elif section_index == total_sections - 2:
            return "resolve"
        else:
            return "flow"
    
    def generate_complete_music_plan(
        self,
        storyboard: Dict
    ) -> Dict[str, Any]:
        """
        Generate complete music plan for storyboard
        
        Args:
            storyboard: Complete storyboard data
            
        Returns:
            Complete music plan with sections and prompts
        """
        # Analyze emotional arc
        emotional_arc = self.analyze_emotional_arc(storyboard)
        
        # Divide into sections
        sections = self.divide_music_sections(storyboard, emotional_arc)
        
        # Add total cuts info
        for section in sections:
            section['total_cuts'] = len(storyboard.get('cuts', []))
        
        # Generate Suno prompts
        music_sections = self.generate_suno_prompts(sections, storyboard)
        
        # Create complete plan
        music_plan = {
            'emotional_arc': emotional_arc,
            'sections': [
                {
                    'section_id': ms.section_id,
                    'cuts': f"{ms.cut_range[0]}-{ms.cut_range[1]}",
                    'duration': f"{ms.duration}s",
                    'description': ms.description,
                    'mood': ms.mood.value,
                    'energy': ms.energy_level,
                    'tempo': f"{ms.tempo}bpm",
                    'genre': ms.genre.value,
                    'instruments': ms.instruments,
                    'suno_prompt': ms.suno_prompt,
                    'transition': ms.transition_type
                }
                for ms in music_sections
            ],
            'total_duration': sum(ms.duration for ms in music_sections),
            'sync_points': self._identify_sync_points(storyboard, music_sections)
        }
        
        return music_plan
    
    def _identify_sync_points(
        self,
        storyboard: Dict,
        music_sections: List[MusicSection]
    ) -> List[Dict]:
        """Identify key sync points between video and music"""
        sync_points = []
        
        cuts = storyboard.get('cuts', [])
        
        for i, cut in enumerate(cuts):
            # Check for key moments
            if any(word in cut.get('action', '').lower() 
                   for word in ['reveal', 'explosion', 'jump', 'impact']):
                
                # Find which music section this belongs to
                section = None
                for ms in music_sections:
                    if ms.cut_range[0] <= i + 1 <= ms.cut_range[1]:
                        section = ms
                        break
                
                if section:
                    sync_points.append({
                        'cut': i + 1,
                        'time': sum(c.get('duration', 10) for c in cuts[:i]),
                        'action': cut.get('action', ''),
                        'music_cue': 'accent' if section.energy_level > 6 else 'soft hit',
                        'section': section.section_id
                    })
        
        return sync_points
    
    def save_music_plan(self, music_plan: Dict, output_path: str):
        """Save music plan to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(music_plan, f, ensure_ascii=False, indent=2)
    
    def create_suno_batch_file(
        self,
        music_plan: Dict,
        output_path: str
    ):
        """Create a batch file with all Suno prompts"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Suno BGM Prompts\n\n")
            f.write(f"Total Duration: {music_plan['total_duration']}s\n")
            f.write(f"Emotional Arc: {music_plan['emotional_arc']['overall_journey']}\n\n")
            
            for section in music_plan['sections']:
                f.write(f"## Section {section['section_id']} (Cuts {section['cuts']})\n")
                f.write(f"Duration: {section['duration']}\n")
                f.write(f"Description: {section['description']}\n")
                f.write(f"Energy: {section['energy']}/10\n")
                f.write(f"Tempo: {section['tempo']}\n\n")
                f.write("```\n")
                f.write(section['suno_prompt'])
                f.write("\n```\n\n")
                f.write("---\n\n")


# Example usage
if __name__ == "__main__":
    # Example storyboard
    sample_storyboard = {
        "title": "School Festival Story",
        "duration": 60,
        "cuts": [
            {
                "cut_number": 1,
                "duration": 10,
                "scene_description": "Morning classroom preparation",
                "mood": "hopeful"
            },
            {
                "cut_number": 2,
                "duration": 8,
                "scene_description": "Students working together",
                "mood": "energetic"
            },
            {
                "cut_number": 3,
                "duration": 7,
                "scene_description": "Friends discussing plans",
                "mood": "cheerful"
            },
            {
                "cut_number": 4,
                "duration": 8,
                "scene_description": "Problem arises",
                "mood": "tense"
            },
            {
                "cut_number": 5,
                "duration": 7,
                "scene_description": "Working to solve issue",
                "mood": "determined"
            },
            {
                "cut_number": 6,
                "duration": 8,
                "scene_description": "Breakthrough moment",
                "mood": "hopeful"
            },
            {
                "cut_number": 7,
                "duration": 7,
                "scene_description": "Final preparation complete",
                "mood": "triumphant"
            },
            {
                "cut_number": 8,
                "duration": 5,
                "scene_description": "Celebration together",
                "mood": "joyful"
            }
        ],
        "style_guide": {
            "visual_style": "anime"
        }
    }
    
    # Generate music plan
    generator = MusicPromptGenerator()
    music_plan = generator.generate_complete_music_plan(sample_storyboard)
    
    # Print results
    print("=== Music Generation Plan ===")
    print(f"Emotional Arc: {music_plan['emotional_arc']['arc_type']}")
    print(f"Journey: {music_plan['emotional_arc']['overall_journey']}")
    print(f"Total Duration: {music_plan['total_duration']}s")
    print()
    
    for section in music_plan['sections']:
        print(f"Section {section['section_id']} (Cuts {section['cuts']})")
        print(f"  Duration: {section['duration']}")
        print(f"  Mood: {section['mood']}")
        print(f"  Energy: {section['energy']}/10")
        print(f"  Tempo: {section['tempo']}")
        print(f"  Genre: {section['genre']}")
        print(f"  Suno Prompt: {section['suno_prompt'][:50]}...")
        print()
    
    # Save to files
    generator.save_music_plan(music_plan, "music_plan.json")
    generator.create_suno_batch_file(music_plan, "suno_prompts.md")
    print("✅ Music plan saved to music_plan.json")
    print("✅ Suno prompts saved to suno_prompts.md")
