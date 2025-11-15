#!/usr/bin/env python3
"""
Enhanced System Test Cases
高度化システムのテスト・検証スクリプト
"""

import sys
from pathlib import Path
import json

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from core.video.enhanced_storyboard_generator import (
    EnhancedStoryboardGenerator, 
    VideoGenre, 
    AspectRatio,
    EmotionalPhase,
    JPOPEmotionalStructure,
    IntelligentSelectionEngine,
    SceneContext,
    VerticalOptimizer,
    EmotionalEngagementEnhancer
)


def test_jpop_structure():
    """J-pop感情構造のテスト"""
    print("🎵 Testing J-pop Emotional Structure...")
    
    story = "白浜の美しい観光地を紹介し、訪問者に魅力を伝える30秒動画"
    duration = 30
    num_cuts = 8
    
    cuts_data = JPOPEmotionalStructure.analyze_story_for_jpop_structure(story, duration, num_cuts)
    
    print(f"   ✓ Generated {len(cuts_data)} cuts")
    
    # 各フェーズの確認
    phases = [cut.get('emotional_phase') for cut in cuts_data]
    phase_counts = {}
    for phase in phases:
        phase_counts[phase] = phase_counts.get(phase, 0) + 1
    
    print(f"   ✓ Phase distribution: {dict(phase_counts)}")
    
    # 強度の確認
    intensities = [cut.get('intensity', 0) for cut in cuts_data]
    print(f"   ✓ Intensity range: {min(intensities):.1f} - {max(intensities):.1f}")
    
    assert len(cuts_data) == num_cuts, "カット数が一致しません"
    assert EmotionalPhase.SABI_HOOK in phases, "サビ（フック）が含まれていません"
    assert EmotionalPhase.SABI_CLIMAX in phases, "サビ（クライマックス）が含まれていません"
    
    print("   ✅ J-pop structure test passed!")
    return cuts_data


def test_intelligent_selection():
    """インテリジェント選択エンジンのテスト"""
    print("\n🧠 Testing Intelligent Selection Engine...")
    
    engine = IntelligentSelectionEngine()
    
    # テスト用コンテキスト
    contexts = [
        SceneContext(
            emotional_phase=EmotionalPhase.SABI_HOOK,
            intensity=0.8,
            pacing='fast',
            mood='energetic',
            genre=VideoGenre.TOURISM,
            aspect_ratio=AspectRatio.VERTICAL
        ),
        SceneContext(
            emotional_phase=EmotionalPhase.A_MELO,
            intensity=0.4,
            pacing='medium',
            mood='peaceful',
            genre=VideoGenre.EDUCATIONAL,
            aspect_ratio=AspectRatio.HORIZONTAL
        ),
        SceneContext(
            emotional_phase=EmotionalPhase.SABI_CLIMAX,
            intensity=1.0,
            pacing='fast',
            mood='dramatic',
            genre=VideoGenre.COMMERCIAL,
            aspect_ratio=AspectRatio.VERTICAL
        )
    ]
    
    for i, context in enumerate(contexts):
        camera_angle = engine.select_camera_angle(context, 'opening')
        composition = engine.select_composition(context, 'opening') 
        movement = engine.select_camera_movement(context, 'opening')
        
        print(f"   Context {i+1}: {context.mood} ({context.intensity}) -> "
              f"Camera: {camera_angle}, Comp: {composition}, Move: {movement}")
        
        # 基本検証
        assert camera_angle in ['ELS', 'LS', 'MS', 'MCU', 'CU', 'ECU'], f"Invalid camera angle: {camera_angle}"
        assert movement is not None, "Movement selection failed"
        assert composition is not None, "Composition selection failed"
    
    print("   ✅ Intelligent selection test passed!")


def test_vertical_optimization():
    """縦型最適化のテスト"""
    print("\n📱 Testing Vertical Optimization...")
    
    context = SceneContext(
        emotional_phase=EmotionalPhase.A_MELO,
        intensity=0.5,
        pacing='medium',
        mood='peaceful',
        genre=VideoGenre.TOURISM,
        aspect_ratio=AspectRatio.VERTICAL
    )
    
    base_prompt = "medium shot, character looking at camera, rule of thirds composition, warm lighting, 16:9"
    optimized = VerticalOptimizer.optimize_for_vertical(base_prompt, 'rule_of_thirds', context)
    
    print(f"   Original: {base_prompt}")
    print(f"   Optimized: {optimized}")
    
    assert '9:16' in optimized, "Aspect ratio not changed to vertical"
    assert 'vertical' in optimized.lower(), "Vertical optimizations not applied"
    
    print("   ✅ Vertical optimization test passed!")


def test_emotional_engagement():
    """感情移入促進機能のテスト"""
    print("\n💝 Testing Emotional Engagement Enhancement...")
    
    context = SceneContext(
        emotional_phase=EmotionalPhase.SABI_HOOK,
        intensity=0.8,
        pacing='fast',
        mood='energetic',
        genre=VideoGenre.TOURISM,
        aspect_ratio=AspectRatio.VERTICAL
    )
    
    cut_data = {
        'duration': 8,
        'scene_description': 'Opening scene',
        'action': 'Character appears',
        'emotional_phase': EmotionalPhase.SABI_HOOK,
        'intensity': 0.8,
        'pacing': 'fast',
        'mood': 'energetic'
    }
    
    # 感情移入促進
    enhanced_cut = EmotionalEngagementEnhancer.enhance_emotional_connection(cut_data, context)
    
    print(f"   Enhanced with empathy hook: {enhanced_cut.get('empathy_hook', 'N/A')}")
    
    # 3層刺激
    stimulated_cut = EmotionalEngagementEnhancer.generate_three_layer_stimulation(enhanced_cut)
    stimulation = stimulated_cut.get('three_layer_stimulation', {})
    
    print(f"   Visual stimulation: {stimulation.get('visual', {}).get('movement', 'N/A')}")
    print(f"   Audio suggestion: {stimulation.get('auditory', {}).get('bgm_style', 'N/A')}")
    
    assert 'empathy_hook' in enhanced_cut, "Empathy hook not added"
    assert 'three_layer_stimulation' in stimulated_cut, "3-layer stimulation not added"
    
    print("   ✅ Emotional engagement test passed!")


