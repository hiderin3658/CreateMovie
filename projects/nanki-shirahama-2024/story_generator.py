"""
南紀白浜プロジェクト: 物語生成システム

素材から4本の10秒観光ストーリーを自動生成
Gemini APIを使用して、素材に基づいた魅力的な物語を作成
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from material_manager import MaterialManager, Material


@dataclass
class VideoStory:
    """動画ストーリー"""
    video_id: int
    title: str
    theme: str
    duration: int
    mood: str
    tempo: int
    narrative: str
    cuts: List[Dict[str, str]]
    materials: List[str]
    character_actions: List[str]

    def to_dict(self) -> dict:
        return asdict(self)


class StoryGenerator:
    """物語生成クラス"""

    def __init__(self, project_root: Path, api_key: Optional[str] = None):
        self.project_root = Path(project_root)
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required")

        if genai is None:
            raise ImportError("google-generativeai package is required")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

        # 素材マネージャー
        self.material_manager = MaterialManager(project_root)
        self.material_manager.load_materials()

    def generate_four_stories(self) -> List[VideoStory]:
        """
        4本の10秒ストーリーを生成

        Returns:
            4本の動画ストーリー
        """
        # 素材情報を取得
        materials_info = self._prepare_materials_info()

        # プロンプト作成
        prompt = self._create_story_prompt(materials_info)

        # Gemini APIで生成
        print("Generating stories with Gemini API...")
        response = self.model.generate_content(prompt)

        # レスポンスをパース
        stories = self._parse_story_response(response.text)

        # 素材を割り当て
        self._assign_materials_to_stories(stories)

        return stories

    def _prepare_materials_info(self) -> Dict:
        """素材情報を準備"""
        info = {
            'total': len(self.material_manager.materials),
            'categories': {}
        }

        for category, materials in self.material_manager.materials_by_category.items():
            info['categories'][category] = [
                {
                    'filename': m.filename,
                    'description': m.description,
                    'resolution': f"{m.width}x{m.height}",
                    'is_hd': m.is_hd
                }
                for m in materials
            ]

        return info

    def _create_story_prompt(self, materials_info: Dict) -> str:
        """ストーリー生成プロンプトを作成"""
        prompt = f"""
# 白浜観光プロモーション動画 ストーリー生成

## 目的
和歌山県白浜町の観光魅力を伝える30秒動画（10秒×4本）のストーリーを作成してください。
「行ってみたい」という旅行意欲を喚起することが目的です。

## 利用可能な素材
以下の16枚の写真を使用します：

### Beach (ビーチ): {len(materials_info['categories'].get('beach', []))}枚
{self._format_materials_list(materials_info['categories'].get('beach', []))}

### Nature (自然景観): {len(materials_info['categories'].get('nature', []))}枚
{self._format_materials_list(materials_info['categories'].get('nature', []))}

### Attractions (観光施設): {len(materials_info['categories'].get('attractions', []))}枚
{self._format_materials_list(materials_info['categories'].get('attractions', []))}

### Culture (文化): {len(materials_info['categories'].get('culture', []))}枚
{self._format_materials_list(materials_info['categories'].get('culture', []))}

## 制作要件

### 動画構成
- **Video 1 (10秒)**: "出会いの予感" - 白浜との最初の出会い
- **Video 2 (10秒)**: "自然の驚き" - 白浜の自然美との出会い
- **Video 3 (10秒)**: "体験の楽しみ" - アクティビティと地域体験
- **Video 4 (10秒)**: "もう一度来たい" - 白浜の魅力の集大成

### キャラクター設定
- 20歳の女性観光客（大学生風、明るく好奇心旺盛）
- 服装: カジュアルな夏服（Tシャツ、ショートパンツ）
- 持ち物: バックパック、カメラ、スマホ

### 各動画の構成
各10秒動画は3-4カットで構成します：
- カット1 (3秒): 導入シーン
- カット2 (3-4秒): メインシーン
- カット3 (3-4秒): クロージングシーン

## 出力形式
以下のJSON形式で4本の動画ストーリーを生成してください：

```json
{{
  "videos": [
    {{
      "video_id": 1,
      "title": "出会いの予感",
      "theme": "arrival_and_first_impression",
      "duration": 10,
      "mood": "hopeful, excited",
      "tempo": 120,
      "narrative": "白浜に到着した主人公が、真っ白な砂浜と青い海に出会う瞬間。...",
      "cuts": [
        {{
          "cut_number": 1,
          "duration": 3,
          "scene": "白良浜の全景",
          "camera_angle": "ELS (Extreme Long Shot)",
          "camera_movement": "Slow pan right",
          "character_action": "画面外から歩いて入ってくる",
          "mood": "期待感、ワクワク",
          "suggested_materials": ["白良浜2（全景）.JPG"]
        }},
        {{
          "cut_number": 2,
          "duration": 4,
          "scene": "砂浜を歩く主人公",
          "camera_angle": "MS (Medium Shot)",
          "camera_movement": "Follow",
          "character_action": "砂浜を歩き、周りを見渡す",
          "mood": "好奇心",
          "suggested_materials": ["白良浜1（海向き全景）.jpeg"]
        }},
        {{
          "cut_number": 3,
          "duration": 3,
          "scene": "海を見つめる主人公",
          "camera_angle": "CU (Close Up)",
          "camera_movement": "Static",
          "character_action": "海を見つめ、笑顔になる",
          "mood": "感動、期待",
          "suggested_materials": ["白良浜4（南向き）.jpeg"]
        }}
      ],
      "character_actions": [
        "ビーチに到着する",
        "砂浜を歩く",
        "海を見て笑顔になる"
      ]
    }}
  ]
}}
```

