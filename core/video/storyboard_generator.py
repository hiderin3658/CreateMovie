#!/usr/bin/env python3
"""
Core Storyboard Generator
Modularized storyboard generation functionality
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from ..base import BaseVideoGenerator, GeneratorConfig


@dataclass
class CutData:
    """Data for a single cut in the storyboard"""
    cut_number: int
    duration: int
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
    # Narration fields
    narration_text: Optional[str] = None
    narration_needed: bool = False
    narration_duration: Optional[float] = None
    narration_timing: Optional[str] = None
    narration_style: Optional[str] = None

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


class CoreStoryboardGenerator(BaseVideoGenerator):
    """Core storyboard generator with modular architecture"""

    # Camera angle selection rules
    SCENE_CAMERA_RULES = {
        'establishing': 'ELS',
        'character_intro': 'MS',
        'dialogue': 'MS',
        'action': 'LS',
        'emotion': 'CU',
        'detail': 'ECU',
        'conclusion': 'LS',
        'opening': 'LS',
        'character': 'MS'
    }

    # Composition selection matrix
    COMPOSITION_MATRIX = {
        'opening': 'rule_of_thirds',
        'character': 'centered',
        'dialogue': 'over_shoulder',
        'action': 'diagonal',
        'emotion': 'centered_tight',
        'landscape': 'golden_ratio',
        'establishing': 'rule_of_thirds',
        'conclusion': 'centered'
    }

    # Camera movement selection
    MOVEMENT_SELECTION = {
        'opening': 'slow_zoom_in',
        'dialogue': 'static',
        'action': 'tracking',
        'revelation': 'dolly_in',
        'ending': 'slow_pull_back',
        'establishing': 'slow_pan',
        'character': 'static',
        'emotion': 'slow_zoom_in',
        'conclusion': 'slow_pull_back'
    }

    def __init__(self, config: Optional[GeneratorConfig] = None):
        """
        Initialize core storyboard generator

        Args:
            config: Generator configuration
        """
        super().__init__(config)

    def generate_storyboard(self, input_data: Dict) -> StoryboardData:
        """
        Generate complete storyboard

        Args:
            input_data: Input data containing story description and optional key visual

        Returns:
            Complete storyboard data
        """
        story_description = input_data.get('story_description', '')
        visual_analysis = input_data.get('visual_analysis')

        # Trigger pre-generation hooks
        input_data = self.trigger_hook('pre_generation', input_data)

        # Step 1: Analyze story structure
        print("\n📝 Analyzing story structure...")
        cuts_data = self._analyze_story_structure(
            story_description,
            self.config.duration,
            self.config.num_cuts,
            visual_analysis
        )

        # Step 2: Create detailed cuts
        print(f"\n🎬 Creating {len(cuts_data)} cuts...")
        cuts = []
        for i, cut_info in enumerate(cuts_data):
            cut = self._create_cut(
                i + 1,
                cut_info,
                visual_analysis
            )
            cuts.append(cut)
            print(f"  ✓ Cut {i + 1}: {cut.scene_description[:50]}...")

        # Step 3: Create storyboard data
        storyboard = StoryboardData(
            title=self.config.title,
            duration=self.config.duration,
            num_cuts=len(cuts),
            cuts=cuts,
            style_guide=self._create_style_guide(visual_analysis),
            key_visual_analysis=visual_analysis,
            created_at=datetime.now().isoformat()
        )

        # Trigger post-generation hooks
        storyboard_dict = storyboard.to_dict()
        storyboard_dict = self.trigger_hook('post_generation', storyboard_dict)

        print("\n✅ Storyboard generation complete!")
        return storyboard

    def _analyze_story_structure(
        self,
        story: str,
        duration: int,
        num_cuts: Optional[int],
        visual_analysis: Optional[Dict]
    ) -> List[Dict]:
        """
        Analyze story and create cut structure

        Args:
            story: Story description
            duration: Total duration
            num_cuts: Number of cuts (optional)
            visual_analysis: Visual analysis data

        Returns:
            List of cut information dictionaries
        """
        return self._basic_story_structure(story, duration, num_cuts)

    def _basic_story_structure(
        self,
        story: str,
        duration: int,
        num_cuts: Optional[int]
    ) -> List[Dict]:
        """Create basic story structure"""
        num_cuts = num_cuts or 8
        cut_duration = duration // num_cuts

        scene_types = ['opening', 'character', 'dialogue', 'action',
                      'emotion', 'action', 'emotion', 'conclusion']

        cuts = []
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
        visual_analysis: Optional[Dict]
    ) -> CutData:
        """Create detailed cut with all parameters"""
        scene_type = cut_info.get('scene_type', 'dialogue')

        camera_angle = self.SCENE_CAMERA_RULES.get(scene_type, 'MS')
        composition = self.COMPOSITION_MATRIX.get(scene_type, 'rule_of_thirds')
        camera_movement = self.MOVEMENT_SELECTION.get(scene_type, 'static')

        image_prompt = self._generate_image_prompt(
            cut_info,
            camera_angle,
            composition,
            visual_analysis
        )

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
        visual_analysis: Optional[Dict]
    ) -> str:
        """Generate image generation prompt"""
        angle_desc = {
            'ELS': 'extreme wide shot',
            'LS': 'wide shot',
            'MS': 'medium shot',
            'CU': 'close-up shot',
            'ECU': 'extreme close-up'
        }.get(camera_angle, 'medium shot')

        comp_desc = composition.replace('_', ' ')

        prompt_parts = [
            angle_desc,
            cut_info.get('scene_description', ''),
            cut_info.get('action', ''),
            comp_desc,
            cut_info.get('mood', '') + ' mood'
        ]

        if visual_analysis:
            prompt_parts.extend([
                visual_analysis.get('style', ''),
                f"color palette: {', '.join(visual_analysis.get('colors', [])[:3])}",
                visual_analysis.get('lighting', '')
            ])
        else:
            prompt_parts.append(self.config.visual_style)

        prompt_parts.append('16:9')

        return ', '.join(filter(None, prompt_parts))

    def _generate_video_prompt(
        self,
        cut_info: Dict,
        camera_movement: str,
        duration: int
    ) -> str:
        """Generate ItoV prompt for video generation"""
        movement_desc = {
            'static': 'static camera with slight natural drift',
            'slow_zoom_in': 'slow zoom in, gradually revealing details',
            'slow_pull_back': 'slow pull back, revealing wider context',
            'tracking': 'smooth tracking shot following action',
            'dolly_in': 'dolly forward toward subject',
            'pan': 'smooth pan across scene',
            'slow_pan': 'slow pan across scene'
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
            'dramatic': 'high contrast lighting',
            'neutral': 'natural lighting'
        }
        return lighting_map.get(mood.lower(), 'natural lighting')

    def _create_style_guide(self, visual_analysis: Optional[Dict]) -> Dict:
        """Create style guide for storyboard"""
        if visual_analysis:
            return {
                'visual_style': visual_analysis.get('style', ''),
                'color_palette': visual_analysis.get('colors', []),
                'mood': visual_analysis.get('mood', ''),
                'lighting': visual_analysis.get('lighting', ''),
                'texture': visual_analysis.get('texture', '')
            }
        else:
            return {
                'visual_style': self.config.visual_style,
                'color_palette': ['#FFE4B5', '#87CEEB'],
                'mood': 'balanced',
                'lighting': 'natural',
                'texture': 'medium detail'
            }

    def _sanitize_title(self, title: str) -> str:
        """
        Sanitize title to create safe directory name (ASCII only)

        Args:
            title: Original title (may contain Japanese/special characters)

        Returns:
            Sanitized title with only alphanumeric and underscores
        """
        # Remove special characters, keep only alphanumeric
        sanitized = re.sub(r'[^\w\s-]', '', title)
        # Replace spaces with underscores
        sanitized = re.sub(r'[\s-]+', '_', sanitized)
        # Remove non-ASCII characters
        sanitized = sanitized.encode('ascii', 'ignore').decode('ascii')
        # Clean up multiple underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')

        # If nothing left, use default
        if not sanitized:
            sanitized = 'storyboard'

        return sanitized.lower()

    def _generate_output_dir(self, title: str, base_dir: str) -> Path:
        """
        Generate timestamped output directory name

        Args:
            title: Storyboard title
            base_dir: Base output directory

        Returns:
            Path object for output directory
        """
        sanitized_title = self._sanitize_title(title)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        dir_name = f"{sanitized_title}_{timestamp}"

        return Path(base_dir) / dir_name

    def _resolve_output_path(self, storyboard: StoryboardData, requested_dir: str) -> Path:
        """
        Resolve final output path based on config settings

        Args:
            storyboard: Storyboard data
            requested_dir: User-requested output directory

        Returns:
            Resolved output path
        """
        if not self.config.auto_naming:
            # Manual mode: use requested directory as-is
            output_path = Path(requested_dir)

            # Check if directory exists and handle overwrite
            if output_path.exists() and not self.config.overwrite:
                # Find next available version number
                version = 2
                while True:
                    versioned_path = Path(f"{requested_dir}_v{version}")
                    if not versioned_path.exists():
                        output_path = versioned_path
                        print(f"⚠️  Directory exists. Using: {output_path}")
                        break
                    version += 1

            return output_path
        else:
            # Auto-naming mode: generate timestamped directory
            return self._generate_output_dir(storyboard.title, requested_dir)

    def save_storyboard(self, storyboard: StoryboardData, output_dir: str):
        """Save storyboard to JSON with automatic naming to prevent overwrites"""
        output_path = self._resolve_output_path(storyboard, output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        json_path = output_path / 'storyboard.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(storyboard.to_dict(), f, ensure_ascii=False, indent=2)

        print(f"\n💾 Saved storyboard to {json_path}")

        self._create_markdown_report(storyboard, output_path)

    def _create_markdown_report(self, storyboard: StoryboardData, output_dir: Path):
        """Create visual markdown report"""
        report = []
        report.append(f"# {storyboard.title}\n")
        report.append(f"**Duration**: {storyboard.duration}s | **Cuts**: {storyboard.num_cuts}\n")
        report.append(f"**Created**: {storyboard.created_at}\n")

        # Check if any images were generated
        images_generated = any(cut.generated_image_path for cut in storyboard.cuts)
        if not images_generated and storyboard.num_cuts > 0:
            report.append("\n---\n")
            report.append("\n> ⚠️ **画像生成について**\n")
            report.append("> \n")
            report.append("> APIが設定されていないか使用できなかったため、画像生成できませんでした。\n")
            report.append("> 各カットの「Image Prompt」を使用して、Gemini 2.5 Flash Image または他の画像生成サービスで手動で生成してください。\n")
            report.append("\n---\n")

        if storyboard.key_visual_analysis:
            report.append("\n## 🎨 Visual Style\n")
            va = storyboard.key_visual_analysis
            report.append(f"- **Style**: {va.get('style', 'N/A')}\n")
            report.append(f"- **Colors**: {', '.join(va.get('colors', []))}\n")
            report.append(f"- **Mood**: {va.get('mood', 'N/A')}\n")

        report.append("\n## 🎬 Storyboard\n")
        for cut in storyboard.cuts:
            report.append(f"\n### Cut {cut.cut_number} ({cut.duration}s)\n")

            if cut.generated_image_path:
                rel_path = Path(cut.generated_image_path).name
                report.append(f"![Cut {cut.cut_number}](frames/{rel_path})\n\n")
            else:
                # Display placeholder when image is not generated
                report.append("\n> 📸 **Image not generated** (API key not available)\n")
                report.append("> Use the Image Prompt below to generate this frame with Imagen 3 or other image generation services.\n\n")

            report.append(f"**Scene**: {cut.scene_description}\n")
            report.append(f"**Action**: {cut.action}\n")
            report.append(f"**Camera**: {cut.camera_angle} | {cut.composition}\n")
            report.append(f"**Movement**: {cut.camera_movement}\n")
            report.append(f"**Mood**: {cut.mood} | {cut.lighting}\n")

            # Add narration if available
            if cut.narration_text:
                report.append(f"\n**Narration** ({cut.narration_timing or 'start'} - {cut.narration_duration or 0}s):\n")
                report.append("```\n")
                report.append(f"{cut.narration_text}\n")
                report.append("```\n")
                if cut.narration_style:
                    report.append(f"> 💡 Style: {cut.narration_style} | Timing: {cut.narration_timing or 'start'} | Duration: ~{cut.narration_duration or 0}s\n")

            report.append(f"\n**Image Prompt**:\n```\n{cut.image_prompt}\n```\n")
            report.append(f"\n**Video Prompt**:\n```\n{cut.video_prompt}\n```\n")

            # Add Veo3 and Sora2 prompts if available
            if cut.veo3_prompt:
                report.append(f"\n**Veo 3 Prompt**:\n```\n{cut.veo3_prompt}\n```\n")
            if cut.sora2_prompt:
                report.append(f"\n**Sora 2 Prompt**:\n```\n{cut.sora2_prompt}\n```\n")
            if cut.recommended_model:
                report.append(f"\n**Recommended Model**: {cut.recommended_model}\n")

            report.append("\n---\n")

        if storyboard.music_sections:
            report.append("\n## 🎵 BGM Structure\n")
            for section in storyboard.music_sections:
                report.append(f"\n### Section {section['section_id']}\n")
                report.append(f"**Cuts**: {section['cuts']} | **Duration**: {section['duration']}\n")
                report.append(f"**Mood**: {section['mood']} | **Energy**: {section['energy']}/10\n")
                report.append(f"**Tempo**: {section['tempo']}\n")
                if 'genre' in section:
                    report.append(f"**Genre**: {section['genre']}\n")
                report.append(f"\n```\n{section['suno_prompt']}\n```\n")

        # Add style guide section
        if storyboard.style_guide:
            report.append("\n## 🎨 Style Guide\n\n")
            sg = storyboard.style_guide
            if 'visual_style' in sg:
                report.append(f"- **Visual Style**: {sg['visual_style']}\n")
            if 'color_palette' in sg:
                colors = ', '.join(sg['color_palette']) if isinstance(sg['color_palette'], list) else sg['color_palette']
                report.append(f"- **Color Palette**: {colors}\n")
            if 'mood' in sg:
                report.append(f"- **Mood**: {sg['mood']}\n")
            if 'lighting' in sg:
                report.append(f"- **Lighting**: {sg['lighting']}\n")
            if 'texture' in sg:
                report.append(f"- **Texture**: {sg['texture']}\n")

        report_path = output_dir / 'storyboard_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(''.join(report))

        print(f"📄 Saved report to {report_path}")
