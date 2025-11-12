#!/usr/bin/env python3
"""
Material Usage Tracking and Reporting
"""

from typing import Dict, List, Optional
from collections import defaultdict


class UsageTracker:
    """素材使用率の追跡"""

    def __init__(self, config: 'MaterialConfig'):
        self.config = config
        self.usage_map: Dict[str, int] = {}  # {material_id: cut_number}
        self.unused_reasons: Dict[str, str] = {}

    def mark_used(self, material_id: str, cut_number: int):
        """素材を使用済みとしてマーク"""
        self.usage_map[material_id] = cut_number

    def is_used(self, material_id: str) -> bool:
        """素材が使用済みかチェック"""
        return material_id in self.usage_map

    def get_usage_rate(self) -> float:
        """使用率を取得（0.0-1.0）"""
        # materials が必要なので、calculate_usage_rate で計算
        return 0.0

    def calculate_usage_rate(self, materials: Optional[List['Material']] = None) -> Dict:
        """詳細な使用率を計算"""
        if materials is None:
            return {
                'used': len(self.usage_map),
                'total': 0,
                'rate': 0.0,
                'percentage': '0%'
            }

        total = len(materials)
        used = len(self.usage_map)
        rate = used / total if total > 0 else 0.0

        return {
            'used': used,
            'total': total,
            'rate': rate,
            'percentage': f"{rate * 100:.1f}%"
        }

    def get_category_usage(self, materials: List['Material']) -> Dict[str, int]:
        """カテゴリ別の使用数"""
        category_usage = defaultdict(int)

        for material in materials:
            if material.id in self.usage_map:
                category_usage[material.category] += 1

        return dict(category_usage)

    def generate_detailed_report(
        self,
        materials: List['Material']
    ) -> Dict:
        """詳細な使用レポート"""

        report = {
            'summary': self.calculate_usage_rate(materials),
            'by_category': {},
            'used_materials': [],
            'unused_materials': []
        }

        # カテゴリ別統計
        category_stats = defaultdict(lambda: {'total': 0, 'used': 0})
        for material in materials:
            cat = material.category
            category_stats[cat]['total'] += 1
            if material.id in self.usage_map:
                category_stats[cat]['used'] += 1

        for cat, stats in category_stats.items():
            rate = stats['used'] / stats['total'] if stats['total'] > 0 else 0.0
            report['by_category'][cat] = {
                **stats,
                'rate': rate,
                'percentage': f"{rate * 100:.1f}%"
            }

        # 使用された素材
        for material in materials:
            if material.id in self.usage_map:
                report['used_materials'].append({
                    'cut_number': self.usage_map[material.id],
                    'filename': material.filename,
                    'category': material.category,
                    'match_score': material.match_score,
                    'path': material.path
                })

        # 未使用の素材
        for material in materials:
            if material.id not in self.usage_map:
                reason = self._analyze_unused_reason(material, materials)
                suggestions = self._generate_suggestions(material, materials)

                report['unused_materials'].append({
                    'filename': material.filename,
                    'category': material.category,
                    'reason': reason,
                    'quality_score': material.quality_score,
                    'suggestions': suggestions
                })

        return report

    def _analyze_unused_reason(
        self,
        material: 'Material',
        all_materials: List['Material']
    ) -> str:
        """未使用の理由を分析"""

        # 品質が低い
        if not material.is_hd:
            return "Low quality (not HD resolution)"

        if material.quality_score < 0.5:
            return f"Low quality score ({material.quality_score:.2f})"

        # 同じカテゴリの素材が多い
        category_materials = [m for m in all_materials if m.category == material.category]
        category_count = len(category_materials)
        category_used = sum(1 for m in category_materials if m.id in self.usage_map)

        if category_count > 5 and category_used >= category_count - 1:
            return f"Category oversupplied ({category_count} {material.category} materials, {category_used} used)"

        # 内容が特定的すぎる
        if material.location and len(material.description) > 100:
            return "Content too specific for current story requirements"

        # スコアが低かった（他の素材が選ばれた）
        return "Not matched to any scene requirements (lower score than alternatives)"

    def _generate_suggestions(
        self,
        material: 'Material',
        all_materials: List['Material']
    ) -> List[str]:
        """改善提案を生成"""
        suggestions = []

        # バリエーション動画での使用を提案
        if material.quality_score >= 0.7:
            suggestions.append("Consider using in video variation or alternative version")

        # 品質改善の提案
        if not material.is_hd:
            suggestions.append("Consider using higher resolution version if available")

        # カテゴリ変更の提案
        if material.quality_score >= 0.6:
            suggestions.append(f"Could be recategorized from '{material.category}' to better match scenes")

        return suggestions