## 重要な制約
1. 各動画は正確に10秒（カットの合計）
2. 各カットは3-4秒
3. 提供された素材のファイル名を `suggested_materials` に含める
4. カメラワークは Pan, Zoom, Tilt のみ
5. キャラクターの動きは自然で観光客らしいもの
6. 4本の動画は独立しているが、ストーリーアークとして繋がっている

## 感情の流れ
Video 1: 期待・ワクワク → Video 2: 驚き・感動 → Video 3: 楽しさ・満足 → Video 4: 余韻・また来たい

それでは、上記の条件に基づいて4本の動画ストーリーをJSON形式で生成してください。
JSON以外のテキストは出力しないでください。
"""
        return prompt

    def _format_materials_list(self, materials: List[Dict]) -> str:
        """素材リストをフォーマット"""
        if not materials:
            return "  (なし)"

        lines = []
        for i, m in enumerate(materials, 1):
            lines.append(f"  {i}. {m['filename']} - {m['description']}")
        return "\n".join(lines)

    def _parse_story_response(self, response_text: str) -> List[VideoStory]:
        """
        Geminiのレスポンスをパースしてストーリーオブジェクトに変換
        """
        # JSONブロックを抽出（```json ... ``` の場合に対応）
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Response text: {response_text[:500]}...")
            raise

        stories = []
        for video_data in data.get('videos', []):
            story = VideoStory(
                video_id=video_data['video_id'],
                title=video_data['title'],
                theme=video_data['theme'],
                duration=video_data['duration'],
                mood=video_data['mood'],
                tempo=video_data['tempo'],
                narrative=video_data['narrative'],
                cuts=video_data['cuts'],
                materials=[],  # 後で割り当て
                character_actions=video_data.get('character_actions', [])
            )
            stories.append(story)

        return stories

    def _assign_materials_to_stories(self, stories: List[VideoStory]):
        """
        ストーリーに素材を割り当て
        """
        for story in stories:
            # カットから推奨素材を収集
            suggested = set()
            for cut in story.cuts:
                for material_name in cut.get('suggested_materials', []):
                    suggested.add(material_name)

            story.materials = list(suggested)

            # 素材マネージャーに割り当てを記録
            for material in self.material_manager.materials:
                if material.filename in suggested:
                    material.assigned_video = story.video_id

    def save_stories(self, stories: List[VideoStory], output_path: Optional[Path] = None):
        """ストーリーを保存"""
        if output_path is None:
            output_path = self.project_root / "generated" / "stories" / "stories.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'project': 'nanki-shirahama-2024',
            'total_videos': len(stories),
            'total_duration': sum(s.duration for s in stories),
            'videos': [s.to_dict() for s in stories]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✓ Stories saved to: {output_path}")

        # 素材マッピングも保存
        self.material_manager.save_mapping()

    def generate_story_report(self, stories: List[VideoStory]) -> str:
        """ストーリーレポートを生成"""
        report = []
        report.append("# 白浜観光プロモーション動画 ストーリー\n")

        for story in stories:
            report.append(f"## Video {story.video_id}: {story.title}\n")
            report.append(f"**テーマ**: {story.theme}")
            report.append(f"**時間**: {story.duration}秒")
            report.append(f"**ムード**: {story.mood}")
            report.append(f"**テンポ**: {story.tempo} BPM\n")

            report.append(f"**ナラティブ**:")
            report.append(f"{story.narrative}\n")

            report.append(f"**カット構成**:\n")
            for cut in story.cuts:
                report.append(f"### Cut {cut['cut_number']} ({cut['duration']}秒)")
                report.append(f"- **シーン**: {cut['scene']}")
                report.append(f"- **カメラ**: {cut['camera_angle']} / {cut['camera_movement']}")
                report.append(f"- **キャラクター**: {cut['character_action']}")
                report.append(f"- **ムード**: {cut['mood']}")
                report.append(f"- **素材**: {', '.join(cut.get('suggested_materials', []))}\n")

            report.append(f"**使用素材**: {len(story.materials)}枚")
            report.append(f"{', '.join(story.materials)}\n")
            report.append("---\n")

        return "\n".join(report)


def main():
    """テスト実行"""
    project_root = Path(__file__).parent

    try:
        generator = StoryGenerator(project_root)
        print("Generating 4 tourism stories for Nanki-Shirahama...")

        stories = generator.generate_four_stories()

        print(f"\n✓ Generated {len(stories)} stories")

        # 保存
        generator.save_stories(stories)

        # レポート生成
        report = generator.generate_story_report(stories)
        report_path = project_root / "generated" / "stories" / "story_report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ Story report saved to: {report_path}")

        # サマリー表示
        for story in stories:
            print(f"\nVideo {story.video_id}: {story.title} ({story.duration}s)")
            print(f"  - {len(story.cuts)} cuts")
            print(f"  - {len(story.materials)} materials")

    except Exception as e:
        print(f"✗ Error: {e}")
        raise


if __name__ == "__main__":
    main()
