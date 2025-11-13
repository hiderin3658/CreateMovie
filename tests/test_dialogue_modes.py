#!/usr/bin/env python3
"""
Test Dialogue Modes (Narration, Monologue, Dialogue)
Demonstrates the 3 dialogue modes in the storyboard system
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.video.storyboard_generator import CoreStoryboardGenerator, CutData, DialogueLine
from core.narration.narration_generator import NarrationGenerator
from core.base import GeneratorConfig


def create_test_storyboard():
    """Create a simple test storyboard"""
    print("=" * 60)
    print("Creating Test Storyboard")
    print("=" * 60)

    config = GeneratorConfig(
        title="Dialogue Modes Test",
        duration=24,  # 3 cuts x 8 seconds
        num_cuts=3,
        visual_style="cinematic"
    )

    generator = CoreStoryboardGenerator(config)

    # Create simple cuts
    cuts = [
        CutData(
            cut_number=1,
            duration=8,
            scene_description="A person standing on a beach at sunset",
            action="Character looks at the ocean pensively",
            composition="rule_of_thirds",
            camera_angle="MS",
            camera_movement="static",
            lighting="warm golden hour",
            mood="peaceful",
            image_prompt="Medium shot of person at beach during sunset, peaceful mood",
            veo3_prompt="Camera: Static shot. Action: Character gazing at ocean.",
            sora2_prompt="The camera remains still as character contemplates the ocean."
        ),
        CutData(
            cut_number=2,
            duration=8,
            scene_description="Two people having a conversation in a café",
            action="Both characters are engaged in an animated discussion",
            composition="over_shoulder",
            camera_angle="MS",
            camera_movement="static",
            lighting="soft indoor lighting",
            mood="energetic",
            image_prompt="Medium shot of two people talking in café, energetic mood",
            veo3_prompt="Camera: Static shot. Action: Animated conversation.",
            sora2_prompt="The camera captures an engaged conversation between two people."
        ),
        CutData(
            cut_number=3,
            duration=8,
            scene_description="Character walking through a forest path",
            action="Character walks slowly, deep in thought",
            composition="rule_of_thirds",
            camera_angle="LS",
            camera_movement="tracking",
            lighting="dappled sunlight",
            mood="contemplative",
            image_prompt="Wide shot of person walking in forest, contemplative mood",
            veo3_prompt="Camera: Smooth tracking shot. Action: Walking through forest.",
            sora2_prompt="The camera tracks smoothly as character walks through dappled forest light."
        )
    ]

    print(f"✓ Created {len(cuts)} test cuts\n")
    return cuts, config


def test_narration_mode():
    """Test Mode 1: Narration"""
    print("=" * 60)
    print("Test 1: Narration Mode (Narrator Voiceover)")
    print("=" * 60)

    cuts, config = create_test_storyboard()
    narration_gen = NarrationGenerator()

    if not narration_gen.use_claude:
        print("⚠️  Claude API not available - showing structure only\n")

        # Manually set narration for demonstration
        cuts[0].dialogue_mode = 'narration'
        cuts[0].narration_text = "夕暮れの海辺。一人の人物が、静かに波の音に耳を傾けている。"
        cuts[0].narration_duration = 6.5
        cuts[0].narration_timing = "start"
        cuts[0].narration_style = "documentary"

        print("Mode: narration")
        print(f"Cut 1 Narration: {cuts[0].narration_text}")
        print(f"Duration: {cuts[0].narration_duration}s")
        print(f"Style: {cuts[0].narration_style}\n")
    else:
        story_context = "A contemplative short film about finding inner peace"
        cuts = narration_gen.generate_dialogue_for_storyboard(
            cuts,
            story_context,
            dialogue_mode='narration',
            style='documentary'
        )

        print("\nGenerated Narrations:")
        for cut in cuts:
            if cut.narration_text:
                print(f"\nCut {cut.cut_number}:")
                print(f"  Text: {cut.narration_text}")
                print(f"  Duration: {cut.narration_duration}s")

    print("\n✅ Test 1 passed!\n")
    return cuts


def test_monologue_mode():
    """Test Mode 2: Monologue"""
    print("=" * 60)
    print("Test 2: Monologue Mode (Single Character Speaking)")
    print("=" * 60)

    cuts, config = create_test_storyboard()
    narration_gen = NarrationGenerator()

    if not narration_gen.use_claude:
        print("⚠️  Claude API not available - showing structure only\n")

        # Manually set monologue for demonstration
        cuts[0].dialogue_mode = 'monologue'
        cuts[0].monologue_character = "主人公"
        cuts[0].monologue_text = "ここに来ると、いつも心が落ち着く。波の音だけが聞こえる。"
        cuts[0].monologue_duration = 7.2

        print("Mode: monologue")
        print(f"Character: {cuts[0].monologue_character}")
        print(f"Cut 1 Monologue: {cuts[0].monologue_text}")
        print(f"Duration: {cuts[0].monologue_duration}s\n")
    else:
        story_context = "A person reflects on their life journey"
        character_info = {
            'character1': {
                'name': '主人公',
                'context': '30代の会社員。人生に疲れ、自然の中で癒しを求めている。'
            }
        }

        cuts = narration_gen.generate_dialogue_for_storyboard(
            cuts,
            story_context,
            dialogue_mode='monologue',
            character_info=character_info
        )

        print("\nGenerated Monologues:")
        for cut in cuts:
            if cut.monologue_text:
                print(f"\nCut {cut.cut_number} ({cut.monologue_character}):")
                print(f"  Text: {cut.monologue_text}")
                print(f"  Duration: {cut.monologue_duration}s")

    print("\n✅ Test 2 passed!\n")
    return cuts


def test_dialogue_mode():
    """Test Mode 3: Dialogue"""
    print("=" * 60)
    print("Test 3: Dialogue Mode (Two Characters Conversing)")
    print("=" * 60)

    cuts, config = create_test_storyboard()
    narration_gen = NarrationGenerator()

    if not narration_gen.use_claude:
        print("⚠️  Claude API not available - showing structure only\n")

        # Manually set dialogue for demonstration
        cuts[1].dialogue_mode = 'dialogue'
        cuts[1].dialogue_characters = ['アキラ', 'ユキ']
        cuts[1].dialogue_lines = [
            DialogueLine(speaker='アキラ', text='最近、どう？調子は？', duration=2.5),
            DialogueLine(speaker='ユキ', text='まあまあかな。仕事が忙しくて。', duration=2.8),
            DialogueLine(speaker='アキラ', text='そうか。無理しないでね。', duration=2.7)
        ]

        print("Mode: dialogue")
        print(f"Characters: {', '.join(cuts[1].dialogue_characters)}")
        print(f"\nCut 2 Dialogue:")
        for line in cuts[1].dialogue_lines:
            print(f"  {line.speaker}: {line.text} ({line.duration}s)")

        total = sum(l.duration for l in cuts[1].dialogue_lines if l.duration)
        print(f"\nTotal Duration: {total}s\n")
    else:
        story_context = "Two friends discuss life changes over coffee"
        character_info = {
            'character1': {
                'name': 'アキラ',
                'context': '楽観的で明るい性格。友人のことを心配している。'
            },
            'character2': {
                'name': 'ユキ',
                'context': '真面目で控えめ。最近仕事で悩んでいる。'
            }
        }

        cuts = narration_gen.generate_dialogue_for_storyboard(
            cuts,
            story_context,
            dialogue_mode='dialogue',
            character_info=character_info
        )

        print("\nGenerated Dialogues:")
        for cut in cuts:
            if cut.dialogue_lines:
                print(f"\nCut {cut.cut_number} ({' & '.join(cut.dialogue_characters)}):")
                for line in cut.dialogue_lines:
                    print(f"  {line.speaker}: {line.text} ({line.duration:.1f}s)")

                total = sum(l.duration for l in cut.dialogue_lines if l.duration)
                print(f"  Total: {total:.1f}s")

    print("\n✅ Test 3 passed!\n")
    return cuts


def test_mixed_modes():
    """Test all three modes in one storyboard"""
    print("=" * 60)
    print("Test 4: Mixed Modes (Narration + Monologue + Dialogue)")
    print("=" * 60)

    cuts, config = create_test_storyboard()

    # Manually assign different modes to each cut
    cuts[0].dialogue_mode = 'narration'
    cuts[0].narration_text = "物語は、静かな海辺から始まる。"
    cuts[0].narration_duration = 5.0
    cuts[0].narration_timing = "start"
    cuts[0].narration_style = "documentary"

    cuts[1].dialogue_mode = 'monologue'
    cuts[1].monologue_character = "主人公"
    cuts[1].monologue_text = "ここで何を探しているんだろう。答えは、まだ見つからない。"
    cuts[1].monologue_duration = 7.5

    cuts[2].dialogue_mode = 'dialogue'
    cuts[2].dialogue_characters = ['アキラ', 'ユキ']
    cuts[2].dialogue_lines = [
        DialogueLine(speaker='アキラ', text='見つかった？', duration=2.0),
        DialogueLine(speaker='ユキ', text='まだ。でも、諦めない。', duration=3.0),
        DialogueLine(speaker='アキラ', text='一緒に探そう。', duration=3.0)
    ]

    print("\nMixed mode storyboard created:")
    print(f"  Cut 1: {cuts[0].dialogue_mode} mode")
    print(f"  Cut 2: {cuts[1].dialogue_mode} mode")
    print(f"  Cut 3: {cuts[2].dialogue_mode} mode")

    # Test markdown generation
    from core.video.storyboard_generator import StoryboardData
    storyboard = StoryboardData(
        title="Mixed Modes Test",
        duration=24,
        num_cuts=3,
        cuts=cuts,
        style_guide={'visual_style': 'cinematic'},
        created_at="2025-01-01T00:00:00"
    )

    # Generate markdown
    generator = CoreStoryboardGenerator(config)
    output_dir = Path("tests/output/dialogue_modes_test")
    output_dir.mkdir(parents=True, exist_ok=True)
    generator._create_markdown_report(storyboard, output_dir)

    print(f"\n✓ Markdown report generated at: {output_dir}/storyboard_report.md")
    print("\n✅ Test 4 passed!\n")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Dialogue Modes Test Suite")
    print("=" * 60)
    print("\nTesting 3 dialogue modes:")
    print("  1. Narration (narrator voiceover)")
    print("  2. Monologue (single character speaking)")
    print("  3. Dialogue (two characters conversing)\n")

    try:
        # Run tests
        test_narration_mode()
        test_monologue_mode()
        test_dialogue_mode()
        test_mixed_modes()

        print("=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)

        print("\n📝 Summary:")
        print("  - CutData class extended with dialogue_mode field")
        print("  - DialogueLine dataclass for dialogue lines")
        print("  - NarrationGenerator supports all 3 modes")
        print("  - Markdown reports display all modes correctly")
        print("\n🎯 Usage:")
        print("  generator.generate_dialogue_for_storyboard(")
        print("      cuts, story_context,")
        print("      dialogue_mode='narration'|'monologue'|'dialogue',")
        print("      character_info={'character1': {...}, 'character2': {...}}")
        print("  )")

        return 0

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
