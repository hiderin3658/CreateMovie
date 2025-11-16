#!/usr/bin/env python3
"""
Test Subtitle Generation Feature
Demonstrates subtitle generation for all 3 dialogue modes
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.video.storyboard_generator import CutData, DialogueLine, SubtitleLine
from core.video.subtitle_generator import SubtitleGenerator


def test_narration_subtitles():
    """Test subtitle generation for narration mode"""
    print("=" * 60)
    print("Test 1: Narration Subtitles")
    print("=" * 60)

    # Create cut with narration
    cut = CutData(
        cut_number=1,
        duration=10,
        scene_description="Beautiful sunset beach",
        action="Waves gently lap the shore",
        composition="rule_of_thirds",
        camera_angle="LS",
        camera_movement="static",
        lighting="golden hour",
        mood="peaceful",
        image_prompt="Beautiful sunset beach scene",
        veo3_prompt="Static shot of beach at sunset",
        sora2_prompt="Peaceful beach scene at golden hour"
    )
    cut.dialogue_mode = 'narration'
    cut.narration_text = "物語は、静かな海辺から始まる。夕日が水平線に沈み、一日が終わりを告げる。波の音だけが聞こえる、穏やかな時間。"
    cut.narration_duration = 10.0
    cut.narration_style = 'documentary'

    # Generate subtitles
    subtitle_gen = SubtitleGenerator()

    # Test 1: Documentary style (auto = no subtitles)
    subtitles = subtitle_gen.generate_narration_subtitles(cut, style='auto')
    print(f"\nDocumentary style (auto):")
    print(f"  Subtitles generated: {len(subtitles)}")
    print(f"  Expected: 0 (documentary usually has no subtitles)")
    assert len(subtitles) == 0, "Documentary should have no subtitles in auto mode"

    # Test 2: Force full subtitles
    subtitles = subtitle_gen.generate_narration_subtitles(cut, style='full')
    print(f"\nForced full style:")
    print(f"  Subtitles generated: {len(subtitles)}")
    for i, sub in enumerate(subtitles, 1):
        print(f"  {i}. [{sub.start_time:.1f}s - {sub.end_time:.1f}s] {sub.text}")

    assert len(subtitles) > 0, "Full style should generate subtitles"
    print("\n✅ Test 1 passed!\n")


def test_monologue_subtitles():
    """Test subtitle generation for monologue mode"""
    print("=" * 60)
    print("Test 2: Monologue Subtitles")
    print("=" * 60)

    # Create cut with monologue
    cut = CutData(
        cut_number=2,
        duration=12,
        scene_description="Person walking alone in forest",
        action="Character walks slowly, deep in thought",
        composition="rule_of_thirds",
        camera_angle="MS",
        camera_movement="tracking",
        lighting="dappled sunlight",
        mood="contemplative",
        image_prompt="Person walking in forest",
        veo3_prompt="Tracking shot of person walking",
        sora2_prompt="Contemplative walk through forest"
    )
    cut.dialogue_mode = 'monologue'
    cut.monologue_character = "主人公"
    cut.monologue_text = "ここに来ると、いつも心が落ち着く。都会の喧騒から離れて、自分と向き合える場所。誰にも邪魔されず、ただ静かに歩くことができる。"
    cut.monologue_duration = 12.0

    # Generate subtitles
    subtitle_gen = SubtitleGenerator()
    subtitles = subtitle_gen.generate_monologue_subtitles(cut, style='auto')

    print(f"\nMonologue subtitles:")
    print(f"  Character: {cut.monologue_character}")
    print(f"  Subtitles generated: {len(subtitles)}")
    for i, sub in enumerate(subtitles, 1):
        speaker_info = f"({sub.speaker})" if sub.speaker else "(no speaker)"
        print(f"  {i}. [{sub.start_time:.1f}s - {sub.end_time:.1f}s] {speaker_info} {sub.text}")

    assert len(subtitles) > 0, "Monologue should generate subtitles"
    # Monologue should NOT have speaker names in subtitles
    assert all(sub.speaker is None for sub in subtitles), "Monologue subtitles should not have speaker names"

    print("\n✅ Test 2 passed!\n")


def test_dialogue_subtitles():
    """Test subtitle generation for dialogue mode"""
    print("=" * 60)
    print("Test 3: Dialogue Subtitles")
    print("=" * 60)

    # Create cut with dialogue
    cut = CutData(
        cut_number=3,
        duration=15,
        scene_description="Two friends talking in café",
        action="Engaged in conversation",
        composition="over_shoulder",
        camera_angle="MS",
        camera_movement="static",
        lighting="soft indoor",
        mood="warm",
        image_prompt="Two friends in café conversation",
        veo3_prompt="Static shot of café conversation",
        sora2_prompt="Warm conversation between friends"
    )
    cut.dialogue_mode = 'dialogue'
    cut.dialogue_characters = ['アキラ', 'ユキ']
    cut.dialogue_lines = [
        DialogueLine(speaker='アキラ', text='最近、どう？元気にしてた？', duration=3.0),
        DialogueLine(speaker='ユキ', text='まあまあかな。仕事が忙しくて、なかなか休めないんだよね。', duration=4.0),
        DialogueLine(speaker='アキラ', text='そうか。でも、無理しないでね。体が一番大事だから。', duration=4.0),
        DialogueLine(speaker='ユキ', text='ありがとう。心配してくれて嬉しいよ。', duration=3.0)
    ]

    # Generate subtitles
    subtitle_gen = SubtitleGenerator()

    # Test 1: With speaker names (auto)
    subtitles = subtitle_gen.generate_dialogue_subtitles(cut, style='auto')
    print(f"\nDialogue subtitles (with speaker):")
    print(f"  Characters: {', '.join(cut.dialogue_characters)}")
    print(f"  Subtitles generated: {len(subtitles)}")
    for i, sub in enumerate(subtitles, 1):
        speaker_info = f"({sub.speaker})" if sub.speaker else ""
        print(f"  {i}. [{sub.start_time:.1f}s - {sub.end_time:.1f}s] {speaker_info} {sub.text}")

    assert len(subtitles) > 0, "Dialogue should generate subtitles"
    # Auto mode should include speaker names
    assert any(sub.speaker for sub in subtitles), "Dialogue should have speaker names in auto mode"

    # Test 2: Without speaker names
    print(f"\nDialogue subtitles (without speaker):")
    subtitles_no_speaker = subtitle_gen.generate_dialogue_subtitles(cut, style='without_speaker')
    for i, sub in enumerate(subtitles_no_speaker, 1):
        print(f"  {i}. [{sub.start_time:.1f}s - {sub.end_time:.1f}s] {sub.text}")

    print("\n✅ Test 3 passed!\n")


def test_text_splitting():
    """Test text splitting for long subtitles"""
    print("=" * 60)
    print("Test 4: Text Splitting")
    print("=" * 60)

    subtitle_gen = SubtitleGenerator()

    # Test 1: Short text (no split needed)
    short_text = "こんにちは。"
    lines = subtitle_gen.split_text_into_lines(short_text)
    print(f"\nShort text: '{short_text}'")
    print(f"  Split into {len(lines)} line(s)")
    assert len(lines) == 1, "Short text should not be split"

    # Test 2: Long text (needs splitting)
    long_text = "これは非常に長いテキストで、字幕として表示するには長すぎます。適切に分割する必要があります。そうしないと読みにくくなってしまいます。"
    lines = subtitle_gen.split_text_into_lines(long_text, max_chars=40)
    print(f"\nLong text: '{long_text}'")
    print(f"  Split into {len(lines)} line(s):")
    for i, line in enumerate(lines, 1):
        print(f"    {i}. {line} ({len(line)} chars)")

    assert len(lines) > 1, "Long text should be split"
    assert all(len(line) <= 40 for line in lines), "All lines should be within max chars"

    print("\n✅ Test 4 passed!\n")


def test_timing_calculation():
    """Test subtitle timing calculation"""
    print("=" * 60)
    print("Test 5: Timing Calculation")
    print("=" * 60)

    subtitle_gen = SubtitleGenerator()

    # Test single line timing
    text = "こんにちは、元気ですか？"
    start, end = subtitle_gen.calculate_timing(text, total_duration=10.0, num_lines=1, line_index=0)
    print(f"\nSingle line: '{text}'")
    print(f"  Duration: 10.0s")
    print(f"  Timing: {start:.1f}s - {end:.1f}s (duration: {end-start:.1f}s)")

    # Test multiple lines timing
    lines = ["最初の行です。", "二番目の行です。", "最後の行です。"]
    print(f"\nMultiple lines (3 lines, 15.0s total):")
    for i, line in enumerate(lines):
        start, end = subtitle_gen.calculate_timing(line, total_duration=15.0, num_lines=3, line_index=i)
        print(f"  Line {i+1}: {start:.1f}s - {end:.1f}s | '{line}'")

    print("\n✅ Test 5 passed!\n")


def test_storyboard_subtitles():
    """Test generating subtitles for complete storyboard"""
    print("=" * 60)
    print("Test 6: Complete Storyboard Subtitles")
    print("=" * 60)

    # Create storyboard with mixed modes
    cuts = []

    # Cut 1: Narration
    cut1 = CutData(
        cut_number=1,
        duration=8,
        scene_description="Sunset beach",
        action="Waves lapping",
        composition="rule_of_thirds",
        camera_angle="LS",
        camera_movement="static",
        lighting="golden",
        mood="peaceful",
        image_prompt="Beach sunset",
        veo3_prompt="Static beach",
        sora2_prompt="Peaceful sunset"
    )
    cut1.dialogue_mode = 'narration'
    cut1.narration_text = "物語は海辺から始まる。"
    cut1.narration_duration = 5.0
    cut1.narration_style = 'cinematic'  # Not documentary, so subtitles will be generated
    cuts.append(cut1)

    # Cut 2: Monologue
    cut2 = CutData(
        cut_number=2,
        duration=10,
        scene_description="Forest path",
        action="Walking alone",
        composition="rule_of_thirds",
        camera_angle="MS",
        camera_movement="tracking",
        lighting="dappled",
        mood="contemplative",
        image_prompt="Forest walk",
        veo3_prompt="Tracking shot",
        sora2_prompt="Forest path"
    )
    cut2.dialogue_mode = 'monologue'
    cut2.monologue_character = "主人公"
    cut2.monologue_text = "ここは静かで心地よい。"
    cut2.monologue_duration = 7.0
    cuts.append(cut2)

    # Cut 3: Dialogue
    cut3 = CutData(
        cut_number=3,
        duration=12,
        scene_description="Café conversation",
        action="Two friends talking",
        composition="over_shoulder",
        camera_angle="MS",
        camera_movement="static",
        lighting="soft",
        mood="warm",
        image_prompt="Café scene",
        veo3_prompt="Static conversation",
        sora2_prompt="Warm café"
    )
    cut3.dialogue_mode = 'dialogue'
    cut3.dialogue_characters = ['アキラ', 'ユキ']
    cut3.dialogue_lines = [
        DialogueLine(speaker='アキラ', text='元気？', duration=2.0),
        DialogueLine(speaker='ユキ', text='うん、元気だよ。', duration=2.5)
    ]
    cuts.append(cut3)

    # Generate subtitles for all cuts
    subtitle_gen = SubtitleGenerator()
    cuts_with_subtitles = subtitle_gen.generate_subtitles_for_storyboard(cuts)

    # Verify
    print(f"\nGenerated subtitles for {len(cuts_with_subtitles)} cuts:")
    for cut in cuts_with_subtitles:
        subtitle_count = len(cut.subtitle_lines) if cut.subtitle_lines else 0
        print(f"  Cut {cut.cut_number} ({cut.dialogue_mode}): {subtitle_count} subtitle lines")

    print("\n✅ Test 6 passed!\n")


def test_srt_export():
    """Test SRT format export"""
    print("=" * 60)
    print("Test 7: SRT Export")
    print("=" * 60)

    # Create cut with subtitles
    cut = CutData(
        cut_number=1,
        duration=10,
        scene_description="Test scene",
        action="Test action",
        composition="rule_of_thirds",
        camera_angle="MS",
        camera_movement="static",
        lighting="soft",
        mood="neutral",
        image_prompt="Test",
        veo3_prompt="Test",
        sora2_prompt="Test"
    )
    cut.dialogue_mode = 'monologue'
    cut.monologue_character = "テスト"
    cut.monologue_text = "これはテストです。字幕が正しく表示されるか確認します。"
    cut.monologue_duration = 8.0

    # Generate subtitles
    subtitle_gen = SubtitleGenerator()
    cut.subtitle_lines = subtitle_gen.generate_monologue_subtitles(cut, style='auto')

    # Generate SRT format
    srt_text = subtitle_gen.format_subtitle_srt(cut, cut_start_time=0.0)
    print("\nGenerated SRT:")
    print(srt_text)

    # Export to file
    output_path = Path("tests/output/test_subtitles.srt")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    success = subtitle_gen.export_srt([cut], str(output_path))
    assert success, "SRT export should succeed"

    print(f"\n✅ Test 7 passed! SRT saved to {output_path}\n")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Subtitle Generation Test Suite")
    print("=" * 60)
    print("\nTesting automatic subtitle generation for 3 dialogue modes\n")

    try:
        # Run tests
        test_narration_subtitles()
        test_monologue_subtitles()
        test_dialogue_subtitles()
        test_text_splitting()
        test_timing_calculation()
        test_storyboard_subtitles()
        test_srt_export()

        print("=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)

        print("\n📝 Summary:")
        print("  - SubtitleGenerator class with 3 dialogue modes support")
        print("  - Automatic text splitting (max 40 chars per line)")
        print("  - Timing calculation based on reading speed")
        print("  - SRT format export")
        print("  - Different subtitle styles:")
        print("    • Narration: Optional (auto=none for documentary)")
        print("    • Monologue: Full text without speaker names")
        print("    • Dialogue: Text with speaker names (auto) or without")

        print("\n🎯 Usage:")
        print("  subtitle_gen = SubtitleGenerator()")
        print("  cuts = subtitle_gen.generate_subtitles_for_storyboard(cuts)")
        print("  subtitle_gen.export_srt(cuts, 'output.srt')")

        return 0

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
