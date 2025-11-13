#!/usr/bin/env python3
"""
Research-Aware Matching Strategy
Uses structured research data to enhance material matching
"""

from pathlib import Path
from typing import Dict, List, Optional
from .matching_strategies import TourismMatchingStrategy
from .research_loader import ResearchDatabase


class ResearchAwareStrategy(TourismMatchingStrategy):
    """
    リサーチデータベースを活用した高度なマッチング戦略

    通常のTourismStrategyに加えて、構造化されたリサーチデータを参照し、
    より精度の高い素材マッチングを実現する。
    """

    def __init__(self, config: 'MaterialConfig', research_db_path: Optional[Path] = None):
        """
        Initialize research-aware strategy

        Args:
            config: Material configuration
            research_db_path: Path to research YAML database
        """
        super().__init__(config)

        self.research_db = None

        # リサーチデータベースの読み込み
        if research_db_path and research_db_path.exists():
            self.research_db = ResearchDatabase(research_db_path)
            print(f"✓ Research database loaded: {self.research_db.project.get('name')}")
        else:
            # デフォルトパスを試行
            default_path = config.project_root / "data" / "shirahama-locations-database.yaml"
            if default_path.exists():
                self.research_db = ResearchDatabase(default_path)
                print(f"✓ Research database loaded from default path")

    def find_best_match(
        self,
        cut: Dict,
        materials: List['Material'],
        matcher: 'MaterialMatcher'
    ) -> Optional['Material']:
        """
        リサーチデータを活用した最適マッチング

        Args:
            cut: カット情報
            materials: 素材リスト
            matcher: マッチャー

        Returns:
            最適な素材
        """
        candidates = matcher.find_candidates(cut, materials)

        def research_aware_bonus(material: 'Material', cut: Dict) -> float:
            """リサーチデータに基づくボーナス"""
            bonus = 0.0

            # 通常のツーリズムボーナス
            bonus += self._tourism_bonus(material, cut)

            # リサーチデータベースが利用可能な場合
            if self.research_db:
                bonus += self._research_bonus(material, cut)

            return bonus

        return self._score_and_select(candidates, cut, matcher, research_aware_bonus)

    def _tourism_bonus(self, material: 'Material', cut: Dict) -> float:
        """観光特有のボーナス（親クラスのロジックを再利用）"""
        bonus = 0.0

        # ランドマークが明確 → ボーナス
        if material.location and len(material.location) > 0:
            bonus += 10.0

        # 天候が良好 → ボーナス
        if material.weather and material.weather.lower() in ['sunny', 'clear']:
            bonus += 5.0

        # ゴールデンアワー/ブルーアワー → ボーナス
        if material.time_of_day and material.time_of_day.lower() in ['golden_hour', 'blue_hour']:
            bonus += 5.0

        # 場所名が完全一致
        if material.location:
            scene_desc = cut.get('scene_description', '').lower()
            if material.location.lower() in scene_desc:
                bonus += 15.0

        return bonus

    def _research_bonus(self, material: 'Material', cut: Dict) -> float:
        """リサーチデータに基づく追加ボーナス"""
        bonus = 0.0

        scene_desc = cut.get('scene_description', '').lower()
        mood = cut.get('mood', '')
        time_of_day = cut.get('time_of_day', '')

        # 素材のロケーション情報からリサーチデータを検索
        if material.location:
            # ロケーション名で検索
            location = self.research_db.get_location_by_name(material.location)

            if location:
                # コアナラティブのマッチング
                narrative_words = location.core_narrative.lower().split()
                for word in narrative_words:
                    if len(word) > 2 and word in scene_desc:
                        bonus += 8.0

                # ストーリーテーマのマッチング
                theme_words = location.storytelling_theme.lower().split()
                for word in theme_words:
                    if len(word) > 2 and word in scene_desc:
                        bonus += 6.0

                # ビジュアル要素のマッチング
                visual_primary = location.visual_elements.get('primary', '')
                if visual_primary:
                    visual_words = visual_primary.lower().split()
                    matches = sum(1 for word in visual_words if len(word) > 2 and word in scene_desc)
                    bonus += matches * 4.0

                # 推奨撮影時間のマッチング
                filming_tips = location.filming_tips
                best_time = filming_tips.get('best_time', '')

                if isinstance(best_time, str) and time_of_day:
                    if time_of_day.lower() in best_time.lower():
                        bonus += 12.0

                # カテゴリの重要度ボーナス
                # 撮影優先度が高いロケーション
                priorities = self.research_db.get_filming_priority_locations()
                priority_locations = [p['location'] for p in priorities]

                if location.name in priority_locations:
                    bonus += 10.0

        # リサーチDBを使ったシーンマッチング提案
        suggested_locations = self.research_db.suggest_locations_for_scene(
            scene_description=scene_desc,
            mood=mood,
            time_of_day=time_of_day
        )

        # 素材のロケーションが提案されたロケーションに含まれる場合
        if material.location and suggested_locations:
            suggested_names = [loc.name for loc in suggested_locations[:3]]  # Top 3
            if material.location in suggested_names:
                # ランキングに応じたボーナス
                rank = suggested_names.index(material.location) + 1
                bonus += 20.0 / rank  # 1位: 20pt, 2位: 10pt, 3位: 6.7pt

        return bonus

    def get_location_context(self, location_name: str) -> Optional[Dict]:
        """
        ロケーションの詳細情報を取得

        Args:
            location_name: ロケーション名

        Returns:
            ロケーション情報（撮影ガイド用）
        """
        if not self.research_db:
            return None

        location = self.research_db.get_location_by_name(location_name)
        if not location:
            return None

        return {
            'name': location.name,
            'core_narrative': location.core_narrative,
            'storytelling_theme': location.storytelling_theme,
            'key_features': location.key_features,
            'visual_elements': location.visual_elements,
            'filming_tips': location.filming_tips,
            'logistics': location.logistics
        }

    def enhance_storyboard_with_research(
        self,
        storyboard: Dict
    ) -> Dict:
        """
        ストーリーボードにリサーチデータを統合

        Args:
            storyboard: 元のストーリーボード

        Returns:
            リサーチデータで強化されたストーリーボード
        """
        if not self.research_db:
            return storyboard

        enhanced = storyboard.copy()

        # プロジェクトのコアバリューを追加
        enhanced['research_context'] = {
            'project_name': self.research_db.project.get('name'),
            'theme': self.research_db.project.get('theme'),
            'core_value': self.research_db.project.get('core_value')
        }

        # 各カットにロケーション情報を追加
        for cut in enhanced.get('cuts', []):
            scene_desc = cut.get('scene_description', '')
            mood = cut.get('mood', '')

            # リサーチDBから推奨ロケーションを取得
            suggested = self.research_db.suggest_locations_for_scene(
                scene_description=scene_desc,
                mood=mood
            )

            if suggested:
                top_location = suggested[0]
                cut['research_suggestion'] = {
                    'location_name': top_location.name,
                    'location_id': top_location.id,
                    'core_narrative': top_location.core_narrative,
                    'filming_tips': top_location.filming_tips,
                    'visual_elements': top_location.visual_elements
                }

        # ナラティブフレーズを追加
        enhanced['narrative_phrases'] = {
            'openings': self.research_db.get_narrative_phrases('openings'),
            'transitions': self.research_db.get_narrative_phrases('transitions'),
            'closings': self.research_db.get_narrative_phrases('closings')
        }

        return enhanced

    def generate_story_with_framework(
        self,
        framework_key: str = 'time',
        num_cuts: int = 10
    ) -> List[Dict]:
        """
        ストーリーフレームワークに基づいてストーリーを生成

        Args:
            framework_key: フレームワークキー (contrast, time, senses)
            num_cuts: カット数

        Returns:
            ストーリー構造
        """
        if not self.research_db:
            raise ValueError("Research database not loaded")

        return self.research_db.generate_story_structure(
            framework_key=framework_key,
            num_cuts=num_cuts
        )
