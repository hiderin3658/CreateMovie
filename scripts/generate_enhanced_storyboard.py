#!/usr/bin/env python3
"""
Enhanced Storyboard Generation Script
高度化システムを活用したストーリーボード生成

使用方法:
python scripts/generate_enhanced_storyboard.py --story "白浜の魅力を紹介する30秒動画" --genre tourism --vertical
"""

import argparse
import os
import sys
import json
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from core.video.enhanced_storyboard_generator import (
    EnhancedStoryboardGenerator, 
    VideoGenre, 
    AspectRatio
)
from core.base import GeneratorConfig


def create_enhanced_config(args):
    """コマンドライン引数から高度化設定を作成"""
    # 基本設定
    base_config = GeneratorConfig(
        title=args.title or "Enhanced Video Storyboard",
        duration=args.duration,
        num_cuts=args.num_cuts,
        visual_style=args.style
    )
    
    # 高度化設定
    enhanced_config = {
        'aspect_ratio': AspectRatio.VERTICAL if args.vertical else AspectRatio.HORIZONTAL,
        'genre': VideoGenre(args.genre),
        'emotional_structure': 'jpop',
        'intelligence_level': args.intelligence,
        'empathy_enhancement': args.empathy,
        'three_layer_stimulation': args.stimulation,
        'vertical_optimization': args.vertical,
        'title': base_config.title,
        'duration': base_config.duration,
        'num_cuts': base_config.num_cuts,
        'visual_style': base_config.visual_style
    }
    
    return enhanced_config


def analyze_visual_reference(reference_path):
    """ビジュアル参照の分析（オプション）"""
    if not reference_path or not Path(reference_path).exists():
        return None
    
    # 簡単な分析例（実際にはAIによる画像分析が必要）
    return {
        'style': 'photographic realism',
        'colors': ['#FFE4B5', '#87CEEB', '#32CD32'],
        'mood': 'bright and welcoming',
        'lighting': 'natural daylight',
        'texture': 'high detail'
    }


def generate_storyboard(args):
    """高度化ストーリーボード生成のメイン処理"""
    print("🚀 Enhanced AI Video Storyboard Generator")
    print("=" * 50)
    
    # 設定作成
    enhanced_config = create_enhanced_config(args)
    print(f"📱 Aspect Ratio: {enhanced_config['aspect_ratio'].value}")
    print(f"🎭 Genre: {enhanced_config['genre'].value}")
    print(f"🧠 Intelligence Level: {enhanced_config['intelligence_level']}")
    print(f"🎵 Emotional Structure: J-pop 4-phase")
    
    # ジェネレーター初期化
    generator = EnhancedStoryboardGenerator(enhanced_config)
    
    # 入力データ準備
    input_data = {
        'story_description': args.story,
        'visual_analysis': analyze_visual_reference(args.reference),
        'target_audience': args.audience
    }
    
    if args.reference:
        print(f"🖼️  Visual Reference: {args.reference}")
    
    # ストーリーボード生成
    print(f"\n📝 Story: {args.story}")
    storyboard = generator.generate_storyboard(input_data)
    
    # 保存
    output_dir = args.output or f"output/enhanced_{storyboard.title.lower().replace(' ', '_')}"
    generator.save_storyboard(storyboard, output_dir)
    
    # 統計表示
    print(f"\n📊 Generation Statistics:")
    print(f"   • Total Duration: {storyboard.duration}s")
    print(f"   • Number of Cuts: {storyboard.num_cuts}")
    print(f"   • Emotional Phases: 4 (J-pop structure)")
    print(f"   • Intelligence Features: {len([k for k, v in enhanced_config.items() if k.endswith('_enhancement') or k.endswith('_optimization') and v])}")
    
    # 各フェーズの情報
    phase_counts = {}
    for cut in storyboard.cuts:
        if hasattr(cut, 'emotional_phase') and cut.emotional_phase:
            phase = getattr(cut, 'emotional_phase', 'unknown')
            if hasattr(phase, 'value'):
                phase = phase.value
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
    
    if phase_counts:
        print(f"\n🎵 Emotional Phase Distribution:")
        for phase, count in phase_counts.items():
            print(f"   • {phase.replace('_', ' ').title()}: {count} cuts")
    
    # 高度機能の利用状況
    features_used = []
    if enhanced_config.get('empathy_enhancement'):
        features_used.append("Empathy Enhancement")
    if enhanced_config.get('three_layer_stimulation'):
        features_used.append("3-Layer Stimulation")
    if enhanced_config.get('vertical_optimization'):
        features_used.append("Vertical Optimization")
    if enhanced_config.get('intelligence_level') == 'high':
        features_used.append("High Intelligence Selection")
    
    if features_used:
        print(f"\n✨ Active Enhancement Features:")
        for feature in features_used:
            print(f"   • {feature}")
    
    return Path(output_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Enhanced AI Video Storyboard Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 縦型観光動画（デフォルト高度化）
  python scripts/generate_enhanced_storyboard.py --story "白浜の魅力を30秒で紹介" --genre tourism --vertical
  
  # 横型教育動画
  python scripts/generate_enhanced_storyboard.py --story "プログラミング基礎講座" --genre educational --duration 60
  
  # 商用動画（最大高度化）
  python scripts/generate_enhanced_storyboard.py --story "新製品の魅力" --genre commercial --intelligence high --empathy --stimulation
  
  # カスタム設定
  python scripts/generate_enhanced_storyboard.py --story "ドキュメンタリー" --genre documentary --cuts 10 --duration 90 --audience adult
        """
    )
    
    # 必須引数
    parser.add_argument('--story', required=True,
                       help='Story description for the storyboard')
    
    # ジャンル設定
    parser.add_argument('--genre', choices=['educational', 'commercial', 'narrative', 'documentary', 'tourism', 'music'],
                       default='tourism', help='Video genre (default: tourism)')
    
    # 基本設定
    parser.add_argument('--title', help='Custom title for the storyboard')
    parser.add_argument('--duration', type=int, default=30, help='Total duration in seconds (default: 30)')
    parser.add_argument('--cuts', dest='num_cuts', type=int, default=8, help='Number of cuts (default: 8)')
    parser.add_argument('--style', default='photorealistic anime style', help='Visual style description')
    
    # アスペクト比
    parser.add_argument('--vertical', action='store_true', help='Use vertical 9:16 aspect ratio (default: horizontal)')
    
    # 高度化機能
    parser.add_argument('--intelligence', choices=['low', 'medium', 'high'], default='high',
                       help='Intelligence level for smart selection (default: high)')
    parser.add_argument('--empathy', action='store_true', default=True,
                       help='Enable empathy enhancement features (default: enabled)')
    parser.add_argument('--stimulation', action='store_true', default=True,
                       help='Enable 3-layer stimulation system (default: enabled)')
    
    # その他
    parser.add_argument('--audience', default='general', help='Target audience (default: general)')
    parser.add_argument('--reference', help='Path to reference image for visual analysis')
    parser.add_argument('--output', help='Custom output directory')
    
    # 機能無効化オプション
    parser.add_argument('--no-empathy', dest='empathy', action='store_false',
                       help='Disable empathy enhancement')
    parser.add_argument('--no-stimulation', dest='stimulation', action='store_false',
                       help='Disable 3-layer stimulation')
    
    args = parser.parse_args()
    
    try:
        output_path = generate_storyboard(args)
        print(f"\n🎉 Success! Enhanced storyboard generated at:")
        print(f"   📁 {output_path.absolute()}")
        print(f"   📄 {output_path / 'storyboard_report.md'}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()