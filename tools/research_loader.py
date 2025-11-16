#!/usr/bin/env python3
"""
Research Data Loader and Query System
Loads structured research data (locations, story frameworks, etc.) for story generation
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class Location:
    """ロケーション情報"""
    id: str
    name: str
    category: str
    type: str
    core_narrative: str
    storytelling_theme: str
    key_features: List[str]
    visual_elements: Dict[str, Any]
    filming_tips: Dict[str, Any]
    logistics: Optional[Dict[str, Any]] = None
    narrative_role: Optional[str] = None
    distinction: Optional[str] = None
    brand_identity: Optional[str] = None
    slogan: Optional[str] = None
    spiritual_value: Optional[str] = None
    historical_depth: Optional[str] = None
    symbolism: Optional[str] = None
    historical_legend: Optional[str] = None
    metaphor: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Location':
        """辞書からLocationオブジェクトを作成"""
        return cls(
            id=data['id'],
            name=data['name'],
            category=data['category'],
            type=data['type'],
            core_narrative=data['core_narrative'],
            storytelling_theme=data['storytelling_theme'],
            key_features=data['key_features'],
            visual_elements=data['visual_elements'],
            filming_tips=data['filming_tips'],
            logistics=data.get('logistics'),
            narrative_role=data.get('narrative_role'),
            distinction=data.get('distinction'),
            brand_identity=data.get('brand_identity'),
            slogan=data.get('slogan'),
            spiritual_value=data.get('spiritual_value'),
            historical_depth=data.get('historical_depth'),
            symbolism=data.get('symbolism'),
            historical_legend=data.get('historical_legend'),
            metaphor=data.get('metaphor')
        )


@dataclass
class StoryFramework:
    """ストーリーフレームワーク"""
    name: str
    theme: str
    target_audience: str
    structure: Optional[Any] = None
    timeline: Optional[List[Dict]] = None
    sensory_mapping: Optional[Dict] = None

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> 'StoryFramework':
        """辞書からStoryFrameworkオブジェクトを作成"""
        return cls(
            name=data['name'],
            theme=data['theme'],
            target_audience=data['target_audience'],
            structure=data.get('structure'),
            timeline=data.get('timeline'),
            sensory_mapping=data.get('sensory_mapping')
        )


class ResearchDatabase:
    """リサーチデータベース"""

    def __init__(self, yaml_path: Path):
        """
        Initialize research database

        Args:
            yaml_path: Path to research YAML file
        """
        self.yaml_path = yaml_path
        self.data = self._load_yaml()

        # プロジェクト情報
        self.project = self.data.get('project', {})

        # ロケーション情報
        self.locations: Dict[str, Location] = {}
        for loc_data in self.data.get('locations', []):
            location = Location.from_dict(loc_data)
            self.locations[location.id] = location

        # ストーリーフレームワーク
        self.story_frameworks: Dict[str, StoryFramework] = {}
        for fw_key, fw_data in self.data.get('story_frameworks', {}).items():
            framework = StoryFramework.from_dict(fw_key, fw_data)
            self.story_frameworks[fw_key] = framework

        # ナラティブフレーズ
        self.narrative_phrases = self.data.get('narrative_phrases', {})

        # 撮影サマリー
        self.filming_summary = self.data.get('filming_summary', {})

    def _load_yaml(self) -> Dict:
        """YAMLファイルを読み込み"""
        with open(self.yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_location(self, location_id: str) -> Optional[Location]:
        """IDでロケーションを取得"""
        return self.locations.get(location_id)

    def get_location_by_name(self, name: str) -> Optional[Location]:
        """名前でロケーションを取得"""
        for location in self.locations.values():
            if location.name == name:
                return location
        return None

    def search_locations(
        self,
        category: Optional[str] = None,
        location_type: Optional[str] = None,
        keywords: Optional[List[str]] = None
    ) -> List[Location]:
        """
        ロケーションを検索

        Args:
            category: カテゴリでフィルタ (attractions, culture, beach, nature)
            location_type: タイプでフィルタ (露天風呂, ビーチ, etc.)
            keywords: キーワードで検索

        Returns:
            マッチしたロケーションのリスト
        """
        results = []

        for location in self.locations.values():
            # カテゴリフィルタ
            if category and location.category != category:
                continue

            # タイプフィルタ
            if location_type and location.type != location_type:
                continue

            # キーワード検索
            if keywords:
                text = f"{location.name} {location.core_narrative} {location.storytelling_theme}"
                text += f" {' '.join(location.key_features)}"
                text = text.lower()

                if not all(kw.lower() in text for kw in keywords):
                    continue

            results.append(location)

        return results

    def get_locations_by_category(self, category: str) -> List[Location]:
        """カテゴリ別にロケーションを取得"""
        return self.search_locations(category=category)

    def get_story_framework(self, framework_key: str) -> Optional[StoryFramework]:
        """ストーリーフレームワークを取得"""
        return self.story_frameworks.get(framework_key)

    def get_recommended_framework(self) -> StoryFramework:
        """推奨されるストーリーフレームワークを取得（時間の物語）"""
        return self.story_frameworks.get('time')

    def get_narrative_phrases(self, phrase_type: str) -> List[str]:
        """
        ナラティブフレーズを取得

        Args:
            phrase_type: openings, transitions, closings

        Returns:
            フレーズのリスト
        """
        return self.narrative_phrases.get(phrase_type, [])

    def get_filming_priority_locations(self) -> List[Dict]:
        """撮影優先度の高いロケーションを取得"""
        return self.filming_summary.get('key_visual_priorities', [])

    def get_seasonal_recommendations(self, season: str) -> Dict:
        """
        季節別の推奨ロケーションを取得

        Args:
            season: summer, spring_autumn, winter

        Returns:
            推奨ロケーション情報
        """
        seasonal = self.filming_summary.get('seasonal_recommendations', {})
        return seasonal.get(season, {})

    def suggest_locations_for_scene(
        self,
        scene_description: str,
        mood: Optional[str] = None,
        time_of_day: Optional[str] = None
    ) -> List[Location]:
        """
        シーン説明に基づいてロケーションを提案

        Args:
            scene_description: シーンの説明
            mood: ムード (peaceful, energetic, romantic, etc.)
            time_of_day: 時間帯

        Returns:
            提案されたロケーションのリスト（スコア順）
        """
        scored_locations = []

        for location in self.locations.values():
            score = 0.0

            # シーン説明とのマッチング
            desc_lower = scene_description.lower()

            # ロケーション名のマッチング
            if location.name.lower() in desc_lower:
                score += 20.0

            # コアナラティブのマッチング
            narrative_words = location.core_narrative.lower().split()
            for word in narrative_words:
                if len(word) > 2 and word in desc_lower:
                    score += 5.0

            # キーフィーチャーのマッチング
            for feature in location.key_features:
                feature_words = feature.lower().split()
                for word in feature_words:
                    if len(word) > 2 and word in desc_lower:
                        score += 3.0

            # ムードのマッチング
            if mood:
                mood_keywords = {
                    'peaceful': ['静', '穏やか', '平和', 'calm'],
                    'energetic': ['動', 'ダイナミック', 'dynamic', '賑わい'],
                    'romantic': ['ロマン', 'romantic', '夕日', 'sunset'],
                    'spiritual': ['霊場', '巡礼', '祈り', 'spiritual'],
                    'natural': ['自然', '野趣', 'nature', '波']
                }

                mood_lower = mood.lower()
                if mood_lower in mood_keywords:
                    keywords = mood_keywords[mood_lower]
                    theme_text = f"{location.storytelling_theme} {location.core_narrative}".lower()

                    for keyword in keywords:
                        if keyword in theme_text:
                            score += 10.0
                            break

            # 時間帯のマッチング
            if time_of_day:
                filming_tips = location.filming_tips
                best_time = filming_tips.get('best_time', '')
                if isinstance(best_time, str):
                    if time_of_day.lower() in best_time.lower():
                        score += 8.0

            if score > 0:
                scored_locations.append((score, location))

        # スコア順にソート
        scored_locations.sort(key=lambda x: x[0], reverse=True)

        return [loc for score, loc in scored_locations]

    def generate_story_structure(
        self,
        framework_key: str = 'time',
        num_cuts: int = 10
    ) -> List[Dict]:
        """
        ストーリー構造を生成

        Args:
            framework_key: 使用するフレームワーク (contrast, time, senses)
            num_cuts: カット数

        Returns:
            各カットのガイダンス情報
        """
        framework = self.get_story_framework(framework_key)
        if not framework:
            raise ValueError(f"Unknown framework: {framework_key}")

        structure = []

        if framework_key == 'time':
            # 時間の物語フレームワーク
            timeline = framework.timeline

            # タイムラインのエントリを分配
            for i, entry in enumerate(timeline):
                era = entry.get('era', '')
                location_name = entry.get('location', '')

                location = self.get_location_by_name(location_name)

                structure.append({
                    'cut_number': i + 1,
                    'era': era,
                    'location': location_name,
                    'location_id': location.id if location else None,
                    'narrative_hint': f"{era}の物語を表現",
                    'visual_elements': location.visual_elements if location else {},
                    'filming_tips': location.filming_tips if location else {}
                })

        elif framework_key == 'contrast':
            # 対比の物語フレームワーク
            contrasts = framework.structure

            for i, contrast_item in enumerate(contrasts):
                contrast_text = contrast_item.get('contrast', '')
                structure.append({
                    'cut_number': i + 1,
                    'contrast': contrast_text,
                    'narrative_hint': f"対比を表現: {contrast_text}"
                })

        elif framework_key == 'senses':
            # 五感の物語フレームワーク
            sensory_map = framework.sensory_mapping

            cut_num = 1
            for sense, locations in sensory_map.items():
                for location_name in locations:
                    location = self.get_location_by_name(location_name)
                    structure.append({
                        'cut_number': cut_num,
                        'sense': sense,
                        'location': location_name,
                        'location_id': location.id if location else None,
                        'narrative_hint': f"{sense}を刺激する表現",
                        'visual_elements': location.visual_elements if location else {},
                        'filming_tips': location.filming_tips if location else {}
                    })
                    cut_num += 1

        return structure[:num_cuts]  # 指定されたカット数に制限


def main():
    """CLI usage example"""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Research Database Query Tool"
    )
    parser.add_argument(
        '--database',
        required=True,
        help='Path to research YAML file'
    )
    parser.add_argument(
        '--list-locations',
        action='store_true',
        help='List all locations'
    )
    parser.add_argument(
        '--search',
        help='Search locations by keyword'
    )
    parser.add_argument(
        '--category',
        help='Filter by category'
    )
    parser.add_argument(
        '--framework',
        help='Show story framework (contrast, time, senses)'
    )

    args = parser.parse_args()

    # Load database
    db = ResearchDatabase(Path(args.database))

    print(f"📚 Research Database: {db.project.get('name', 'Unknown')}")
    print(f"   Theme: {db.project.get('theme', 'N/A')}")
    print(f"   Core Value: {db.project.get('core_value', 'N/A')}")
    print()

    # List locations
    if args.list_locations:
        print(f"📍 Locations ({len(db.locations)}):")
        for location in db.locations.values():
            print(f"  • {location.name} ({location.category})")
            print(f"    {location.core_narrative}")
            print()

    # Search
    if args.search:
        keywords = args.search.split(',')
        results = db.search_locations(
            category=args.category,
            keywords=keywords
        )
        print(f"🔍 Search results for '{args.search}':")
        for location in results:
            print(f"  • {location.name}")
            print(f"    {location.storytelling_theme}")
            print()

    # Framework
    if args.framework:
        framework = db.get_story_framework(args.framework)
        if framework:
            print(f"📖 Story Framework: {framework.name}")
            print(f"   Theme: {framework.theme}")
            print(f"   Target: {framework.target_audience}")
            if framework.timeline:
                print("   Timeline:")
                for entry in framework.timeline:
                    print(f"     • {entry.get('era')}: {entry.get('location')}")
            print()


if __name__ == "__main__":
    main()