def test_full_generation():
    """完全な生成プロセスのテスト"""
    print("\n🚀 Testing Full Enhanced Generation...")
    
    # 設定作成
    enhanced_config = {
        'aspect_ratio': AspectRatio.VERTICAL,
        'genre': VideoGenre.TOURISM,
        'emotional_structure': 'jpop',
        'intelligence_level': 'high',
        'empathy_enhancement': True,
        'three_layer_stimulation': True,
        'vertical_optimization': True,
        'title': 'Test Enhanced Storyboard',
        'duration': 30,
        'num_cuts': 6,
        'visual_style': 'photorealistic anime style'
    }
    
    # ジェネレーター初期化
    generator = EnhancedStoryboardGenerator(enhanced_config)
    
    # 入力データ
    input_data = {
        'story_description': '白浜の美しい観光地を紹介し、訪問者に魅力を伝える30秒縦型動画。朝から夜まで様々な魅力を4段階で紹介。',
        'visual_analysis': {
            'style': 'bright travel photography',
            'colors': ['#FFE4B5', '#87CEEB', '#32CD32'],
            'mood': 'welcoming and inspiring',
            'lighting': 'golden hour natural light'
        },
        'target_audience': 'young travelers'
    }
    
    # 生成実行
    storyboard = generator.generate_storyboard(input_data)
    
    print(f"   ✓ Generated storyboard with {storyboard.num_cuts} cuts")
    print(f"   ✓ Title: {storyboard.title}")
    print(f"   ✓ Duration: {storyboard.duration}s")
    
    # 各カットの検証
    for i, cut in enumerate(storyboard.cuts):
        print(f"   Cut {i+1}: {cut.camera_angle} | {cut.composition} | {cut.camera_movement}")
        
        # 基本検証
        assert cut.image_prompt is not None, f"Cut {i+1}: Image prompt missing"
        assert cut.veo3_prompt is not None, f"Cut {i+1}: Veo3 prompt missing"
        assert cut.sora2_prompt is not None, f"Cut {i+1}: Sora2 prompt missing"
        
        # 縦型指定の確認
        if '9:16' not in cut.image_prompt and 'vertical' not in cut.image_prompt:
            print(f"   Warning: Cut {i+1} may not be optimized for vertical")
    
    # スタイルガイドの確認
    style_guide = storyboard.style_guide
    print(f"   ✓ Style guide includes: {list(style_guide.keys())}")
    
    assert 'aspect_ratio' in style_guide, "Aspect ratio not in style guide"
    assert style_guide['aspect_ratio'] == '9:16', "Incorrect aspect ratio in style guide"
    
    print("   ✅ Full generation test passed!")
    
    return storyboard


def test_reference_integration():
    """リファレンス統合のテスト"""
    print("\n📚 Testing Reference Integration...")
    
    engine = IntelligentSelectionEngine()
    
    # ムード別選択の検証
    mood_tests = [
        ('peaceful', 'opening'),
        ('energetic', 'action'),
        ('tense', 'emotion'),
        ('dramatic', 'climax')
    ]
    
    for mood, scene_type in mood_tests:
        context = SceneContext(
            emotional_phase=EmotionalPhase.A_MELO,
            intensity=0.6,
            pacing='medium',
            mood=mood,
            genre=VideoGenre.TOURISM,
            aspect_ratio=AspectRatio.VERTICAL
        )
        
        camera = engine.select_camera_angle(context, scene_type)
        composition = engine.select_composition(context, scene_type)
        movement = engine.select_camera_movement(context, scene_type)
        
        # リファレンスマトリックスとの整合性確認
        if mood in engine.MOOD_CAMERA_MATRIX:
            expected_cameras = engine.MOOD_CAMERA_MATRIX[mood]['primary']
            if camera not in expected_cameras:
                print(f"   Note: {mood} -> {camera} (expected one of {expected_cameras})")
        
        print(f"   {mood} + {scene_type}: {camera} | {composition} | {movement}")
    
    print("   ✅ Reference integration test passed!")


def run_all_tests():
    """全テストの実行"""
    print("🧪 Enhanced Storyboard Generator Test Suite")
    print("=" * 60)
    
    try:
        # 個別機能テスト
        test_jpop_structure()
        test_intelligent_selection()
        test_vertical_optimization()
        test_emotional_engagement()
        test_reference_integration()
        
        # 統合テスト
        storyboard = test_full_generation()
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed! Enhanced system is working correctly.")
        print("\n📊 Generated Storyboard Summary:")
        print(f"   • Title: {storyboard.title}")
        print(f"   • Cuts: {storyboard.num_cuts}")
        print(f"   • Duration: {storyboard.duration}s") 
        print(f"   • Aspect Ratio: {storyboard.style_guide.get('aspect_ratio', 'N/A')}")
        print(f"   • Genre: {storyboard.style_guide.get('genre_optimization', 'N/A')}")
        print(f"   • Enhanced Features: {len(storyboard.style_guide.get('intelligence_features', {}))}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)