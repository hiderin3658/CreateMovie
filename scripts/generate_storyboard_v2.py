#!/usr/bin/env python3
"""
AI Video Storyboard Generator V2 - Modular Version
Complete workflow using the new modular architecture
"""
import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from core.base import GeneratorConfig
from core.video import CoreStoryboardGenerator, ImageGenerator
from core.analysis import VisualAnalyzer
from core.music import MusicGenerator


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='AI Video Storyboard Generator V2 (Modular)'
    )
    parser.add_argument('story', help='Story description')
    parser.add_argument('--key-visual', help='Key visual reference image path')
    parser.add_argument('--duration', type=int, default=60, help='Video duration in seconds')
    parser.add_argument('--cuts', type=int, help='Number of cuts (default: auto)')
    parser.add_argument('--output', default='outputs', help='Output base directory (default: outputs)')
    parser.add_argument('--title', help='Storyboard title')
    parser.add_argument('--style', help='Visual style (cinematic, anime, etc.)')
    parser.add_argument('--no-images', action='store_true', help='Skip image generation')
    parser.add_argument('--no-music', action='store_true', help='Skip music generation')
    parser.add_argument('--no-auto-naming', action='store_true', help='Disable automatic timestamped naming')
    parser.add_argument('--overwrite', action='store_true', help='Allow overwriting existing directory')

    args = parser.parse_args()

    # Create configuration
    config = GeneratorConfig(
        duration=args.duration,
        num_cuts=args.cuts,
        visual_style=args.style or 'cinematic',
        generate_images=not args.no_images,
        generate_music=not args.no_music,
        output_dir=args.output,
        title=args.title or 'AI Generated Storyboard',
        auto_naming=not args.no_auto_naming,
        overwrite=args.overwrite
    )

    print("="*60)
    print("🎬 AI Video Storyboard Generator V2 (Modular)")
    print("="*60)
    print(f"\nStory: {args.story}")
    if args.key_visual:
        print(f"Key Visual: {args.key_visual}")
    print(f"Duration: {args.duration}s")
    print(f"Output: {args.output}")
    print()

    # Step 1: Analyze key visual if provided
    visual_analysis = None
    if args.key_visual:
        print(f"📸 Analyzing key visual: {args.key_visual}")
        analyzer = VisualAnalyzer()
        visual_analysis_obj = analyzer.analyze_key_visual(args.key_visual)
        visual_analysis = visual_analysis_obj.to_dict()
        print(f"  ✓ Style: {visual_analysis['style']}")
        print(f"  ✓ Colors: {', '.join(visual_analysis['colors'][:3])}")
        print(f"  ✓ Mood: {visual_analysis['mood']}")

    # Step 2: Generate storyboard
    generator = CoreStoryboardGenerator(config)

    input_data = {
        'story_description': args.story,
        'key_visual_path': args.key_visual,
        'visual_analysis': visual_analysis
    }

    storyboard = generator.generate_storyboard(input_data)

    # Step 3: Generate images if requested
    if config.generate_images:
        print("\n🎨 Generating images with Imagen 3...")
        image_gen = ImageGenerator()
        image_gen.generate_images(storyboard.cuts, config.output_dir)

    # Step 4: Generate music prompts if requested
    if config.generate_music:
        print("\n🎵 Generating BGM prompts...")
        music_gen = MusicGenerator()
        music_plan = music_gen.generate_music_plan(storyboard.to_dict())
        storyboard.music_sections = music_plan['sections']
        print(f"  ✓ Created {len(music_plan['sections'])} music sections")

    # Step 5: Save results
    generator.save_storyboard(storyboard, config.output_dir)

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
