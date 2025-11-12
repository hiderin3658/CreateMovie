#!/usr/bin/env python3
"""
Matching Strategies for Different Project Types
Strategy Pattern implementation for flexible material matching
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class MaterialMatchingStrategy(ABC):
    """素材マッチング戦略の基底クラス"""

    def __init__(self, config: 'MaterialConfig'):
        self.config = config

    @abstractmethod
    def find_best_match(
        self,
        cut: Dict,
        materials: List['Material'],
        matcher: 'MaterialMatcher'
    ) -> Optional['Material']:
        """最適な素材を検索"""
        pass

    def _score_and_select(
        self,
        candidates: List['Material'],
        cut: Dict,
        matcher: 'MaterialMatcher',
        bonus_fn=None
    ) -> Optional['Material']:
        """候補をスコアリングして最適な素材を選択（共通ロジック）"""
        if not candidates:
            return None

        scored = []
        for material in candidates:
            score = matcher.score_material(material, cut)

            # ストラテジー固有のボーナス
            if bonus_fn:
                score += bonus_fn(material, cut)

            material.match_score = score
            scored.append((score, material))

        # スコア順にソート
        scored.sort(key=lambda x: x[0], reverse=True)

        return scored[0][1] if scored else None


class TourismMatchingStrategy(MaterialMatchingStrategy):
    """観光プロジェクト用のマッチング戦略"""

    def find_best_match(
        self,
        cut: Dict,
        materials: List['Material'],
        matcher: 'MaterialMatcher'
    ) -> Optional['Material']:
        """観光向けマッチング"""

        candidates = matcher.find_candidates(cut, materials)

        def tourism_bonus(material: 'Material', cut: Dict) -> float:
            """観光特有のボーナス"""
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

        return self._score_and_select(candidates, cut, matcher, tourism_bonus)


class EducationMatchingStrategy(MaterialMatchingStrategy):
    """教育プロジェクト用のマッチング戦略"""

    def find_best_match(
        self,
        cut: Dict,
        materials: List['Material'],
        matcher: 'MaterialMatcher'
    ) -> Optional['Material']:
        """教育向けマッチング"""

        candidates = matcher.find_candidates(cut, materials)

        def education_bonus(material: 'Material', cut: Dict) -> float:
            """教育特有のボーナス"""
            bonus = 0.0

            # シンプルな構図 → 学習しやすい
            if material.composition and material.composition.lower() in ['centered', 'simple']:
                bonus += 10.0

            # 明るい画像 → 見やすい
            if material.color_tone and material.color_tone.lower() in ['bright', 'clear']:
                bonus += 5.0

            # 高い教育的価値（カスタムフィールド）
            # educational_value は Gemini の education プロンプトで取得
            # ここではデフォルト実装

            return bonus

        return self._score_and_select(candidates, cut, matcher, education_bonus)


class MarketingMatchingStrategy(MaterialMatchingStrategy):
    """マーケティングプロジェクト用のマッチング戦略"""

    def find_best_match(
        self,
        cut: Dict,
        materials: List['Material'],
        matcher: 'MaterialMatcher'
    ) -> Optional['Material']:
        """マーケティング向けマッチング"""

        candidates = matcher.find_candidates(cut, materials)

        def marketing_bonus(material: 'Material', cut: Dict) -> float:
            """マーケティング特有のボーナス"""
            bonus = 0.0

            # 感情的な訴求力
            emotional_keywords = ['exciting', 'luxurious', 'premium', 'lifestyle', 'elegant']
            material_desc = material.description.lower()
            if any(kw in material_desc for kw in emotional_keywords):
                bonus += 10.0

            # 構図が商品配置に適している
            if material.composition and material.composition.lower() in ['rule_of_thirds', 'leading_lines']:
                bonus += 5.0

            # 明るく鮮やかな色調
            if material.color_tone and material.color_tone.lower() in ['vivid', 'bright', 'saturated']:
                bonus += 3.0

            return bonus

        return self._score_and_select(candidates, cut, matcher, marketing_bonus)


class CompetitionMatchingStrategy(MaterialMatchingStrategy):
    """コンペ用のマッチング戦略（全素材使用を優先）"""

    def find_best_match(
        self,
        cut: Dict,
        materials: List['Material'],
        matcher: 'MaterialMatcher'
    ) -> Optional['Material']:
        """コンペ向けマッチング（全素材使用を優先）"""

        candidates = matcher.find_candidates(cut, materials)

        def competition_bonus(material: 'Material', cut: Dict) -> float:
            """コンペ特有のボーナス"""
            bonus = 0.0

            # 未使用素材に大きなボーナス（全素材使用を促進）
            if material.assigned_to is None:
                bonus += 20.0

            return bonus

        return self._score_and_select(candidates, cut, matcher, competition_bonus)


class DefaultMatchingStrategy(MaterialMatchingStrategy):
    """デフォルトのマッチング戦略"""

    def find_best_match(
        self,
        cut: Dict,
        materials: List['Material'],
        matcher: 'MaterialMatcher'
    ) -> Optional['Material']:
        """標準的なマッチング"""

        candidates = matcher.find_candidates(cut, materials)

        return self._score_and_select(candidates, cut, matcher, bonus_fn=None)
