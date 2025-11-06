#!/usr/bin/env python3
"""
AI Video Storyboard Generator - Main Script
Complete workflow for generating video storyboards with AI
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
except ImportError:
    pass  # python-dotenv not installed, skip

# Import sub-modules
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("Warning: google-generativeai not installed")
    GEMINI_AVAILABLE = False

from visual_reference_analyzer import VisualReferenceAnalyzer, VisualAnalysis
from music_generator_suno import MusicPromptGenerator


@dataclass
class CutData:
    """Data for a single cut in the storyboard"""
    cut_number: int
    duration: int  # seconds
    scene_description: str
    action: str
    composition: str
    camera_angle: str
    camera_movement: str
    lighting: str
    mood: str
    image_prompt: str
    video_prompt: str
    generated_image_path: Optional[str] = None
    veo3_prompt: Optional[str] = None
    sora2_prompt: Optional[str] = None
    recommended_model: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class StoryboardData:
    """Complete storyboard data"""
    title: str
    duration: int
    num_cuts: int
    cuts: List[CutData]
    style_guide: Dict[str, Any]
    key_visual_analysis: Optional[Dict] = None
    music_sections: Optional[List[Dict]] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'duration': self.duration,
            'num_cuts': self.num_cuts,
            'cuts': [cut.to_dict() for cut in self.cuts],
            'style_guide': self.style_guide,
            'key_visual_analysis': self.key_visual_analysis,
            'music_sections': self.music_sections,
            'created_at': self.created_at
        }


class StoryboardGenerator:
    """Main storyboard generator"""

    # Camera angle selection rules
    SCENE_CAMERA_RULES = {
        'establishing': 'ELS',  # Extreme Long Shot
        'character_intro': 'MS',  # Medium Shot
        'dialogue': 'MS',  # Medium Shot / Medium Close-Up
        'action': 'LS',  # Long Shot
        'emotion': 'CU',  # Close-Up
        'detail': 'ECU',  # Extreme Close-Up
        'conclusion': 'LS'  # Long Shot
    }

    # Composition selection matrix
    COMPOSITION_MATRIX = {
        'opening': 'rule_of_thirds',
        'character': 'centered',
        'dialogue': 'over_shoulder',
        'action': 'diagonal',
        'emotion': 'centered_tight',
        'landscape': 'golden_ratio'
    }

    # Camera movement selection
    MOVEMENT_SELECTION = {
        'opening': 'slow_zoom_in',
        'dialogue': 'static',
        'action': 'tracking',
        'revelation': 'dolly_in',
        'ending': 'slow_pull_back'
    }

    def __init__(self, api_key: Optional[str] = None):
        """Initialize generator with Gemini API (image generation only)"""
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not set. Image generation will be skipped.")

        self.use_gemini = GEMINI_AVAILABLE and self.api_key

        if self.use_gemini:
            # Configure Gemini API for image generation only
            genai.configure(api_key=self.api_key)
            # Only use Gemini for image generation
            self.image_model = "gemini-2.5-flash-image"

    def generate_complete_storyboard(
        self,
        story_description: str,
        key_visual_path: Optional[str] = None,
        config: Optional[Dict] = None
    ) -> StoryboardData:
        """
        Generate complete storyboard from story description

        Args:
            story_description: Story/concept description
            key_visual_path: Optional reference image path
            config: Optional configuration

        Returns:
            Complete StoryboardData
        """
        config = config or {}

        # Step 1: Analyze key visual if provided
        visual_analysis = None
        if key_visual_path:
            print(f"📸 Analyzing key visual: {key_visual_path}")
            analyzer = VisualReferenceAnalyzer(self.api_key)
            visual_analysis = analyzer.analyze_key_visual(key_visual_path)
            print(f"  ✓ Style: {visual_analysis.style}")
            print(f"  ✓ Colors: {', '.join(visual_analysis.colors[:3])}")
            print(f"  ✓ Mood: {visual_analysis.mood}")

        # Step 2: Analyze story and break into cuts
        print("\n📝 Analyzing story structure...")
        cuts_data = self._analyze_story_structure(
            story_description,
            config.get('duration', 60),
            config.get('num_cuts'),
            visual_analysis
        )

        # Step 3: Create detailed cuts
        print(f"\n🎬 Creating {len(cuts_data)} cuts...")
        cuts = []
        for i, cut_info in enumerate(cuts_data):
            cut = self._create_cut(
                i + 1,
                cut_info,
                visual_analysis,
                config
            )
            cuts.append(cut)
            print(f"  ✓ Cut {i + 1}: {cut.scene_description[:50]}...")

        # Step 4: Generate images if API available
        if self.use_gemini and config.get('generate_images', True):
            print("\n🎨 Generating images with Imagen 3...")
            self._generate_images(cuts, config.get('output_dir', 'output'))

        # Step 5: Create storyboard data
        storyboard = StoryboardData(
            title=config.get('title', 'AI Generated Storyboard'),
            duration=config.get('duration', 60),
            num_cuts=len(cuts),
            cuts=cuts,
            style_guide=self._create_style_guide(visual_analysis, config),
            key_visual_analysis=visual_analysis.to_dict() if visual_analysis else None,
            created_at=datetime.now().isoformat()
        )

        # Step 6: Generate music prompts if requested
        if config.get('generate_music', True):
            print("\n🎵 Generating BGM prompts...")
            music_gen = MusicPromptGenerator()
            music_plan = music_gen.generate_complete_music_plan(storyboard.to_dict())
            storyboard.music_sections = music_plan['sections']
            print(f"  ✓ Created {len(music_plan['sections'])} music sections")

        print("\n✅ Storyboard generation complete!")
        return storyboard

    def _analyze_story_structure(
        self,
        story: str,
        duration: int,
        num_cuts: Optional[int],
        visual_analysis: Optional[VisualAnalysis]
    ) -> List[Dict]:
        """Analyze story and create cut structure (now uses Claude via basic structure)"""

        # Always use basic structure (which will be called by Claude in Skills mode)
        # This removes dependency on Gemini text generation API
        return self._basic_story_structure(story, duration, num_cuts)

    def _basic_story_structure(
        self,
        story: str,
        duration: int,
        num_cuts: Optional[int]
    ) -> List[Dict]:
        """Create basic story structure without AI"""

        num_cuts = num_cuts or 8
        cut_duration = duration // num_cuts

        # Basic structure: opening, development, climax, conclusion
        cuts = []

        scene_types = ['opening', 'character', 'dialogue', 'action',
                      'emotion', 'action', 'emotion', 'conclusion']

        for i in range(num_cuts):
            scene_type = scene_types[i] if i < len(scene_types) else 'dialogue'

            cuts.append({
                'duration': cut_duration,
                'scene_description': f"Scene {i+1}",
                'action': f"Action for scene {i+1}",
                'scene_type': scene_type,
                'mood': 'neutral'
            })

        return cuts

    def _create_cut(
        self,
        cut_number: int,
        cut_info: Dict,
        visual_analysis: Optional[VisualAnalysis],
        config: Dict
    ) -> CutData:
        """Create detailed cut with all parameters"""

        scene_type = cut_info.get('scene_type', 'dialogue')

        # Auto-select camera angle
        camera_angle = self.SCENE_CAMERA_RULES.get(scene_type, 'MS')

        # Auto-select composition
        composition = self.COMPOSITION_MATRIX.get(scene_type, 'rule_of_thirds')

        # Auto-select camera movement
        camera_movement = self.MOVEMENT_SELECTION.get(scene_type, 'static')

        # Generate image prompt
        image_prompt = self._generate_image_prompt(
            cut_info,
            camera_angle,
            composition,
            visual_analysis,
            config
        )

        # Generate video prompt
        video_prompt = self._generate_video_prompt(
            cut_info,
            camera_movement,
            cut_info.get('duration', 8)
        )

        return CutData(
            cut_number=cut_number,
            duration=cut_info.get('duration', 8),
            scene_description=cut_info.get('scene_description', ''),
            action=cut_info.get('action', ''),
            composition=composition,
            camera_angle=camera_angle,
            camera_movement=camera_movement,
            lighting=self._determine_lighting(cut_info.get('mood', 'neutral')),
            mood=cut_info.get('mood', 'neutral'),
            image_prompt=image_prompt,
            video_prompt=video_prompt
        )

    def _generate_image_prompt(
        self,
        cut_info: Dict,
        camera_angle: str,
        composition: str,
        visual_analysis: Optional[VisualAnalysis],
        config: Dict
    ) -> str:
        """Generate image generation prompt"""

        # Camera angle descriptions
        angle_desc = {
            'ELS': 'extreme wide shot',
            'LS': 'wide shot',
            'MS': 'medium shot',
            'CU': 'close-up shot',
            'ECU': 'extreme close-up'
        }.get(camera_angle, 'medium shot')

        # Composition descriptions
        comp_desc = composition.replace('_', ' ')

        # Base prompt
        prompt_parts = [
            angle_desc,
            cut_info.get('scene_description', ''),
            cut_info.get('action', ''),
            comp_desc,
            cut_info.get('mood', '') + ' mood'
        ]

        # Add visual style if available
        if visual_analysis:
            prompt_parts.extend([
                visual_analysis.style,
                f"color palette: {', '.join(visual_analysis.colors[:3])}",
                visual_analysis.lighting
            ])
        else:
            # Default style
            style = config.get('visual_style', 'cinematic')
            prompt_parts.append(style)

        # Add technical specs
        prompt_parts.append('16:9')

        return ', '.join(filter(None, prompt_parts))

    def _generate_video_prompt(
        self,
        cut_info: Dict,
        camera_movement: str,
        duration: int
    ) -> str:
        """Generate ItoV prompt for video generation"""

        # Movement descriptions
        movement_desc = {
            'static': 'static camera with slight natural drift',
            'slow_zoom_in': 'slow zoom in, gradually revealing details',
            'slow_pull_back': 'slow pull back, revealing wider context',
            'tracking': 'smooth tracking shot following action',
            'dolly_in': 'dolly forward toward subject',
            'pan': 'smooth pan across scene'
        }.get(camera_movement, 'subtle camera movement')

        prompt = f"""
        {movement_desc},
        {cut_info.get('action', 'natural movement')},
        {duration} seconds,
        {cut_info.get('mood', 'neutral')} atmosphere,
        maintain first frame composition throughout
        """.strip()

        return prompt

    def _determine_lighting(self, mood: str) -> str:
        """Determine lighting based on mood"""

        lighting_map = {
            'hopeful': 'soft morning sunlight',
            'energetic': 'bright dynamic lighting',
            'tense': 'dramatic shadows',
            'peaceful': 'warm golden hour',
            'mysterious': 'low key lighting',
            'joyful': 'bright even lighting',
            'dramatic': 'high contrast lighting'
        }

        return lighting_map.get(mood.lower(), 'natural lighting')

    def _create_style_guide(
        self,
        visual_analysis: Optional[VisualAnalysis],
        config: Dict
    ) -> Dict:
        """Create style guide for storyboard"""

        if visual_analysis:
            return {
                'visual_style': visual_analysis.style,
                'color_palette': visual_analysis.colors,
                'mood': visual_analysis.mood,
                'lighting': visual_analysis.lighting,
                'texture': visual_analysis.texture
            }
        else:
            return {
                'visual_style': config.get('visual_style', 'cinematic'),
                'color_palette': config.get('color_palette', ['#FFE4B5', '#87CEEB']),
                'mood': config.get('mood', 'balanced'),
                'lighting': 'natural',
                'texture': 'medium detail'
            }

    def _generate_images(self, cuts: List[CutData], output_dir: str):
        """Generate images using Gemini 2.5 Flash Image"""

        if not self.use_gemini:
            print("Gemini API not available, skipping image generation")
            return

        # Create output directory
        frames_dir = Path(output_dir) / 'frames'
        frames_dir.mkdir(parents=True, exist_ok=True)

        for cut in cuts:
            try:
                print(f"  Generating image for Cut {cut.cut_number}...")

                # Generate image using Gemini 2.5 Flash Image
                model = genai.GenerativeModel(self.image_model)
                response = model.generate_content(cut.image_prompt)

                # Save image if generated
                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data:
                            image_path = frames_dir / f"cut_{cut.cut_number:02d}.jpg"

                            # Save image data
                            import base64
                            image_data = base64.b64decode(part.inline_data.data)
                            with open(image_path, 'wb') as f:
                                f.write(image_data)

                            cut.generated_image_path = str(image_path)
                            print(f"    ✓ Saved to {image_path}")
                            break

            except Exception as e:
                print(f"    ✗ Error generating image for Cut {cut.cut_number}: {e}")

    def save_storyboard(self, storyboard: StoryboardData, output_dir: str):
        """Save storyboard to JSON"""

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save JSON
        json_path = output_path / 'storyboard.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(storyboard.to_dict(), f, ensure_ascii=False, indent=2)

        print(f"\n💾 Saved storyboard to {json_path}")

        # Create markdown report
        self._create_markdown_report(storyboard, output_path)

    def _create_markdown_report(self, storyboard: StoryboardData, output_dir: Path):
        """Create visual markdown report"""

        report = []
        report.append(f"# {storyboard.title}\n")
        report.append(f"**Duration**: {storyboard.duration}s | **Cuts**: {storyboard.num_cuts}\n")
        report.append(f"**Created**: {storyboard.created_at}\n")

        # Visual style
        if storyboard.key_visual_analysis:
            report.append("\n## 🎨 Visual Style\n")
            va = storyboard.key_visual_analysis
            report.append(f"- **Style**: {va.get('style', 'N/A')}\n")
            report.append(f"- **Colors**: {', '.join(va.get('colors', []))}\n")
            report.append(f"- **Mood**: {va.get('mood', 'N/A')}\n")

        # Cuts
        report.append("\n## 🎬 Storyboard\n")
        for cut in storyboard.cuts:
            report.append(f"\n### Cut {cut.cut_number} ({cut.duration}s)\n")

            if cut.generated_image_path:
                rel_path = Path(cut.generated_image_path).name
                report.append(f"![Cut {cut.cut_number}](frames/{rel_path})\n")

            report.append(f"**Scene**: {cut.scene_description}\n")
            report.append(f"**Action**: {cut.action}\n")
            report.append(f"**Camera**: {cut.camera_angle} | {cut.composition}\n")
            report.append(f"**Movement**: {cut.camera_movement}\n")
            report.append(f"**Mood**: {cut.mood} | {cut.lighting}\n")

            report.append(f"\n**Image Prompt**:\n```\n{cut.image_prompt}\n```\n")
            report.append(f"\n**Video Prompt**:\n```\n{cut.video_prompt}\n```\n")

        # Music sections
        if storyboard.music_sections:
            report.append("\n## 🎵 BGM Structure\n")
            for section in storyboard.music_sections:
                report.append(f"\n### Section {section['section_id']}\n")
                report.append(f"**Cuts**: {section['cuts']} | **Duration**: {section['duration']}\n")
                report.append(f"**Mood**: {section['mood']} | **Energy**: {section['energy']}/10\n")
                report.append(f"**Tempo**: {section['tempo']}\n")
                report.append(f"\n```\n{section['suno_prompt']}\n```\n")

        # Save report
        report_path = output_dir / 'storyboard_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(''.join(report))

        print(f"📄 Saved report to {report_path}")


def create_complete_storyboard(
    story_description: str,
    key_visual_path: Optional[str] = None,
    config: Optional[Dict] = None
) -> StoryboardData:
    """
    Main function to create complete storyboard

    Args:
        story_description: Story/concept description
        key_visual_path: Optional reference image
        config: Optional configuration

    Returns:
        StoryboardData
    """
    generator = StoryboardGenerator()
    return generator.generate_complete_storyboard(
        story_description,
        key_visual_path,
        config
    )


def main():
    """Main CLI entry point"""

    parser = argparse.ArgumentParser(
        description='AI Video Storyboard Generator'
    )
    parser.add_argument('story', help='Story description')
    parser.add_argument('--key-visual', help='Key visual reference image path')
    parser.add_argument('--duration', type=int, default=60, help='Video duration in seconds')
    parser.add_argument('--cuts', type=int, help='Number of cuts (default: auto)')
    parser.add_argument('--output', default='output', help='Output directory')
    parser.add_argument('--title', help='Storyboard title')
    parser.add_argument('--style', help='Visual style (cinematic, anime, etc.)')
    parser.add_argument('--no-images', action='store_true', help='Skip image generation')
    parser.add_argument('--no-music', action='store_true', help='Skip music generation')
    parser.add_argument('--model', choices=['veo3', 'sora2', 'auto'], default='auto',
                       help='Target video model')

    args = parser.parse_args()

    # Build config
    config = {
        'duration': args.duration,
        'num_cuts': args.cuts,
        'output_dir': args.output,
        'title': args.title or 'AI Generated Storyboard',
        'visual_style': args.style,
        'generate_images': not args.no_images,
        'generate_music': not args.no_music,
        'video_model': args.model
    }

    print("="*60)
    print("🎬 AI Video Storyboard Generator")
    print("="*60)
    print(f"\nStory: {args.story}")
    if args.key_visual:
        print(f"Key Visual: {args.key_visual}")
    print(f"Duration: {args.duration}s")
    print(f"Output: {args.output}")
    print()

    # Generate storyboard
    generator = StoryboardGenerator()
    storyboard = generator.generate_complete_storyboard(
        args.story,
        args.key_visual,
        config
    )

    # Save results
    generator.save_storyboard(storyboard, args.output)

    print("\n" + "="*60)
    print("✅ Generation Complete!")
    print("="*60)
    print(f"\nOutput files:")
    print(f"  📄 {args.output}/storyboard.json")
    print(f"  📄 {args.output}/storyboard_report.md")
    if storyboard.music_sections:
        print(f"  🎵 {len(storyboard.music_sections)} music sections generated")
    if any(cut.generated_image_path for cut in storyboard.cuts):
        print(f"  🖼️  {args.output}/frames/ ({storyboard.num_cuts} images)")
    print()


if __name__ == '__main__':
    main()
