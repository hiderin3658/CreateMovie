#!/usr/bin/env python3
"""
Generic Material Management System
Supports multiple project types with pluggable strategies
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class Material:
    """素材データクラス（汎用）"""
    # 識別情報
    id: str
    filename: str
    path: str
    category: str

    # 基本情報
    width: int
    height: int
    file_size: int

    # AI解析結果
    description: str
    main_subject: str
    location: Optional[str] = None
    time_of_day: Optional[str] = None
    weather: Optional[str] = None
    color_tone: Optional[str] = None
    composition: Optional[str] = None

    # 使用状況
    assigned_to: Optional[int] = None
    match_score: float = 0.0

    # 品質指標
    quality_score: float = 0.0
    is_hd: bool = False

    @property
    def aspect_ratio(self) -> float:
        """アスペクト比を計算"""
        return self.width / self.height if self.height > 0 else 1.0

    @classmethod
    def from_dict(cls, data: Dict, materials_root: Path) -> 'Material':
        """辞書からMaterialオブジェクトを作成"""
        # パスの構築
        category = data.get('category', 'unknown')
        filename = data['filename']

        # パスの優先順位: data['path'] > 自動構築
        if 'path' in data and data['path']:
            file_path = str(data['path'])
        else:
            file_path = str(materials_root / "raw" / category / filename)

        # is_hd の判定
        width = data.get('width', 0)
        height = data.get('height', 0)
        is_hd = width >= 1920 or height >= 1080

        return cls(
            id=data.get('id', f"{category}_{Path(filename).stem}"),
            filename=filename,
            path=file_path,
            category=category,
            width=width,
            height=height,
            file_size=data.get('file_size', 0),
            description=data.get('description', ''),
            main_subject=data.get('main_subject', ''),
            location=data.get('location'),
            time_of_day=data.get('time_of_day'),
            weather=data.get('weather'),
            color_tone=data.get('color_tone'),
            composition=data.get('composition'),
            assigned_to=data.get('assigned_to'),
            match_score=data.get('match_score', 0.0),
            quality_score=data.get('quality_score', 0.0),
            is_hd=is_hd
        )

    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        return asdict(self)


@dataclass
class MaterialConfig:
    """素材管理の設定"""
    project_root: Path
    project_type: str  # "tourism", "education", "marketing", "competition", "custom"
    categories: List[str]  # プロジェクト固有のカテゴリ
    usage_requirements: Dict[str, Any]  # 使用要件
    constraints: Dict[str, bool]  # 制約（変形禁止など）
    scoring_weights: Dict[str, float]  # スコアリングの重み

    @classmethod
    def from_yaml(cls, config_path: Path) -> 'MaterialConfig':
        """プロジェクト設定ファイルから読み込み"""
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # プロジェクトタイプ
        project_type = data.get('project', {}).get('type', 'custom')

        # カテゴリ（複数の形式に対応）
        requirements = data.get('requirements', {})
        materials_config = requirements.get('materials', {})

        # categories の取得（dict形式 or list形式に対応）
        categories_data = materials_config.get('categories', [])
        if isinstance(categories_data, dict):
            # dict形式 {"beach": "4-5", "nature": "4-5"} → ["beach", "nature"]
            categories = list(categories_data.keys())
        elif isinstance(categories_data, list):
            # list形式 ["beach", "nature", ...]
            categories = categories_data
        else:
            categories = []

        # 使用要件
        usage_requirements = materials_config.get('usage_requirements', {})

        # 制約
        constraints = materials_config.get('constraints', {})

        # スコアリング重み（カスタム or デフォルト）
        scoring_weights = data.get('material_scoring_weights', cls._default_weights())

        return cls(
            project_root=config_path.parent,
            project_type=project_type,
            categories=categories,
            usage_requirements=usage_requirements,
            constraints=constraints,
            scoring_weights=scoring_weights
        )

    @staticmethod
    def _default_weights() -> Dict[str, float]:
        """デフォルトのスコアリング重み"""
        return {
            'keyword_match': 5.0,
            'category_match': 3.0,
            'time_match': 2.0,
            'mood_match': 2.0,
            'quality_bonus': 1.0,
            'unused_bonus': 0.5
        }


class MaterialSystem:
    """汎用素材管理システム"""

    def __init__(self, config: MaterialConfig):
        """
        Initialize material system

        Args:
            config: Material configuration
        """
        self.config = config
        self.materials_root = config.project_root / "source_materials"

        # コンポーネント初期化（後で実装）
        from .material_analyzer import MaterialAnalyzer
        from .material_matcher import MaterialMatcher
        from .usage_tracker import UsageTracker

        self.analyzer = MaterialAnalyzer(self.config)
        self.matcher = MaterialMatcher(self.config)
        self.tracker = UsageTracker(self.config)

        # ストラテジー選択
        self.strategy = self._select_strategy()

        # 素材リスト
        self.materials: List[Material] = []

    def _select_strategy(self) -> 'MaterialMatchingStrategy':
        """プロジェクトタイプに応じたストラテジー選択"""
        from .matching_strategies import (
            TourismMatchingStrategy,
            EducationMatchingStrategy,
            MarketingMatchingStrategy,
            CompetitionMatchingStrategy,
            DefaultMatchingStrategy
        )

        strategies = {
            'tourism': TourismMatchingStrategy,
            'education': EducationMatchingStrategy,
            'marketing': MarketingMatchingStrategy,
            'competition': CompetitionMatchingStrategy
        }

        strategy_class = strategies.get(
            self.config.project_type,
            DefaultMatchingStrategy
        )

        return strategy_class(self.config)

    def load_materials(self) -> List[Material]:
        """素材を読み込む"""
        # メタデータファイルから読み込み
        metadata_file = self.materials_root / "metadata" / "photo_descriptions.yaml"

        if metadata_file.exists():
            print(f"📂 Loading materials from metadata: {metadata_file}")
            self.materials = self._load_from_metadata(metadata_file)
        else:
            # メタデータがない場合は自動解析
            print("📸 Metadata not found. Analyzing materials...")
            self.materials = self.analyzer.analyze_all_materials(self.materials_root)

        # カテゴリ別にインデックス
        self.matcher.index_materials(self.materials)

        print(f"✅ Loaded {len(self.materials)} materials")
        return self.materials

    def _load_from_metadata(self, metadata_file: Path) -> List[Material]:
        """メタデータファイルから素材を読み込む"""
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        materials = []
        for item in data.get('photos', []):
            material = Material.from_dict(item, self.materials_root)
            materials.append(material)

        return materials

    def map_to_storyboard(
        self,
        storyboard: Dict,
        allow_generation: bool = True
    ) -> Dict:
        """
        ストーリーボードに素材をマッピング

        Args:
            storyboard: ストーリーボードデータ
            allow_generation: 素材がない場合のAI生成を許可

        Returns:
            素材がマッピングされたストーリーボード
        """
        print("\n🎯 Mapping materials to storyboard...")

        mapped_storyboard = storyboard.copy()

        for i, cut in enumerate(mapped_storyboard['cuts'], 1):
            print(f"  Cut {i}:", end=" ")

            # ストラテジーを使ってマッチング
            best_material = self.strategy.find_best_match(
                cut=cut,
                materials=self.materials,
                matcher=self.matcher
            )

            if best_material:
                # 素材を割り当て
                cut['source_material'] = {
                    'filename': best_material.filename,
                    'path': best_material.path,
                    'category': best_material.category,
                    'confidence': best_material.match_score
                }
                cut['generation_required'] = False

                # 使用を追跡
                self.tracker.mark_used(best_material.id, cut_number=i)

                print(f"✓ {best_material.filename} (score: {best_material.match_score:.1f})")

            else:
                # 素材が見つからない
                if allow_generation:
                    cut['generation_required'] = True
                    cut['generation_prompt'] = self._create_generation_prompt(cut)
                    print("⚠️ No match, requires AI generation")
                else:
                    raise ValueError(f"No suitable material found for cut {i}")

        # 使用率を計算
        usage_stats = self.tracker.calculate_usage_rate(self.materials)
        mapped_storyboard['material_usage'] = usage_stats

        print(f"\n📊 Material usage: {usage_stats['percentage']}")

        return mapped_storyboard

    def _create_generation_prompt(self, cut: Dict) -> str:
        """素材生成用のプロンプトを作成"""
        return f"""
