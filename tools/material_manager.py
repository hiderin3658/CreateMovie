#!/usr/bin/env python3
"""
Material Manager for Tourism Project
Handles photo analysis, categorization, and mapping to video cuts
"""
import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from PIL import Image


@dataclass
class MaterialMetadata:
    """Metadata for a source material"""
    filename: str
    category: str
    location: str
    description: str
    time_of_day: str
    weather: str
    main_subject: str
    composition: str
    color_tone: str
    assigned_video: Optional[int] = None
    usage_notes: str = ""

    # Image properties
    width: int = 0
    height: int = 0
    file_size: int = 0

    def to_dict(self) -> Dict:
        return asdict(self)


class MaterialManager:
    """Manager for source materials in tourism projects"""

    def __init__(self, project_path: Path):
        """
        Initialize material manager

        Args:
            project_path: Path to project directory
        """
        self.project_path = Path(project_path)
        self.materials_path = self.project_path / "source_materials"
        self.raw_path = self.materials_path / "raw"
        self.analyzed_path = self.materials_path / "analyzed"
        self.metadata_path = self.materials_path / "metadata"

        # Ensure directories exist
        self.analyzed_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)

        self.materials: List[MaterialMetadata] = []

    def scan_materials(self) -> int:
        """
        Scan all materials in raw folder

        Returns:
            Number of materials found
        """
        print("📁 Scanning materials...")

        categories = ["beach", "nature", "attractions", "culture"]

        for category in categories:
            category_path = self.raw_path / category
            if not category_path.exists():
                print(f"  ⚠️  Category folder not found: {category}")
                continue

            # Find image files
            image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
            image_files = [
                f for f in category_path.glob("*")
                if f.suffix.lower() in image_extensions
            ]

            print(f"  ✓ {category}: {len(image_files)} files")

            for image_file in image_files:
                metadata = self._extract_metadata(image_file, category)
                self.materials.append(metadata)

        print(f"\n✅ Total materials found: {len(self.materials)}")
        return len(self.materials)

    def _extract_metadata(
        self,
        image_path: Path,
        category: str
    ) -> MaterialMetadata:
        """
        Extract metadata from image file

        Args:
            image_path: Path to image file
            category: Material category

        Returns:
            MaterialMetadata object
        """
        # Get image properties
        try:
            img = Image.open(image_path)
            width, height = img.size
            img.close()
        except Exception:
            width, height = 0, 0

        file_size = image_path.stat().st_size

        # Create metadata (basic info, to be enhanced later)
        metadata = MaterialMetadata(
            filename=image_path.name,
            category=category,
            location="白浜",  # Default
            description=f"{category} photo from Shirahama",
            time_of_day="unknown",
            weather="unknown",
            main_subject=category,
            composition="unknown",
            color_tone="unknown",
            width=width,
            height=height,
            file_size=file_size
        )

        return metadata

    def save_metadata(self) -> Path:
        """
        Save materials metadata to YAML file

        Returns:
            Path to saved file
        """
        output_path = self.metadata_path / "photo_descriptions.yaml"

        data = {
            'project': 'nanki-shirahama-2024',
            'total_materials': len(self.materials),
            'photos': [m.to_dict() for m in self.materials]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

        print(f"\n💾 Metadata saved to: {output_path}")
        return output_path

    def generate_analysis_report(self) -> Dict:
        """
        Generate analysis report for materials

        Returns:
            Analysis report dict
        """
        print("\n📊 Generating analysis report...")

        # Count by category
        category_counts = {}
        for material in self.materials:
            cat = material.category
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # Resolution check
        hd_count = sum(
            1 for m in self.materials
            if m.width >= 1920 and m.height >= 1080
        )

        # Average file size
        avg_size = sum(m.file_size for m in self.materials) / len(self.materials) if self.materials else 0

        report = {
            'total_materials': len(self.materials),
            'by_category': category_counts,
            'hd_quality': {
                'count': hd_count,
                'percentage': f"{hd_count / len(self.materials) * 100:.1f}%" if self.materials else "0%"
            },
            'average_file_size_mb': f"{avg_size / (1024 * 1024):.2f}",
            'quality_assessment': 'good' if hd_count >= len(self.materials) * 0.8 else 'needs_improvement',
            'recommendations': self._generate_recommendations(category_counts)
        }

        # Save report
        report_path = self.analyzed_path / "material_analysis.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"  ✓ Report saved to: {report_path}")

        return report

    def _generate_recommendations(
        self,
        category_counts: Dict[str, int]
    ) -> List[str]:
        """Generate recommendations based on material counts"""
        recommendations = []

        # Check if we have enough materials per category
        min_per_category = 3

        for category in ["beach", "nature", "attractions", "culture"]:
            count = category_counts.get(category, 0)
            if count < min_per_category:
                recommendations.append(
                    f"Need more {category} photos (current: {count}, recommended: {min_per_category}+)"
                )
            elif count > 5:
                recommendations.append(
                    f"{category}: Excellent variety ({count} photos)"
                )

        return recommendations

    def map_materials_to_videos(self) -> Dict:
        """
        Map materials to 4 videos based on categories

        Returns:
            Mapping dictionary
        """
        print("\n🎬 Mapping materials to videos...")

        mapping = {
            'video1': {
                'title': '出会いの予感',
                'categories': ['beach'],
                'materials': []
            },
            'video2': {
                'title': '自然の驚き',
                'categories': ['nature'],
                'materials': []
            },
            'video3': {
                'title': '体験の楽しみ',
                'categories': ['attractions', 'culture'],
                'materials': []
            },
            'video4': {
                'title': 'もう一度来たい',
                'categories': ['beach', 'nature'],
                'materials': []
            }
        }

        # Assign materials to videos
        for video_id, video_data in mapping.items():
            for category in video_data['categories']:
                category_materials = [
                    m for m in self.materials
                    if m.category == category
                ]
                video_data['materials'].extend([
                    m.filename for m in category_materials
                ])

        # Save mapping
        mapping_path = self.analyzed_path / "material_mapping.json"
        with open(mapping_path, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)

        print(f"  ✓ Mapping saved to: {mapping_path}")

        # Print summary
        for video_id, video_data in mapping.items():
            print(f"\n  {video_id}: {video_data['title']}")
            print(f"    Categories: {', '.join(video_data['categories'])}")
            print(f"    Materials: {len(video_data['materials'])} files")

        return mapping

    def print_summary(self):
        """Print summary of materials"""
        print("\n" + "="*60)
        print("📋 MATERIAL SUMMARY")
        print("="*60)

        print(f"\nTotal materials: {len(self.materials)}")

        # By category
        print("\nBy category:")
        categories = {}
        for material in self.materials:
            cat = material.category
            categories[cat] = categories.get(cat, 0) + 1

        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} files")

        # Quality check
        hd_materials = [
            m for m in self.materials
            if m.width >= 1920 and m.height >= 1080
        ]

        print(f"\nQuality:")
        print(f"  HD (1920x1080+): {len(hd_materials)}/{len(self.materials)}")
        print(f"  Percentage: {len(hd_materials)/len(self.materials)*100:.1f}%")

        print("\n" + "="*60)


def main():
    """Main function for CLI usage"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Material Manager for Tourism Projects"
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Project directory path'
    )
    parser.add_argument(
        '--scan',
        action='store_true',
        help='Scan materials'
    )
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze materials'
    )
    parser.add_argument(
        '--map',
        action='store_true',
        help='Map materials to videos'
    )

    args = parser.parse_args()

    # Initialize manager
    manager = MaterialManager(Path(args.project))

    # Scan materials
    if args.scan or args.analyze or args.map:
        manager.scan_materials()

    # Analyze
    if args.analyze:
        manager.generate_analysis_report()

    # Map to videos
    if args.map:
        manager.map_materials_to_videos()

    # Always show summary
    manager.print_summary()

    # Save metadata
    manager.save_metadata()

    print("\n✅ Material management complete!")


if __name__ == "__main__":
    main()
