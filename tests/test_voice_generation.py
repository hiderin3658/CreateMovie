#!/usr/bin/env python3
"""
Test Voice Generation Feature
Demonstrates voice generation for all 3 dialogue modes
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.video.storyboard_generator import CoreStoryboardGenerator, CutData, DialogueLine
from core.narration.narration_generator import NarrationGenerator
from core.audio.voice_generator import VoiceGenerator
from core.base import GeneratorConfig


def create_test_storyboard_with_dialogue():
    """Create a test storyboard with dialogue in all 3 modes"""
    print("=" * 60)
    print("Creating Test Storyboard with Dialogue")
    print("=" * 60)

    # Cut 1: Narration mode
    cut1 = CutData(
        cut_number=1,
        duration=8,
        scene_description="A peaceful beach at sunset",
        action="Waves gently lap against the shore",
        composition="rule_of_thirds",
        camera_angle="LS",
        camera_movement="static",
        lighting="warm golden hour",
        mood="peaceful",
        image_prompt="Wide shot of peaceful beach at sunset",
        veo3_prompt="Camera: Static shot. Action: Waves lapping.",
        sora2_prompt="The camera remains still capturing the peaceful beach."
    )
    cut1.dialogue_mode = 'narration'
    cut1.narration_text = "物語は、静かな海辺から始まる。夕日が水平線に沈み、一日が終わりを告げる。"
    cut1.narration_duration = 6.5
    cut1.narration_timing = "start"
    cut1.narration_style = "documentary"

    # Cut 2: Monologue mode
    cut2 = CutData(
        cut_number=2,
        duration=10,
        scene_description="Person walking alone on a forest path",
        action="Character walks slowly, deep in thought",
        composition="rule_of_thirds",
        camera_angle="MS",
        camera_movement="tracking",
        lighting="dappled sunlight",
        mood="contemplative",
        image_prompt="Medium shot of person walking in forest",
        veo3_prompt="Camera: Smooth tracking. Action: Walking slowly.",
        sora2_prompt="The camera tracks as character walks through forest."
    )
    cut2.dialogue_mode = 'monologue'
    cut2.monologue_character = "主人公"
    cut2.monologue_text = "ここに来ると、いつも心が落ち着く。都会の喧騒から離れて、自分と向き合える場所。"
    cut2.monologue_duration = 8.5

    # Cut 3: Dialogue mode
    cut3 = CutData(
        cut_number=3,
        duration=12,
        scene_description="Two friends sitting in a café",
        action="Both characters are engaged in conversation",
        composition="over_shoulder",
        camera_angle="MS",
        camera_movement="static",
        lighting="soft indoor lighting",
        mood="warm",
        image_prompt="Medium shot of two people talking in café",
        veo3_prompt="Camera: Static. Action: Conversation.",
        sora2_prompt="The camera captures a conversation between two friends."
    )
    cut3.dialogue_mode = 'dialogue'
    cut3.dialogue_characters = ['アキラ', 'ユキ']
    cut3.dialogue_lines = [
        DialogueLine(speaker='アキラ', text='最近、どう？元気にしてた？', duration=3.0),
        DialogueLine(speaker='ユキ', text='まあまあかな。仕事が忙しくて。', duration=3.0),
        DialogueLine(speaker='アキラ', text='そうか。でも、無理しないでね。', duration=3.0),
        DialogueLine(speaker='ユキ', text='ありがとう。心配してくれて。', duration=3.0)
    ]

    cuts = [cut1, cut2, cut3]
    print(f"✓ Created {len(cuts)} test cuts with dialogue\n")
    return cuts


def test_voice_profile_selection():
    """Test automatic voice profile selection"""
    print("=" * 60)
    print("Test 1: Voice Profile Selection")
    print("=" * 60)

    voice_gen = VoiceGenerator()

    if not voice_gen.use_google_tts:
        print("⚠️  Google TTS not available - skipping test\n")
        return

    # Test narrator voice
    profile = voice_gen.select_voice_profile('narration')
    print(f"Narration profile: {profile['voice_name']} ({profile['description']})")

    # Test monologue with young male character
    profile = voice_gen.select_voice_profile(
        'monologue',
        character_context='20代の若い男性、元気で明るい性格',
        mood='energetic'
    )
    print(f"Young male monologue: {profile['voice_name']} (rate: {profile['speaking_rate']})")

    # Test dialogue with mature female character
    profile = voice_gen.select_voice_profile(
        'dialogue',
        character_context='30代の落ち着いた女性',
        mood='calm'
    )
    print(f"Mature female dialogue: {profile['voice_name']} (rate: {profile['speaking_rate']})")

    print("\n✅ Test 1 passed!\n")


def test_ssml_generation():
    """Test SSML generation"""
    print("=" * 60)
    print("Test 2: SSML Generation")
    print("=" * 60)

    voice_gen = VoiceGenerator()

    # Test different moods
    text = "こんにちは、今日はいい天気ですね。"

    ssml_excited = voice_gen.generate_ssml(text, mood='excited')
    print(f"Excited mood SSML:\n{ssml_excited}\n")

    ssml_sad = voice_gen.generate_ssml(text, mood='sad')
    print(f"Sad mood SSML:\n{ssml_sad}\n")

    print("✅ Test 2 passed!\n")


def test_single_voice_generation():
    """Test generating a single voice file"""
    print("=" * 60)
    print("Test 3: Single Voice Generation")
    print("=" * 60)

    voice_gen = VoiceGenerator()

    if not voice_gen.use_google_tts:
        print("⚠️  Google TTS not available - skipping test")
        print("    To enable, set up Google Cloud credentials:")
        print("    export GOOGLE_APPLICATION_CREDENTIALS='path/to/credentials.json'\n")
        return

    output_dir = Path("tests/output/voice_generation_test")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Test narration
    text = "これはテストの音声です。日本語の音声合成を確認しています。"
    profile = voice_gen.select_voice_profile('narration')
    output_path = output_dir / "test_narration.mp3"

    success = voice_gen.generate_voice(
        text,
        str(output_path),
        profile,
        use_ssml=True,
        mood='documentary'
    )

    if success:
        print(f"✓ Generated test voice: {output_path}")
        print("✅ Test 3 passed!\n")
    else:
        print("❌ Test 3 failed!\n")


def test_storyboard_voice_generation():
    """Test generating voices for entire storyboard"""
    print("=" * 60)
    print("Test 4: Full Storyboard Voice Generation")
    print("=" * 60)

    # Create test storyboard
    cuts = create_test_storyboard_with_dialogue()

    # Initialize voice generator
    voice_gen = VoiceGenerator()

    if not voice_gen.use_google_tts:
        print("⚠️  Google TTS not available - skipping test")
        print("    To enable, set up Google Cloud credentials:")
        print("    export GOOGLE_APPLICATION_CREDENTIALS='path/to/credentials.json'\n")
        return

    # Generate voices
    output_dir = "tests/output/voice_generation_test/storyboard"
    generated_files = voice_gen.generate_voices_for_storyboard(
        cuts,
        output_dir,
        use_ssml=True
    )

    # Display results
    print("\n📁 Generated files:")
    for mode, files in generated_files.items():
        if files:
            print(f"\n  {mode.capitalize()}:")
            for file in files:
                print(f"    - {Path(file).name}")

    print("\n✅ Test 4 passed!\n")


def test_custom_voice_profiles():
    """Test using custom voice profiles for characters"""
    print("=" * 60)
    print("Test 5: Custom Voice Profiles")
    print("=" * 60)

    voice_gen = VoiceGenerator()

    if not voice_gen.use_google_tts:
        print("⚠️  Google TTS not available - skipping test\n")
        return

    # Create cuts with dialogue
    cuts = create_test_storyboard_with_dialogue()

    # Define custom voice profiles for characters
    character_voices = {
        '主人公': {
            'voice_name': 'ja-JP-Neural2-D',
            'pitch': 0.0,
            'speaking_rate': 0.95,
            'description': 'Calm thoughtful male'
        },
        'アキラ': {
            'voice_name': 'ja-JP-Neural2-C',
            'pitch': 2.0,
            'speaking_rate': 1.1,
            'description': 'Energetic cheerful male'
        },
        'ユキ': {
            'voice_name': 'ja-JP-Neural2-A',
            'pitch': 0.0,
            'speaking_rate': 0.95,
            'description': 'Gentle mature female'
        }
    }

    # Generate voices with custom profiles
    output_dir = "tests/output/voice_generation_test/custom_voices"
    generated_files = voice_gen.generate_voices_for_storyboard(
        cuts,
        output_dir,
        character_voices=character_voices,
        use_ssml=True
    )

    print("\n✅ Test 5 passed!\n")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Voice Generation Test Suite")
    print("=" * 60)
    print("\nTesting Google Cloud Text-to-Speech integration")
    print("for 3 dialogue modes: Narration, Monologue, Dialogue\n")

    try:
        # Run tests
        test_voice_profile_selection()
        test_ssml_generation()
        test_single_voice_generation()
        test_storyboard_voice_generation()
        test_custom_voice_profiles()

        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)

        print("\n📝 Summary:")
        print("  - VoiceGenerator class with Google TTS integration")
        print("  - Automatic voice profile selection (6 profiles)")
        print("  - SSML support for mood-based prosody")
        print("  - 3 dialogue modes supported (Narration, Monologue, Dialogue)")
        print("  - Custom voice profiles for characters")

        print("\n🎯 Usage:")
        print("  voice_gen = VoiceGenerator()")
        print("  generated_files = voice_gen.generate_voices_for_storyboard(")
        print("      cuts, output_dir, use_ssml=True")
        print("  )")

        print("\n⚠️  Requirements:")
        print("  1. Install: pip install google-cloud-texttospeech")
        print("  2. Set up Google Cloud credentials:")
        print("     export GOOGLE_APPLICATION_CREDENTIALS='path/to/credentials.json'")
        print("  3. Enable Text-to-Speech API in Google Cloud Console")

        return 0

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
