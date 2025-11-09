"""
南紀白浜プロジェクト: 素材管理システム

素材の読み込み、分類、動画への割り当てを管理
制約: 素材の拡大/縮小のみ許可、形状変更は禁止
"""

import json
import yaml
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Material:
    """素材データクラス"""
    filename: str
    category: str
    location: str
    description: str
    width: int
    height: int
    file_size: int
    path: str
    time_of_day: Optional[str] = None
    weather: Optional[str] = None
    main_subject: Optional[str] = None
    composition: Optional[str] = None
    color_tone: Optional[str] = None
    assigned_video: Optional[int] = None
    usage_notes: str = ""

    @property
    def aspect_ratio(self) -> float:
        """アスペクト比を計算"""
        return self.width / self.height if self.height > 0 else 1.0

    @property
    def is_hd(self) -> bool:
        """HD画質かどうか"""
        return self.width >= 1920 or self.height >= 1080

    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return asdict(self)


class MaterialManager:
    """素材管理クラス"""

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.materials_root = self.project_root / "source_materials"
        self.metadata_file = self.materials_root / "metadata" / "photo_descriptions.yaml"
        self.analysis_file = self.materials_root / "analyzed" / "material_analysis.json"
        self.mapping_file = self.materials_root / "analyzed" / "material_mapping.json"

        self.materials: List[Material] = []
        self.materials_by_category: Dict[str, List[Material]] = {}
        self.materials_by_video: Dict[int, List[Material]] = {}

    def load_materials(self) -> List[Material]:
        """素材メタデータを読み込む"""
        # メタデータファイルがある場合は読み込む
        if self.metadata_file.exists():
            return self._load_from_metadata()
        else:
            # メタデータがない場合はファイルから自動検出
            print("  ℹ️  メタデータファイルが見つかりません。ファイルから自動検出します...")
            return self._load_from_files()

    def _load_from_metadata(self) -> List[Material]:
        """メタデータファイルから素材を読み込む"""
        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        self.materials = []
        for photo in data.get('photos', []):
            # ファイルパスを構築
            category = photo['category']
            filename = photo['filename']
            file_path = self.materials_root / "raw" / category / filename

            material = Material(
                filename=filename,
                category=category,
                location=photo.get('location', ''),
                description=photo.get('description', ''),
                width=photo.get('width', 0),
                height=photo.get('height', 0),
                file_size=photo.get('file_size', 0),
                path=str(file_path),
                time_of_day=photo.get('time_of_day'),
                weather=photo.get('weather'),
                main_subject=photo.get('main_subject'),
                composition=photo.get('composition'),
                color_tone=photo.get('color_tone'),
                assigned_video=photo.get('assigned_video'),
                usage_notes=photo.get('usage_notes', '')
            )
            self.materials.append(material)

        # カテゴリ別に整理
        self._organize_by_category()

        return self.materials

    def _load_from_files(self) -> List[Material]:
        """ファイルシステムから素材を自動検出"""
        from PIL import Image
        import os

        self.materials = []
        raw_dir = self.materials_root / "raw"

        if not raw_dir.exists():
            raise FileNotFoundError(f"Materials directory not found: {raw_dir}")

        # カテゴリディレクトリを走査
        for category_dir in raw_dir.iterdir():
            if not category_dir.is_dir():
                continue

            category = category_dir.name

            # 画像ファイルを検出
            for image_file in category_dir.glob("*"):
                if image_file.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
                    continue

                try:
                    # 画像サイズを取得
                    with Image.open(image_file) as img:
                        width, height = img.size

                    # ファイル名から場所情報を抽出
                    filename = image_file.name
                    # 拡張子を除去
                    name_without_ext = filename.rsplit('.', 1)[0]
                    # 括弧とその中身を除去（全角・半角両対応）
                    location = re.split(r'[（(]', name_without_ext)[0]
                    # 数字とスペースを除去（例: "白良浜1" → "白良浜"）
                    location = re.sub(r'[\d\s]+$', '', location).strip()

                    material = Material(
                        filename=filename,
                        category=category,
                        location=location,
                        description=f"{location}の写真",
                        width=width,
                        height=height,
                        file_size=os.path.getsize(image_file),
                        path=str(image_file),
                        main_subject=location
                    )
                    self.materials.append(material)

                except Exception as e:
                    print(f"  ⚠️  Failed to load {image_file.name}: {e}")

        # カテゴリ別に整理
        self._organize_by_category()

        print(f"  ✓ {len(self.materials)} 枚の素材を自動検出しました")

        return self.materials

    def _organize_by_category(self):
        """カテゴリ別に素材を整理"""
        self.materials_by_category = {}
        for material in self.materials:
            if material.category not in self.materials_by_category:
                self.materials_by_category[material.category] = []
            self.materials_by_category[material.category].append(material)

    def get_materials_for_video(
        self,
        video_id: int,
        categories: List[str],
        count: int = 3
    ) -> List[Material]:
        """
        指定した動画用の素材を取得

        Args:
            video_id: 動画ID (1-4)
            categories: 使用するカテゴリリスト
            count: 必要な素材数

        Returns:
            選択された素材リスト
        """
        available = []
        for category in categories:
            if category in self.materials_by_category:
                # まだ割り当てられていない素材を優先
                unassigned = [
                    m for m in self.materials_by_category[category]
                    if m.assigned_video is None or m.assigned_video == video_id
                ]
                available.extend(unassigned)

        # HD画質優先でソート
        available.sort(key=lambda m: (m.is_hd, m.file_size), reverse=True)

        # 必要数だけ取得
        selected = available[:count]

        # 割り当てを記録
        for material in selected:
            material.assigned_video = video_id

        return selected

    def get_statistics(self) -> dict:
        """素材の統計情報を取得"""
        total = len(self.materials)
        hd_count = sum(1 for m in self.materials if m.is_hd)

        by_category = {}
        for category, materials in self.materials_by_category.items():
            by_category[category] = {
                'count': len(materials),
                'hd_count': sum(1 for m in materials if m.is_hd),
                'avg_size_mb': sum(m.file_size for m in materials) / len(materials) / (1024 * 1024)
            }

        return {
            'total_materials': total,
            'hd_count': hd_count,
            'hd_percentage': f"{hd_count / total * 100:.1f}%" if total > 0 else "0%",
            'by_category': by_category,
            'usage_rate': self._calculate_usage_rate()
        }

    def _calculate_usage_rate(self) -> dict:
        """素材使用率を計算"""
        total = len(self.materials)
        used = sum(1 for m in self.materials if m.assigned_video is not None)
        return {
            'used': used,
            'total': total,
            'rate': f"{used / total * 100:.1f}%" if total > 0 else "0%"
        }

    def save_mapping(self):
        """素材の割り当てマッピングを保存"""
        mapping = {
            'videos': {},
            'statistics': self.get_statistics()
        }

        # 動画別に整理
        for material in self.materials:
            if material.assigned_video:
                video_id = material.assigned_video
                if video_id not in mapping['videos']:
                    mapping['videos'][video_id] = []
                mapping['videos'][video_id].append({
                    'filename': material.filename,
                    'category': material.category,
                    'path': material.path,
                    'resolution': f"{material.width}x{material.height}",
                    'aspect_ratio': round(material.aspect_ratio, 2)
                })

        # 保存
        self.mapping_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)

        print(f"✓ Material mapping saved to: {self.mapping_file}")

    def validate_constraints(self) -> List[str]:
        """
        素材制約の検証

        Returns:
            警告メッセージのリスト
        """
        warnings = []

        # 最小使用率チェック (75%以上)
        stats = self.get_statistics()
        usage = stats['usage_rate']
        used = usage['used']
        total = usage['total']

        if used / total < 0.75:
            warnings.append(
                f"⚠ Material usage rate too low: {usage['rate']} (minimum: 75%)"
            )

        # HD画質比率チェック
        if stats['hd_count'] / total < 0.5:
            warnings.append(
                f"⚠ Low HD quality ratio: {stats['hd_percentage']} (recommended: 50%+)"
            )

        # カテゴリバランスチェック
        for category, info in stats['by_category'].items():
            if info['count'] < 2:
                warnings.append(
                    f"⚠ Category '{category}' has only {info['count']} material(s)"
                )

        return warnings

    def get_material_constraints_prompt(self) -> str:
        """
        素材制約をプロンプトとして生成
        画像生成AIに渡すための制約説明
        """
        return """
        *** 重要な素材制約 ***

        1. 提供された写真のモチーフ（被写体）は一切変更禁止
        2. 写真の拡大・縮小・トリミングは許可
        3. 写真の回転・歪み・変形は禁止
        4. アニメスタイルへの変換は許可（ただし構図とモチーフは保持）
        5. キャラクターの追加は許可（背景として写真を使用）

        *** I2V (Image-to-Video) 生成時の制約 ***

        - カメラワーク: Pan, Zoom, Tilt のみ使用
        - モーション強度: 低〜中程度（素材の形状を保持）
        - 被写体の変形を伴うモーションは使用禁止
        - 背景写真のモチーフは常に保持されること

        この制約を守りながら、観光プロモーションとして魅力的な動画を生成すること。
        """


def main():
    """テスト実行"""
    project_root = Path(__file__).parent
    manager = MaterialManager(project_root)

    print("Loading materials...")
    materials = manager.load_materials()
    print(f"✓ Loaded {len(materials)} materials")

    print("\nStatistics:")
    stats = manager.get_statistics()
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    print("\nConstraint validation:")
    warnings = manager.validate_constraints()
    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("✓ All constraints satisfied")

    print("\nMaterial constraints prompt:")
    print(manager.get_material_constraints_prompt())


if __name__ == "__main__":
    main()
