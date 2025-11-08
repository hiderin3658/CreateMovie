#!/usr/bin/env python3
"""
南紀白浜観光プロモーション動画生成システム - 統合実行スクリプト

素材から物語→絵コンテ→動画プロンプトまでを一括生成
制約: 素材の拡大/縮小のみ許可、形状変更は禁止

使用方法:
    python generate_tourism_videos.py
    python generate_tourism_videos.py --stories-only  # 物語生成のみ
    python generate_tourism_videos.py --from-storyboard  # 絵コンテからのみ
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Optional

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from material_manager import MaterialManager
from story_generator import StoryGenerator, VideoStory
from storyboard_generator import StoryboardGenerator, Storyboard
from video_prompt_generator import VideoPromptGenerator


class TourismVideoGenerator:
    """観光動画生成統合クラス"""

    def __init__(self, project_root: Path, api_key: Optional[str] = None):
        self.project_root = Path(project_root)
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is required. "
                "Set it via environment variable or .env file"
            )

        # 各コンポーネントの初期化
        self.material_manager = MaterialManager(project_root)
        self.story_generator = StoryGenerator(project_root, self.api_key)
        self.storyboard_generator = StoryboardGenerator(project_root, self.api_key)
        self.prompt_generator = VideoPromptGenerator(project_root)

        # 出力ディレクトリ
        self.output_dir = self.project_root / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_full_pipeline(self):
        """フルパイプライン実行"""
        print("=" * 60)
        print("南紀白浜観光プロモーション動画生成システム")
        print("=" * 60)
        print()

        # Step 1: 素材検証
        print("[Step 1/4] 素材検証")
        print("-" * 60)
        self._validate_materials()
        print()

        # Step 2: 物語生成
        print("[Step 2/4] 物語生成（Gemini API）")
        print("-" * 60)
        stories = self._generate_stories()
        print()

        # Step 3: 絵コンテ生成
        print("[Step 3/4] 絵コンテ生成（Gemini API）")
        print("-" * 60)
        storyboards = self._generate_storyboards(stories)
        print()

        # Step 4: 動画プロンプト生成
        print("[Step 4/4] 動画プロンプト生成（I2V用）")
        print("-" * 60)
        self._generate_video_prompts(storyboards)
        print()

        # サマリー
        self._print_summary(stories, storyboards)

    def _validate_materials(self):
        """素材検証"""
        print("Loading materials...")
        materials = self.material_manager.load_materials()
        print(f"✓ Loaded {len(materials)} materials")

        # 統計表示
        stats = self.material_manager.get_statistics()
        print(f"  - Beach: {stats['by_category']['beach']['count']}")
        print(f"  - Nature: {stats['by_category']['nature']['count']}")
        print(f"  - Attractions: {stats['by_category']['attractions']['count']}")
        print(f"  - Culture: {stats['by_category']['culture']['count']}")
        print(f"  - HD quality: {stats['hd_percentage']}")

        # 制約チェック
        warnings = self.material_manager.validate_constraints()
        if warnings:
            print("\n⚠️  Warnings:")
            for warning in warnings:
                print(f"  {warning}")
        else:
            print("✓ All material constraints satisfied")

    def _generate_stories(self) -> list[VideoStory]:
        """物語生成"""
        print("Generating 4 tourism stories with Gemini API...")
        print("This may take 30-60 seconds...")

        stories = self.story_generator.generate_four_stories()

        print(f"✓ Generated {len(stories)} stories:")
        for story in stories:
            print(f"  - Video {story.video_id}: {story.title} ({story.duration}s, {len(story.cuts)} cuts)")

        # 保存
        self.story_generator.save_stories(stories)

        # レポート生成
        report = self.story_generator.generate_story_report(stories)
        report_path = self.output_dir / "stories" / "story_report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ Story report: {report_path}")

        return stories

    def _generate_storyboards(self, stories: list[VideoStory]) -> list[Storyboard]:
        """絵コンテ生成"""
        storyboards = []

        for i, story in enumerate(stories, 1):
            print(f"[{i}/{len(stories)}] Generating storyboard for: {story.title}")

            storyboard = self.storyboard_generator.generate_storyboard_from_story(story)
            storyboards.append(storyboard)

            # 保存
            self.storyboard_generator.save_storyboard(storyboard)

            # レポート
            report = self.storyboard_generator.generate_storyboard_report(storyboard)
            report_path = (
                self.output_dir / "storyboards" /
                f"video{storyboard.video_id}_report.md"
            )
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)

            print(f"  ✓ {storyboard.total_cuts} cuts, {len(storyboard.materials_used)} materials")

        print(f"✓ All storyboards generated")
        return storyboards

    def _generate_video_prompts(self, storyboards: list[Storyboard]):
        """動画プロンプト生成"""
        for i, storyboard in enumerate(storyboards, 1):
            print(f"[{i}/{len(storyboards)}] Generating I2V prompts for: {storyboard.title}")

            prompt_set = self.prompt_generator.generate_prompts_from_storyboard(storyboard)

            # 保存
            self.prompt_generator.save_prompts(prompt_set)

            # ガイド
            guide = self.prompt_generator.generate_prompt_guide(prompt_set)
            guide_path = (
                self.output_dir / "video_prompts" /
                f"video{prompt_set.video_id}_prompt_guide.md"
            )
            guide_path.parent.mkdir(parents=True, exist_ok=True)
            with open(guide_path, 'w', encoding='utf-8') as f:
                f.write(guide)

            print(f"  ✓ {len(prompt_set.prompts)} prompts (Runway, Pika, General)")

        print(f"✓ All I2V prompts generated")

    def _print_summary(self, stories: list[VideoStory], storyboards: list[Storyboard]):
        """サマリー表示"""
        print("=" * 60)
        print("生成完了")
        print("=" * 60)
        print()
        print(f"✓ 4本の観光プロモーション動画の準備が完了しました")
        print()

        for i, (story, storyboard) in enumerate(zip(stories, storyboards), 1):
            print(f"Video {i}: {story.title}")
            print(f"  - 時間: {story.duration}秒")
            print(f"  - カット数: {storyboard.total_cuts}")
            print(f"  - 使用素材: {len(storyboard.materials_used)}枚")
            print()

        print("出力ファイル:")
        print(f"  - ストーリー: {self.output_dir}/stories/")
        print(f"  - 絵コンテ: {self.output_dir}/storyboards/")
        print(f"  - 動画プロンプト: {self.output_dir}/video_prompts/")
        print()

        print("次のステップ:")
        print("  1. generated/video_prompts/ のプロンプトガイドを確認")
        print("  2. Runway Gen-3 または Pika Labs で各カットを動画化")
        print("  3. 生成された動画を編集ソフトで結合")
        print("  4. Suno AI で BGM を生成して追加")
        print()

        # 素材使用率
        stats = self.material_manager.get_statistics()
        usage = stats['usage_rate']
        print(f"素材使用率: {usage['rate']} ({usage['used']}/{usage['total']})")
        if float(usage['rate'].rstrip('%')) >= 75:
            print("✓ コンペ要件（75%以上）を満たしています")
        else:
            print("⚠️  素材使用率が75%未満です")

    def generate_stories_only(self):
        """物語生成のみ"""
        print("物語生成モード")
        print("-" * 60)
        self._validate_materials()
        print()
        self._generate_stories()

    def generate_from_stories(self):
        """既存のストーリーから絵コンテとプロンプトを生成"""
        print("絵コンテ・プロンプト生成モード")
        print("-" * 60)

        # ストーリー読み込み
        stories_file = self.output_dir / "stories" / "stories.json"
        if not stories_file.exists():
            print(f"✗ Stories file not found: {stories_file}")
            print("  Please run with --stories-only first")
            sys.exit(1)

        with open(stories_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        stories = []
        for video_data in data['videos']:
            story = VideoStory(**video_data)
            stories.append(story)

        print(f"✓ Loaded {len(stories)} stories")
        print()

        # 絵コンテ生成
        storyboards = self._generate_storyboards(stories)
        print()

        # プロンプト生成
        self._generate_video_prompts(storyboards)
        print()

        self._print_summary(stories, storyboards)


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="南紀白浜観光プロモーション動画生成システム"
    )
    parser.add_argument(
        '--stories-only',
        action='store_true',
        help='物語生成のみを実行'
    )
    parser.add_argument(
        '--from-stories',
        action='store_true',
        help='既存のストーリーから絵コンテとプロンプトを生成'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='Gemini API key (or set GEMINI_API_KEY env var)'
    )

    args = parser.parse_args()

    try:
        generator = TourismVideoGenerator(project_root, args.api_key)

        if args.stories_only:
            generator.generate_stories_only()
        elif args.from_stories:
            generator.generate_from_stories()
        else:
            generator.run_full_pipeline()

        print()
        print("=" * 60)
        print("✓ Success!")
        print("=" * 60)

    except Exception as e:
        print()
        print("=" * 60)
        print(f"✗ Error: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
