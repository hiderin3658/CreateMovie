#!/usr/bin/env python3
"""
AI-powered Material Analyzer
Uses Gemini Vision API for image understanding
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class MaterialAnalyzer:
    """AI画像解析クラス"""

    def __init__(self, config: 'MaterialConfig'):
        self.config = config
        self.use_gemini = GEMINI_AVAILABLE and os.environ.get('GEMINI_API_KEY')

        if self.use_gemini:
            genai.configure(api_key=os.environ['GEMINI_API_KEY'])
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            print("  ✓ Gemini Vision API enabled")
        else:
            if not GEMINI_AVAILABLE:
                print("  ⚠️  google-generativeai not installed")
            else:
                print("  ⚠️  GEMINI_API_KEY not set")
            print("  → Using basic analysis only")

    def analyze_all_materials(
        self,
        materials_root: Path
    ) -> List['Material']:
        """全素材を解析"""
        from .material_system import Material

        print("🔍 Analyzing materials with AI...")

        materials = []
        raw_path = materials_root / "raw"

        # rawパスが存在しない場合
        if not raw_path.exists():
            print(f"  ⚠️  Raw materials path not found: {raw_path}")
            return materials

        # カテゴリフォルダをスキャン
        category_dirs = [d for d in raw_path.iterdir() if d.is_dir()]

        if not category_dirs:
            print(f"  ⚠️  No category directories found in {raw_path}")
            return materials

        for category_dir in category_dirs:
            category = category_dir.name
            print(f"\n  📂 Category: {category}")

            # 画像ファイルを検索
            image_files = []
            for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp']:
                image_files.extend(category_dir.glob(f"*{ext}"))
                image_files.extend(category_dir.glob(f"*{ext.upper()}"))

            if not image_files:
                print(f"    ⚠️  No image files found")
                continue

            print(f"    Found {len(image_files)} images")

            for image_file in image_files:
                print(f"    📸 {image_file.name}...", end=" ")

                # 画像を解析
                analysis = self.analyze_image(image_file, category)

                # Materialオブジェクト作成
                material = Material(
                    id=f"{category}_{image_file.stem}",
                    filename=image_file.name,
                    path=str(image_file),
                    category=category,
                    width=analysis['width'],
                    height=analysis['height'],
                    file_size=analysis['file_size'],
                    description=analysis['description'],
                    main_subject=analysis['main_subject'],
                    location=analysis.get('location'),
                    time_of_day=analysis.get('time_of_day'),
                    weather=analysis.get('weather'),
                    color_tone=analysis.get('color_tone'),
                    composition=analysis.get('composition'),
                    quality_score=analysis.get('quality_score', 0.0),
                    is_hd=analysis['width'] >= 1920 or analysis['height'] >= 1080
                )

                materials.append(material)
                print("✓")

        # メタデータを保存
        if materials:
            self._save_metadata(materials, materials_root)

        print(f"\n✅ Analyzed {len(materials)} materials")
        return materials

    def analyze_image(
        self,
        image_path: Path,
        category: str
    ) -> Dict:
        """単一画像を解析"""

        # 基本情報取得
        basic_info = self._get_basic_info(image_path)

        if not self.use_gemini:
            # Gemini利用不可の場合は基本情報のみ
            return {
                **basic_info,
                'description': f"{category} image",
                'main_subject': category,
                'quality_score': 0.5
            }

        # Gemini Vision APIで解析
        try:
            img = Image.open(image_path)

            # プロジェクトタイプに応じたプロンプト
            prompt = self._create_analysis_prompt(category, self.config.project_type)

            response = self.model.generate_content([prompt, img])

            # レスポンスをパース
            analysis = self._parse_gemini_response(response.text)

            return {
                **basic_info,
                **analysis
            }

        except Exception as e:
            print(f"\n    ⚠️  Error analyzing {image_path.name}: {e}")
            return {
                **basic_info,
                'description': f"{category} image",
                'main_subject': category,
                'quality_score': 0.5
            }

    def _get_basic_info(self, image_path: Path) -> Dict:
        """画像の基本情報を取得"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            img.close()
        except Exception:
            width, height = 0, 0

        file_size = image_path.stat().st_size

        return {
            'width': width,
            'height': height,
            'file_size': file_size
        }

    def _create_analysis_prompt(
        self,
        category: str,
        project_type: str
    ) -> str:
        """プロジェクトタイプに応じた解析プロンプト"""

        base_prompt = """Analyze this image and provide detailed metadata in JSON format.
Include the following fields:"""

        # 共通フィールド
        fields = [
            "description: Brief description of the image (2-3 sentences)",
            "main_subject: The main subject/landmark in the image",
            "composition: Composition type (centered, rule_of_thirds, symmetrical, etc.)",
            "color_tone: Overall color tone (warm, cool, neutral, vibrant, muted, etc.)",
            "quality_score: Visual quality score (0.0-1.0)"
        ]

        # プロジェクトタイプ別の追加フィールド
        if project_type == 'tourism':
            fields.extend([
                "location: Specific location or landmark name if identifiable",
                "time_of_day: Time of day (morning, afternoon, evening, night, golden_hour, blue_hour)",
                "weather: Weather condition (sunny, cloudy, rainy, foggy, clear)",
                "appeal_factor: What makes this location appealing"
            ])
        elif project_type == 'education':
            fields.extend([
                "educational_value: Educational value (0.0-1.0)",
                "complexity: Visual complexity (simple, moderate, complex)",
                "focus_points: Key areas that should be highlighted for learning"
            ])
        elif project_type == 'marketing':
            fields.extend([
                "product_visibility: How well a product could be showcased (0.0-1.0)",
                "emotional_appeal: Emotional appeal (exciting, calming, luxurious, etc.)",
                "target_audience: Suitable target audience"
            ])

        prompt = base_prompt + "\n" + "\n".join(f"- {f}" for f in fields)
        prompt += "\n\nRespond with ONLY valid JSON, no markdown formatting."

        return prompt

    def _parse_gemini_response(self, response_text: str) -> Dict:
        """Geminiのレスポンスをパース"""
        try:
            # JSONブロックを抽出（マークダウンのコードブロックを除去）
            cleaned_text = response_text.strip()

            # マークダウンのコードブロックを削除
            if cleaned_text.startswith('```'):
                # ```json ... ``` の形式
                cleaned_text = re.sub(r'^```(?:json)?\s*\n', '', cleaned_text)
                cleaned_text = re.sub(r'\n```\s*$', '', cleaned_text)

            # JSON部分を抽出
            json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())

                # 必須フィールドのデフォルト値
                defaults = {
                    'description': 'Image analysis',
                    'main_subject': 'unknown',
                    'quality_score': 0.5
                }

                # デフォルト値をマージ
                for key, default_value in defaults.items():
                    if key not in data:
                        data[key] = default_value

                return data
            else:
                # JSON形式でない場合はデフォルト
                return {
                    'description': response_text[:200],
                    'main_subject': 'unknown',
                    'quality_score': 0.5
                }

        except json.JSONDecodeError as e:
            print(f"\n    ⚠️  JSON parse error: {e}")
            return {
                'description': response_text[:200] if response_text else 'Parse error',
                'main_subject': 'unknown',
                'quality_score': 0.5
            }

    def _save_metadata(
        self,
        materials: List['Material'],
        materials_root: Path
    ):
        """メタデータをYAMLファイルに保存"""
        metadata_path = materials_root / "metadata" / "photo_descriptions.yaml"
        metadata_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'project_type': self.config.project_type,
            'total_materials': len(materials),
            'analyzed_by': 'MaterialAnalyzer with Gemini Vision API' if self.use_gemini else 'MaterialAnalyzer (basic)',
            'photos': [m.to_dict() for m in materials]
        }

        import yaml
        with open(metadata_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

        print(f"💾 Metadata saved to: {metadata_path}")