Generate an image for this scene:
- Description: {cut.get('scene_description', '')}
- Mood: {cut.get('mood', '')}
- Time: {cut.get('time_of_day', '')}
- Camera: {cut.get('camera_angle', '')}
- Style: {self.config.project_type}
"""

    def generate_report(self, output_path: Optional[Path] = None) -> Dict:
        """使用レポートを生成"""
        print("\n📋 Generating usage report...")

        report = self.tracker.generate_detailed_report(self.materials)

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Report saved to: {output_path}")

        return report

    def validate_requirements(self) -> Dict[str, Any]:
        """プロジェクト要件を検証"""
        print("\n✅ Validating requirements...")

        validation = {
            'valid': True,
            'errors': [],
            'warnings': []
        }

        # 最小使用率チェック
        min_usage = self.config.usage_requirements.get('minimum_usage_rate', 0.0)
        usage_stats = self.tracker.calculate_usage_rate(self.materials)
        current_usage = usage_stats['rate']

        if current_usage < min_usage:
            error_msg = (
                f"Usage rate {current_usage:.1%} below requirement {min_usage:.1%}"
            )
            validation['errors'].append(error_msg)
            validation['valid'] = False
            print(f"  ❌ {error_msg}")
        else:
            print(f"  ✓ Usage rate {current_usage:.1%} meets requirement {min_usage:.1%}")

        # カテゴリ別の使用チェック
        category_usage = self.tracker.get_category_usage(self.materials)
        for category in self.config.categories:
            if category not in category_usage or category_usage[category] == 0:
                warning_msg = f"No materials used from category: {category}"
                validation['warnings'].append(warning_msg)
                print(f"  ⚠️ {warning_msg}")

        return validation


def main():
    """CLI usage example"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generic Material Management System"
    )
    parser.add_argument(
        '--config',
        required=True,
        help='Project config.yaml path'
    )
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze materials (force re-analysis)'
    )

    args = parser.parse_args()

    # Load configuration
    config = MaterialConfig.from_yaml(Path(args.config))

    # Initialize system
    system = MaterialSystem(config)

    # Load or analyze materials
    if args.analyze:
        # Force re-analysis
        metadata_file = system.materials_root / "metadata" / "photo_descriptions.yaml"
        if metadata_file.exists():
            metadata_file.unlink()
        system.load_materials()
    else:
        system.load_materials()

    # Generate report
    report_path = system.materials_root / "analyzed" / "material_analysis.json"
    system.generate_report(report_path)

    print("\n✅ Material management complete!")


if __name__ == "__main__":
    main()
