#!/usr/bin/env python3
"""
Claude Skills Enhanced Storyboard Generation Script
Claude Skills前提の統合実行スクリプト

使用方法:
python scripts/generate_skills_storyboard.py --project nanki-shirahama-2024 --story "白浜の魅力紹介"
"""

import argparse
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from core.video.claude_skills_enhanced_generator import CloudeSkillsEnhancedGenerator
    SKILLS_AVAILABLE = True
except ImportError:
    print("⚠️  Claude Skills enhanced generator not available, falling back to basic enhanced generator")
    from core.video.enhanced_storyboard_generator import EnhancedStoryboardGenerator, VideoGenre, AspectRatio
    SKILLS_AVAILABLE = False


def main():
    parser = argparse.ArgumentParser(
        description="Claude Skills Enhanced AI Video Storyboard Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Claude Skills統合例:
  # 白浜プロジェクト（設定自動読込）
  python scripts/generate_skills_storyboard.py --project nanki-shirahama-2024
  
  # カスタムストーリー指定
  python scripts/generate_skills_storyboard.py --project nanki-shirahama-2024 --story "新しい白浜の魅力"
  
  # 他のプロジェクト
  python scripts/generate_skills_storyboard.py --project your-project --config path/to/config.yaml
        """
    )
    
    # Claude Skills対応引数
    parser.add_argument('--project', default='nanki-shirahama-2024',
                       help='Project ID (matches config.yaml project.id)')
    parser.add_argument('--config', 
                       help='Path to project config.yaml file')
    parser.add_argument('--story', 
                       help='Story description (overrides config if provided)')
    
    # 基本引数
    parser.add_argument('--output', help='Custom output directory')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Preview configuration without generation')
    
    # デバッグ・詳細オプション
    parser.add_argument('--verbose', action='store_true', 
                       help='Verbose output with detailed steps')
    parser.add_argument('--skills-info', action='store_true',
                       help='Show Claude Skills integration information')
    
    args = parser.parse_args()
    
    if args.skills_info:
        show_skills_info()
        return
    
    try:
        generate_with_skills(args)
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def show_skills_info():
    """Claude Skills統合情報表示"""
    print("🎨 Claude Skills Enhanced Storyboard Generator")
    print("=" * 60)
    print(f"Skills Integration: {'✅ Active' if SKILLS_AVAILABLE else '❌ Fallback mode'}")
    
    if SKILLS_AVAILABLE:
        print("\n🔧 Integrated Features:")
        print("  • Hook system (pre/post generation)")
        print("  • Plugin architecture")
        print("  • Workflow management (5-phase)")
        print("  • Project config.yaml integration")
        print("  • Material management system")
        print("  • Character consistency tracking")
        
        print("\n📁 Supported Projects:")
        projects_dir = Path("projects")
        if projects_dir.exists():
            for project_dir in projects_dir.iterdir():
                if project_dir.is_dir() and (project_dir / "config.yaml").exists():
                    print(f"  • {project_dir.name}")
        else:
            print("  • No project directories found")
        
        print("\n🔗 Available Plugins:")
        print("  • material_analyzer")
        print("  • anime_style_transfer") 
        print("  • character_consistency_checker")
        print("  • tourism_narrative_builder")
    
    else:
        print("\n⚠️  Fallback Mode:")
        print("  Using basic enhanced generator without Skills integration")
        print("  To enable Skills: install dependencies and check imports")


def generate_with_skills(args):
    """Claude Skills統合生成実行"""
    print("🚀 Claude Skills Enhanced Generation")
    print("=" * 50)
    
    # 設定パス解決
    config_path = args.config
    if not config_path:
        config_path = f"projects/{args.project}/config.yaml"
    
    if args.verbose:
        print(f"📋 Configuration:")
        print(f"  Project ID: {args.project}")
        print(f"  Config path: {config_path}")
        print(f"  Skills mode: {SKILLS_AVAILABLE}")
    
    # ジェネレーター初期化
    if SKILLS_AVAILABLE:
        generator = CloudeSkillsEnhancedGenerator(config_path)
        print(f"✅ Claude Skills generator initialized")
    else:
        # フォールバック：基本高度化ジェネレーター
        enhanced_config = {
            'aspect_ratio': AspectRatio.VERTICAL,
            'genre': VideoGenre.TOURISM,
            'intelligence_level': 'high',
            'empathy_enhancement': True,
            'three_layer_stimulation': True,
            'vertical_optimization': True,
            'title': f'{args.project} Storyboard',
            'duration': 30,
            'num_cuts': 8
        }
        generator = EnhancedStoryboardGenerator(enhanced_config)
        print(f"⚠️  Using fallback enhanced generator")
    
    # 入力データ準備
    input_data = {
        'project_id': args.project,
        'story_description': args.story or f"{args.project} promotional video showcasing key attractions and experiences",
        'target_audience': 'young travelers',
        'platform': 'social_media_shorts'
    }
    
    if args.verbose:
        print(f"\n📝 Input Data:")
        for key, value in input_data.items():
            print(f"  {key}: {value}")
    
    if args.dry_run:
        print(f"\n🔍 Dry Run - Configuration Preview:")
        print(f"  Would generate storyboard with above configuration")
        print(f"  Skills features: {'enabled' if SKILLS_AVAILABLE else 'disabled'}")
        return
    
    # 生成実行
    print(f"\n🎬 Generating storyboard...")
    storyboard = generator.generate_storyboard(input_data)
    
    # 出力
    output_dir = args.output or f"output/skills_{args.project}"
    generator.save_storyboard(storyboard, output_dir)
    
    # 結果サマリー
    print(f"\n📊 Generation Results:")
    print(f"   Project: {args.project}")
    print(f"   Duration: {storyboard.duration}s")
    print(f"   Cuts: {storyboard.num_cuts}")
    
    if SKILLS_AVAILABLE and hasattr(storyboard, 'claude_skills_metadata'):
        metadata = getattr(storyboard, 'claude_skills_metadata', {})
        if metadata:
            print(f"   Skills version: {metadata.get('skills_version', 'N/A')}")
            print(f"   Plugins used: {len(metadata.get('plugins_used', []))}")
    
    # 出力パス表示
    output_path = Path(output_dir)
    print(f"\n🎉 Success! Output saved to:")
    print(f"   📁 {output_path.absolute()}")
    if (output_path / 'storyboard_report.md').exists():
        print(f"   📄 {output_path / 'storyboard_report.md'}")


if __name__ == "__main__":
    main()