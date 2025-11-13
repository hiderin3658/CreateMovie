#!/usr/bin/env python3
"""
Voice Generator using Google Cloud Text-to-Speech API
Generates voice audio for storyboard narration, monologue, and dialogue
"""
import os
from typing import Optional, Dict, List, Any
from pathlib import Path

try:
    from google.cloud import texttospeech
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False


class VoiceGenerator:
    """
    Generate voice audio for storyboard using Google Cloud Text-to-Speech

    Supports 3 dialogue modes:
    - narration: Narrator voiceover
    - monologue: Single character speaking
    - dialogue: Two characters conversing
    """

    # Voice mappings for Japanese (Neural2 voices for best quality)
    VOICE_PROFILES = {
        'narrator_male': {
            'voice_name': 'ja-JP-Neural2-C',
            'gender': texttospeech.SsmlVoiceGender.MALE if GOOGLE_TTS_AVAILABLE else None,
            'pitch': 0.0,
            'speaking_rate': 1.0,
            'description': 'Documentary-style male narrator'
        },
        'narrator_female': {
            'voice_name': 'ja-JP-Neural2-A',
            'gender': texttospeech.SsmlVoiceGender.FEMALE if GOOGLE_TTS_AVAILABLE else None,
            'pitch': 0.0,
            'speaking_rate': 1.0,
            'description': 'Documentary-style female narrator'
        },
        'character_male_young': {
            'voice_name': 'ja-JP-Neural2-D',
            'gender': texttospeech.SsmlVoiceGender.MALE if GOOGLE_TTS_AVAILABLE else None,
            'pitch': 2.0,
            'speaking_rate': 1.1,
            'description': 'Young energetic male'
        },
        'character_male_mature': {
            'voice_name': 'ja-JP-Neural2-C',
            'gender': texttospeech.SsmlVoiceGender.MALE if GOOGLE_TTS_AVAILABLE else None,
            'pitch': -2.0,
            'speaking_rate': 0.95,
            'description': 'Mature calm male'
        },
        'character_female_young': {
            'voice_name': 'ja-JP-Neural2-A',
            'gender': texttospeech.SsmlVoiceGender.FEMALE if GOOGLE_TTS_AVAILABLE else None,
            'pitch': 3.0,
            'speaking_rate': 1.05,
            'description': 'Young cheerful female'
        },
        'character_female_mature': {
            'voice_name': 'ja-JP-Neural2-A',
            'gender': texttospeech.SsmlVoiceGender.FEMALE if GOOGLE_TTS_AVAILABLE else None,
            'pitch': -1.0,
            'speaking_rate': 0.95,
            'description': 'Mature gentle female'
        }
    }

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize voice generator

        Args:
            credentials_path: Path to Google Cloud credentials JSON file
                            (defaults to GOOGLE_APPLICATION_CREDENTIALS env var)
        """
        self.use_google_tts = GOOGLE_TTS_AVAILABLE
        self.client = None

        if not self.use_google_tts:
            print("⚠️  Google Cloud Text-to-Speech not available")
            print("    Install: pip install google-cloud-texttospeech")
            return

        # Set credentials if provided
        if credentials_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

        try:
            self.client = texttospeech.TextToSpeechClient()
            print("✅ Google Cloud Text-to-Speech initialized")
        except Exception as e:
            print(f"⚠️  Failed to initialize Google TTS: {e}")
            self.use_google_tts = False

    def select_voice_profile(
        self,
        dialogue_mode: str,
        character_context: Optional[str] = None,
        mood: Optional[str] = None,
        gender_preference: Optional[str] = None
    ) -> Dict:
        """
        Automatically select appropriate voice profile based on context

        Args:
            dialogue_mode: 'narration', 'monologue', or 'dialogue'
            character_context: Character description (for monologue/dialogue)
            mood: Scene mood (e.g., 'energetic', 'calm', 'sad')
            gender_preference: 'male', 'female', or None (auto-detect)

        Returns:
            Voice profile dict
        """
        # Narration mode - use narrator voice
        if dialogue_mode == 'narration':
            if gender_preference == 'female':
                return self.VOICE_PROFILES['narrator_female'].copy()
            else:
                return self.VOICE_PROFILES['narrator_male'].copy()

        # Detect gender from character context
        gender = gender_preference
        if not gender and character_context:
            context_lower = character_context.lower()
            # Simple keyword detection
            male_keywords = ['男', '男性', 'man', 'male', '彼', 'guy', 'boy']
            female_keywords = ['女', '女性', 'woman', 'female', '彼女', 'girl', 'lady']

            if any(kw in context_lower for kw in male_keywords):
                gender = 'male'
            elif any(kw in context_lower for kw in female_keywords):
                gender = 'female'
            else:
                gender = 'male'  # Default

        if not gender:
            gender = 'male'

        # Detect age/maturity from context
        is_young = False
        if character_context:
            context_lower = character_context.lower()
            young_keywords = ['若', '若い', '10代', '20代', '学生', 'young', 'teen', 'student', '元気', '明るい']
            mature_keywords = ['30代', '40代', '50代', '中年', '大人', 'mature', '落ち着', '真面目']

            if any(kw in context_lower for kw in young_keywords):
                is_young = True
            elif any(kw in context_lower for kw in mature_keywords):
                is_young = False

        # Select base profile
        if gender == 'female':
            profile_key = 'character_female_young' if is_young else 'character_female_mature'
        else:
            profile_key = 'character_male_young' if is_young else 'character_male_mature'

        profile = self.VOICE_PROFILES[profile_key].copy()

        # Adjust speaking rate based on mood
        if mood:
            mood_lower = mood.lower()
            if any(m in mood_lower for m in ['energetic', 'excited', 'happy', '元気', '興奮', '楽しい']):
                profile['speaking_rate'] = min(1.2, profile['speaking_rate'] + 0.1)
            elif any(m in mood_lower for m in ['calm', 'peaceful', 'sad', '静か', '落ち着', '悲しい']):
                profile['speaking_rate'] = max(0.85, profile['speaking_rate'] - 0.1)

        return profile

    def generate_ssml(
        self,
        text: str,
        mood: Optional[str] = None,
        emphasis_words: Optional[List[str]] = None
    ) -> str:
        """
        Generate SSML markup for enhanced speech synthesis

        Args:
            text: Text to convert to SSML
            mood: Scene mood for prosody adjustment
            emphasis_words: Words to emphasize

        Returns:
            SSML string
        """
        # Start SSML
        ssml = '<speak>'

        # Add prosody based on mood
        if mood:
            mood_lower = mood.lower()
            if any(m in mood_lower for m in ['excited', 'happy', '興奮', '楽しい']):
                ssml += '<prosody rate="fast" pitch="+2st">'
            elif any(m in mood_lower for m in ['sad', 'melancholy', '悲しい', '憂鬱']):
                ssml += '<prosody rate="slow" pitch="-2st">'
            elif any(m in mood_lower for m in ['dramatic', 'tense', 'ドラマチック', '緊張']):
                ssml += '<prosody rate="medium" pitch="+1st" volume="loud">'
            else:
                ssml += '<prosody rate="medium">'
        else:
            ssml += '<prosody rate="medium">'

        # Add emphasis to specific words if provided
        if emphasis_words:
            for word in emphasis_words:
                text = text.replace(word, f'<emphasis level="strong">{word}</emphasis>')

        ssml += text
        ssml += '</prosody>'
        ssml += '</speak>'

        return ssml

    def generate_voice(
        self,
        text: str,
        output_path: str,
        voice_profile: Optional[Dict] = None,
        use_ssml: bool = False,
        mood: Optional[str] = None
    ) -> bool:
        """
        Generate voice audio from text

        Args:
            text: Text to synthesize
            output_path: Path to save audio file (MP3)
            voice_profile: Voice profile dict (if None, uses default narrator)
            use_ssml: Whether to use SSML for enhanced synthesis
            mood: Scene mood for SSML generation

        Returns:
            True if successful, False otherwise
        """
        if not self.use_google_tts or not self.client:
            print("⚠️  Google TTS not available")
            return False

        try:
            # Use default narrator voice if none specified
            if not voice_profile:
                voice_profile = self.VOICE_PROFILES['narrator_male']

            # Prepare input
            if use_ssml:
                ssml_text = self.generate_ssml(text, mood)
                synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
            else:
                synthesis_input = texttospeech.SynthesisInput(text=text)

            # Configure voice
            voice = texttospeech.VoiceSelectionParams(
                language_code="ja-JP",
                name=voice_profile['voice_name']
            )

            # Configure audio
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=voice_profile.get('speaking_rate', 1.0),
                pitch=voice_profile.get('pitch', 0.0)
            )

            # Generate speech
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            # Save to file
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'wb') as f:
                f.write(response.audio_content)

            return True

        except Exception as e:
            print(f"❌ Error generating voice: {e}")
            return False

    def generate_voices_for_storyboard(
        self,
        cuts: List[Any],
        output_dir: str,
        character_voices: Optional[Dict[str, Dict]] = None,
        use_ssml: bool = True
    ) -> Dict[str, List[str]]:
        """
        Generate voice audio for entire storyboard

        Args:
            cuts: List of CutData objects
            output_dir: Directory to save audio files
            character_voices: Optional manual voice profile mapping
                             {'character_name': voice_profile_dict}
            use_ssml: Whether to use SSML for enhanced synthesis

        Returns:
            Dict mapping cut numbers to generated audio file paths
            {'narration': [...], 'monologue': [...], 'dialogue': [...]}
        """
        if not self.use_google_tts:
            print("⚠️  Google TTS not available, skipping voice generation")
            return {'narration': [], 'monologue': [], 'dialogue': []}

        print(f"\n🎤 Generating voices for storyboard...")
        print(f"   Output directory: {output_dir}")

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        generated_files = {
            'narration': [],
            'monologue': [],
            'dialogue': []
        }

        for cut in cuts:
            mode = cut.dialogue_mode

            # Mode 1: Narration
            if mode == 'narration' and cut.narration_text:
                print(f"\n  Cut {cut.cut_number} - Narration:")

                voice_profile = self.select_voice_profile(
                    'narration',
                    mood=cut.mood
                )

                filename = f"cut_{cut.cut_number:02d}_narration.mp3"
                output_path = output_dir / filename

                success = self.generate_voice(
                    cut.narration_text,
                    str(output_path),
                    voice_profile,
                    use_ssml=use_ssml,
                    mood=cut.mood
                )

                if success:
                    print(f"    ✓ Generated: {filename}")
                    generated_files['narration'].append(str(output_path))
                else:
                    print(f"    ✗ Failed to generate: {filename}")

            # Mode 2: Monologue
            elif mode == 'monologue' and cut.monologue_text:
                print(f"\n  Cut {cut.cut_number} - Monologue ({cut.monologue_character}):")

                # Use custom voice if provided, otherwise auto-select
                if character_voices and cut.monologue_character in character_voices:
                    voice_profile = character_voices[cut.monologue_character]
                else:
                    # Try to extract character context from somewhere
                    # For now, we'll use the cut's action/scene description as context
                    character_context = f"{cut.scene_description} {cut.action}"
                    voice_profile = self.select_voice_profile(
                        'monologue',
                        character_context=character_context,
                        mood=cut.mood
                    )

                filename = f"cut_{cut.cut_number:02d}_monologue_{cut.monologue_character}.mp3"
                output_path = output_dir / filename

                success = self.generate_voice(
                    cut.monologue_text,
                    str(output_path),
                    voice_profile,
                    use_ssml=use_ssml,
                    mood=cut.mood
                )

                if success:
                    print(f"    ✓ Generated: {filename}")
                    generated_files['monologue'].append(str(output_path))
                else:
                    print(f"    ✗ Failed to generate: {filename}")

            # Mode 3: Dialogue
            elif mode == 'dialogue' and cut.dialogue_lines:
                print(f"\n  Cut {cut.cut_number} - Dialogue ({' & '.join(cut.dialogue_characters)}):")

                for i, line in enumerate(cut.dialogue_lines):
                    speaker = line.speaker

                    # Use custom voice if provided, otherwise auto-select
                    if character_voices and speaker in character_voices:
                        voice_profile = character_voices[speaker]
                    else:
                        character_context = f"{cut.scene_description}"
                        voice_profile = self.select_voice_profile(
                            'dialogue',
                            character_context=character_context,
                            mood=cut.mood
                        )

                    filename = f"cut_{cut.cut_number:02d}_dialogue_{i+1}_{speaker}.mp3"
                    output_path = output_dir / filename

                    success = self.generate_voice(
                        line.text,
                        str(output_path),
                        voice_profile,
                        use_ssml=use_ssml,
                        mood=cut.mood
                    )

                    if success:
                        print(f"    ✓ Generated line {i+1} ({speaker}): {filename}")
                        generated_files['dialogue'].append(str(output_path))
                    else:
                        print(f"    ✗ Failed to generate line {i+1}: {filename}")

        # Summary
        total_files = sum(len(files) for files in generated_files.values())
        print(f"\n✅ Generated {total_files} voice files")
        print(f"   Narration: {len(generated_files['narration'])}")
        print(f"   Monologue: {len(generated_files['monologue'])}")
        print(f"   Dialogue: {len(generated_files['dialogue'])}")

        return generated_files
