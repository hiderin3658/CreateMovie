#!/usr/bin/env python3
"""
AI Video Storyboard Generator V2 - Modular Version
Complete workflow using the new modular architecture
"""
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
from core.narration import NarrationGenerator


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='AI Video Storyboard Generator V2 (Modular)'
    )
    parser.add_argument('story', help='Story description')
    parser.add_argument('--key-visual', help='Key visual reference image path (single image)')
    parser.add_argument('--reference-images', nargs='+', help='Reference images (up to 3 images for Gemini 2.5 Flash Image)')
    parser.add_argument('--duration', type=int, default=60, help='Video duration in seconds')
    parser.add_argument('--cuts', type=int, help='Number of cuts (default: auto)')
    parser.add_argument('--output', default='outputs', help='Output base directory (default: outputs)')
    parser.add_argument('--title', help='Storyboard title')
    parser.add_argument('--style', help='Visual style (cinematic, anime, etc.)')
    parser.add_argument('--no-images', action='store_true', help='Skip image generation')
    parser.add_argument('--no-music', action='store_true', help='Skip music generation')
    parser.add_argument('--narration', action='store_true', help='Generate narration text')
    parser.add_argument('--narration-style', default='documentary', help='Narration style (documentary, dramatic, casual, epic)')
    parser.add_argument('--narration-language', default='ja', help='Narration language (ja, en)')
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
        overwrite=args.overwrite,
        generate_narrations=args.narration,
        narration_style=args.narration_style,
        narration_language=args.narration_language
    )

    print("=" * 60)
    print("🎬 AI Video Storyboard Generator V2 (Modular)")
    print("=" * 60)
    print(f"\nStory: {args.story}")

    # Handle reference images (support both --key-visual and --reference-images)
    reference_images = []
    if args.reference_images:
        reference_images = args.reference_images[:3]  # Limit to 3 images (Gemini 2.5 Flash Image limit)
        print(f"Reference Images: {len(reference_images)} images")
        for i, img in enumerate(reference_images, 1):
            print(f"  {i}. {img}")
    elif args.key_visual:
        reference_images = [args.key_visual]
        print(f"Key Visual: {args.key_visual}")

    print(f"Duration: {args.duration}s")
    print(f"Output: {args.output}")
    print()

    # Step 1: Analyze reference images if provided
    visual_analysis = None
    if reference_images:
        print(f"📸 Analyzing reference images ({len(reference_images)} images)...")
        analyzer = VisualAnalyzer()
        # Analyze the first reference image for style
        visual_analysis_obj = analyzer.analyze_key_visual(reference_images[0])
        visual_analysis = visual_analysis_obj.to_dict()
        print(f"  ✓ Style: {visual_analysis['style']}")
        print(f"  ✓ Colors: {', '.join(visual_analysis['colors'][:3])}")
        print(f"  ✓ Mood: {visual_analysis['mood']}")

    # Step 2: Generate storyboard
    generator = CoreStoryboardGenerator(config)

    input_data = {
        'story_description': args.story,
        'key_visual_path': reference_images[0] if reference_images else None,
        'reference_images': reference_images if reference_images else None,
        'visual_analysis': visual_analysis
    }

    storyboard = generator.generate_storyboard(input_data)

    # Step 3: Generate images if requested
    if config.generate_images:
        print("\n🎨 Generating images with Imagen 3...")
        image_gen = ImageGenerator()
        image_gen.generate_images(storyboard.cuts, config.output_dir)

    # Step 4: Generate narrations if requested
    if config.generate_narrations:
        narration_gen = NarrationGenerator()
        storyboard.cuts = narration_gen.generate_narrations_for_storyboard(
            storyboard.cuts,
            args.story,
            config.narration_style
        )

    # Step 5: Generate music prompts if requested
    if config.generate_music:
        print("\n🎵 Generating BGM prompts...")
        music_gen = MusicGenerator()
        music_plan = music_gen.generate_music_plan(storyboard.to_dict())
        storyboard.music_sections = music_plan['sections']
        print(f"  ✓ Created {len(music_plan['sections'])} music sections")

    # Step 6: Save results
    generator.save_storyboard(storyboard, config.output_dir)

    print("\n" + "=" * 60)
    print("✅ Generation Complete!")
    print("=" * 60)
    print("\nOutput files:")
    print(f"  📄 {args.output}/storyboard.json")
    print(f"  📄 {args.output}/storyboard_report.md")
    if storyboard.music_sections:
        print(f"  🎵 {len(storyboard.music_sections)} music sections generated")
    if any(cut.generated_image_path for cut in storyboard.cuts):
        print(f"  🖼️  {args.output}/frames/ ({storyboard.num_cuts} images)")
    narration_count = sum(1 for cut in storyboard.cuts if cut.narration_text)
    if narration_count > 0:
        print(f"  🎙️  {narration_count} narrations generated")
    print()


if __name__ == '__main__':
    main()
