#!/usr/bin/env python3
"""
Material Matching Engine with Scoring System
"""

import re
from typing import Dict, List, Optional
from collections import defaultdict


class MaterialMatcher:
    """素材マッチングエンジン"""

    def __init__(self, config: 'MaterialConfig'):
        self.config = config
        self.weights = config.scoring_weights

        # インデックス
        self.by_category: Dict[str, List['Material']] = defaultdict(list)
        self.by_subject: Dict[str, List['Material']] = defaultdict(list)
        self.by_time: Dict[str, List['Material']] = defaultdict(list)

    def index_materials(self, materials: List['Material']):
        """素材をインデックス化して高速検索"""
        self.by_category.clear()
        self.by_subject.clear()
        self.by_time.clear()

        for material in materials:
            # カテゴリ別
            self.by_category[material.category].append(material)

            # 被写体別
            if material.main_subject:
                self.by_subject[material.main_subject.lower()].append(material)

            # 時間帯別
            if material.time_of_day:
                self.by_time[material.time_of_day.lower()].append(material)

    def find_candidates(
        self,
        cut: Dict,
        materials: List['Material']
    ) -> List['Material']:
        """候補素材をフィルタリング"""

        candidates = []

        # カテゴリフィルター
        required_categories = cut.get('categories', [])
        if required_categories:
            for category in required_categories:
                candidates.extend(self.by_category.get(category, []))
        else:
            # カテゴリ指定なしなら全素材
            candidates = materials.copy()

        # 既に使用済みの素材を除外（オプション）
        if not self.config.usage_requirements.get('allow_reuse', False):
            candidates = [m for m in candidates if m.assigned_to is None]

        return candidates

    def score_material(
        self,
        material: 'Material',
        cut: Dict
    ) -> float:
        """素材をスコアリング"""

        score = 0.0
        scene_desc = cut.get('scene_description', '').lower()

        # 1. キーワードマッチング
        keywords = self._extract_keywords(scene_desc)
        material_text = f"{material.description} {material.main_subject} {material.location or ''}".lower()

        keyword_matches = sum(1 for kw in keywords if kw in material_text)
        score += keyword_matches * self.weights.get('keyword_match', 5.0)

        # 2. カテゴリマッチング
        if material.category in cut.get('categories', []):
            score += self.weights.get('category_match', 3.0)

        # 3. 時間帯マッチング
        cut_time = cut.get('time_of_day', '').lower()
        if cut_time and material.time_of_day:
            if cut_time in material.time_of_day.lower():
                score += self.weights.get('time_match', 2.0)

        # 4. ムードマッチング
        cut_mood = cut.get('mood', '').lower()
        if cut_mood and material.color_tone:
            if self._mood_matches_color(cut_mood, material.color_tone):
                score += self.weights.get('mood_match', 2.0)

        # 5. 品質ボーナス
        if material.is_hd:
            score += self.weights.get('quality_bonus', 1.0)

        score += material.quality_score * self.weights.get('quality_bonus', 1.0)

        # 6. 未使用ボーナス
        if material.assigned_to is None:
            score += self.weights.get('unused_bonus', 0.5)

        return score

    def _extract_keywords(self, text: str) -> List[str]:
        """テキストからキーワードを抽出"""
        # 3文字以上の単語を抽出
        words = re.findall(r'\b\w{3,}\b', text.lower())
        # 重複を除去
        return list(set(words))

    def _mood_matches_color(self, mood: str, color_tone: str) -> bool:
        """ムードと色調の相性チェック"""
        mood_color_map = {
            'hopeful': ['warm', 'bright', 'gold', 'yellow'],
            'adventurous': ['vivid', 'blue', 'bright'],
            'romantic': ['warm', 'pink', 'soft', 'pastel'],
            'peaceful': ['blue', 'soft', 'calm', 'muted'],
            'energetic': ['vivid', 'bright', 'saturated'],
            'nostalgic': ['warm', 'sepia', 'muted'],
            'mysterious': ['dark', 'cool', 'shadow'],
            'joyful': ['bright', 'vivid', 'saturated'],
            'melancholy': ['muted', 'gray', 'soft']
        }

        mood_lower = mood.lower()
        color_lower = color_tone.lower()

        # 直接マッチング
        if mood_lower in mood_color_map:
            return any(c in color_lower for c in mood_color_map[mood_lower])

        # 部分マッチング（"hopeful and excited" のようなケース）
        for mood_key, colors in mood_color_map.items():
            if mood_key in mood_lower:
                if any(c in color_lower for c in colors):
                    return True

        return False
