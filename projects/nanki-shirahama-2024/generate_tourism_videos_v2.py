#!/usr/bin/env python3
"""
南紀白浜観光プロモーション動画生成システム（コアシステム統合版）

コアシステム（CoreStoryboardGenerator）を使用し、
南紀白浜特有の制約をプラグインで実装

画像生成: Gemini 2.5 Flash Image (最大3枚の参照画像対応)

使用方法:
    # 基本
    python generate_tourism_videos_v2.py "白浜の観光体験を描いた30秒動画"

    # 参照画像1枚
    python generate_tourism_videos_v2.py "白浜旅行" --character-ref tourist.png

    # 参照画像複数枚（最大3枚）
    python generate_tourism_videos_v2.py "白浜旅行" --character-ref char1.png char2.png style.png
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.base import GeneratorConfig
from core.video import CoreStoryboardGenerator

# 南紀白浜プロジェクトのモジュール
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from plugins.shirahama_tourism_plugin import create_plugin
from material_manager import MaterialManager


class ShirahamaTourismVideoGenerator:
    """南紀白浜観光動画生成（コアシステム統合版）"""

    def __init__(
        self,
        story_description: str,
        duration: int = 30,
        num_videos: int = 4,
        character_reference: Optional[list] = None,
        output_dir: Optional[Path] = None
    ):
        """
        初期化

        Args:
            story_description: ストーリーの説明
            duration: 総時間（秒）
            num_videos: 動画本数
            character_reference: キャラクター参照画像リスト（最大3枚、Gemini 2.5 Flash Image仕様）
            output_dir: 出力ディレクトリ
        """
        self.story_description = story_description
        self.total_duration = duration
        self.num_videos = num_videos
        self.video_duration = duration // num_videos  # 各動画の時間
        # 参照画像は最大3枚に制限（Gemini 2.5 Flash Image の仕様）
        if character_reference:
            self.character_reference = character_reference[:3] if isinstance(character_reference, list) else [character_reference]
        else:
            self.character_reference = None
        self.project_dir = Path(__file__).parent
        self.output_dir = output_dir or self.project_dir / "generated_v2"

        # 素材マネージャー
        self.material_manager = MaterialManager(self.project_dir)

        # プラグイン
        self.tourism_plugin = create_plugin()

        print("=" * 70)
        print("南紀白浜観光プロモーション動画生成システム（コアシステム統合版）")
        print("=" * 70)
        print()

    def generate_all_videos(self):
        """全動画を生成"""
        # 素材ロード
        print("[Step 1/5] 素材検証")
        print("-" * 70)
        self._load_and_validate_materials()
        print()

        # 動画ごとに生成
        for video_id in range(1, self.num_videos + 1):
            print(f"[Step 2-4/5] Video {video_id}/{self.num_videos} 生成中...")
            print("-" * 70)
            self._generate_single_video(video_id)
            print()

        # サマリー
        print("[Step 5/5] 完了")
        print("-" * 70)
        self._print_summary()

    def _load_and_validate_materials(self):
        """素材ロードと検証"""
        materials = self.material_manager.load_materials()
        print(f"✓ {len(materials)} 枚の素材をロード")

        stats = self.material_manager.get_statistics()
        for category, info in stats['by_category'].items():
            print(f"  - {category}: {info['count']}枚")

        # 制約チェック
        warnings = self.material_manager.validate_constraints()
        if warnings:
            print("\n⚠️  警告:")
            for warning in warnings:
                print(f"  {warning}")

        # プラグインの制約表示
        print(f"\n[Plugin: {self.tourism_plugin.name}] 素材制約:")
        for key, value in self.tourism_plugin.material_constraints.items():
            print(f"  - {key}: {value}")

    def _generate_single_video(self, video_id: int):
        """単一動画を生成"""
        # ビデオ情報をロード（config.yamlから）
        video_config = self._load_video_config(video_id)

        # コアシステムのコンフィグ作成
        config = GeneratorConfig(
            duration=self.video_duration,
            num_cuts=video_config.get('cuts', 3),
            visual_style='anime',
            generate_images=False,  # 後で実装
            generate_music=False,   # 後で実装
            output_dir=str(self.output_dir / f"video{video_id}"),
            title=video_config['title']
        )

        # コア絵コンテジェネレーター作成
        generator = CoreStoryboardGenerator(config)

        # 南紀白浜プラグインを追加
        generator.add_plugin(self.tourism_plugin)

        print(f"  Video {video_id}: {video_config['title']}")
        print(f"  Theme: {video_config['theme']}")
        print(f"  Duration: {self.video_duration}秒")

        # ストーリー記述を構築
        story_input = {
            'story_description': self._build_story_for_video(video_id, video_config),
            'video_id': video_id,
            'theme': video_config['theme'],
            'mood': video_config['mood'],
            'categories': video_config.get('categories', []),
            'duration': self.video_duration
        }

        # キャラクター参照があれば追加
        if self.character_reference:
            # 複数の参照画像に対応
            story_input['reference_images'] = [str(ref) for ref in self.character_reference]
            # 後方互換性のため、最初の画像をkey_visual_pathにも設定
            story_input['key_visual_path'] = str(self.character_reference[0])

        # プラグイン: 事前処理
        story_input = generator.process_plugins(story_input, 'pre_generation')

        # コアシステムで絵コンテ生成
        print("  ⏳ 絵コンテ生成中...")
        storyboard = generator.generate_storyboard(story_input)

        # プラグイン: 事後処理（制約チェック）
        storyboard = generator.process_plugins(storyboard, 'post_generation')

        # プラグイン: バリデーション
        storyboard = generator.process_plugins(storyboard, 'validation')

        # 保存
        output_path = self.output_dir / f"video{video_id}"
        output_path.mkdir(parents=True, exist_ok=True)

        storyboard_file = output_path / "storyboard.json"
        generator.save_storyboard(storyboard, str(storyboard_file))

        print(f"  ✓ 絵コンテ保存: {storyboard_file}")

        # プラグインの警告があれば表示
        if 'plugin_warnings' in storyboard:
            print(f"  ⚠️  {len(storyboard['plugin_warnings'])} 件の警告")
            for warning in storyboard['plugin_warnings'][:3]:  # 最初の3件のみ
                print(f"      {warning}")

        # I2Vプロンプト生成（簡易版）
        self._generate_i2v_prompts(video_id, storyboard, output_path)

    def _load_video_config(self, video_id: int) -> dict:
        """config.yamlから動画設定をロード"""
        import yaml
        config_file = self.project_dir / "config.yaml"

        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        video_key = f"video{video_id}"
        return config['story_structure']['videos'][video_key]

    def _build_story_for_video(self, video_id: int, video_config: dict) -> str:
        """動画用のストーリー記述を構築"""
        story = f"""
        {self.story_description}

        Video {video_id}: {video_config['title']}
        テーマ: {video_config['theme']}
        ムード: {video_config['mood']}
        時間: {self.video_duration}秒

        この動画では、{video_config['title']}をテーマに、
        白浜の魅力を{self.video_duration}秒で表現します。

        使用する素材カテゴリ: {', '.join(video_config.get('categories', []))}
        """
        return story.strip()

    def _generate_i2v_prompts(self, video_id: int, storyboard: dict, output_path: Path):
        """I2Vプロンプト生成（簡易版）"""
        prompts = []

        for cut in storyboard.get('cuts', []):
            prompt = {
                'cut_number': cut['cut_number'],
                'duration': cut['duration'],
                'scene': cut['scene_description'],
                'camera': f"{cut['camera_angle']} / {cut['camera_movement']}",
                'runway_prompt': cut.get('video_prompt', ''),
                'constraints': self.tourism_plugin.generate_i2v_constraints_note()
            }
            prompts.append(prompt)

        # 保存
        import json
        prompts_file = output_path / "i2v_prompts.json"
        with open(prompts_file, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)

        print(f"  ✓ I2Vプロンプト保存: {prompts_file}")

    def _print_summary(self):
        """サマリー表示"""
        print("✓ 全動画の生成が完了しました")
        print()
        print(f"出力ディレクトリ: {self.output_dir}")
        print()
        print("次のステップ:")
        print("  1. generated_v2/ の絵コンテ(storyboard.json)を確認")
        print("  2. i2v_prompts.json を参照して Runway Gen-3 で動画化")
        print("  3. 素材制約（Scale/Crop のみ）を厳守してください")
        print()

        # 素材使用率
        stats = self.material_manager.get_statistics()
        usage = stats['usage_rate']
        print(f"素材使用率: {usage['rate']} ({usage['used']}/{usage['total']})")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="南紀白浜観光プロモーション動画生成（コアシステム統合版）"
    )
    parser.add_argument(
        'story',
        type=str,
        help='ストーリーの説明（例: "白浜の観光体験"）'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=30,
        help='総時間（秒）。デフォルト: 30'
    )
    parser.add_argument(
        '--num-videos',
        type=int,
        default=4,
        help='動画本数。デフォルト: 4'
    )
    parser.add_argument(
        '--character-ref',
        type=str,
        nargs='+',
        help='キャラクター参照画像のパス（最大3枚、Gemini 2.5 Flash Image仕様）'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='出力ディレクトリ'
    )

    args = parser.parse_args()

    # 参照画像をPathオブジェクトのリストに変換
    character_ref = None
    if args.character_ref:
        character_ref = [Path(ref) for ref in args.character_ref]
        if len(character_ref) > 3:
            print(f"⚠️  警告: 参照画像が{len(character_ref)}枚指定されていますが、最大3枚まで使用されます（Gemini 2.5 Flash Image仕様）")

    output_dir = Path(args.output) if args.output else None

    try:
        generator = ShirahamaTourismVideoGenerator(
            story_description=args.story,
            duration=args.duration,
            num_videos=args.num_videos,
            character_reference=character_ref,
            output_dir=output_dir
        )

        generator.generate_all_videos()

        print()
        print("=" * 70)
        print("✓ Success!")
        print("=" * 70)

    except Exception as e:
        print()
        print("=" * 70)
        print(f"✗ Error: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
