"""
南紀白浜プロジェクト: 絵コンテ生成システム

ストーリーから詳細な絵コンテを生成
素材制約（拡大/縮小のみ）を考慮したカメラワークを設定
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from story_generator import VideoStory
from material_manager import MaterialManager


@dataclass
class StoryboardCut:
    """絵コンテのカット"""
    cut_number: int
    duration: float
    scene_description: str
    camera_angle: str
    camera_movement: str
    character_action: str
    background_material: str
    background_path: str
    composition: str
    mood: str
    lighting: str
    notes: str = ""

    # I2V用の制約情報
    material_constraints: str = "Scale and crop only - no shape modification"
    camera_constraints: str = "Pan, Zoom, Tilt only"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Storyboard:
    """絵コンテ全体"""
    video_id: int
    title: str
    theme: str
    duration: int
    total_cuts: int
    cuts: List[StoryboardCut]
    materials_used: List[str]
    character_reference: Optional[str] = None
    created_at: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


class StoryboardGenerator:
    """絵コンテ生成クラス"""

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

    def generate_storyboard_from_story(self, story: VideoStory) -> Storyboard:
        """
        ストーリーから絵コンテを生成

        Args:
            story: VideoStory オブジェクト

        Returns:
            Storyboard オブジェクト
        """
        # プロンプト作成
        prompt = self._create_storyboard_prompt(story)

        # Gemini APIで詳細化
        print(f"Generating storyboard for Video {story.video_id}: {story.title}...")
        response = self.model.generate_content(prompt)

        # パースして絵コンテオブジェクト作成
        storyboard = self._parse_storyboard_response(response.text, story)

        return storyboard

    def _create_storyboard_prompt(self, story: VideoStory) -> str:
        """絵コンテ生成プロンプト"""
        # 使用する素材情報を取得
        materials_info = []
        for material_name in story.materials:
            material = next(
                (m for m in self.material_manager.materials if m.filename == material_name),
                None
            )
            if material:
                materials_info.append({
                    'filename': material.filename,
                    'path': material.path,
                    'category': material.category,
                    'resolution': f"{material.width}x{material.height}",
                    'aspect_ratio': f"{material.aspect_ratio:.2f}"
                })

        prompt = f"""
# 絵コンテ詳細化タスク

## Video情報
- **Video ID**: {story.video_id}
- **タイトル**: {story.title}
- **テーマ**: {story.theme}
- **時間**: {story.duration}秒
- **ムード**: {story.mood}

## ナラティブ
{story.narrative}

## カット構成
{json.dumps(story.cuts, ensure_ascii=False, indent=2)}

## 使用可能な素材
{json.dumps(materials_info, ensure_ascii=False, indent=2)}

## タスク
上記のカット構成を元に、各カットの詳細な絵コンテ情報を生成してください。

### 重要な制約
1. **素材制約**: 背景素材は拡大・縮小・トリミングのみ可能。形状変更・歪み・変形は禁止
2. **カメラワーク制約**: Pan（パン）、Zoom（ズーム）、Tilt（チルト）のみ使用可能
3. **素材の保持**: 背景写真のモチーフ（被写体）は必ず保持
4. **キャラクター配置**: 背景を邪魔しない位置にキャラクターを配置

### 各カットに必要な情報
- **composition**: 構図（三分割法、中央配置など）
- **lighting**: 照明（昼光、夕焼け、自然光など）
- **character_position**: キャラクターの配置位置
- **background_treatment**: 背景の扱い（フル表示、ズーム、パンなど）
- **notes**: I2V生成時の注意事項

## 出力形式
以下のJSON形式で出力してください：

```json
{{
  "cuts": [
    {{
      "cut_number": 1,
      "duration": 3.0,
      "scene_description": "白良浜の広大な白い砂浜と青い海が広がる全景。遠くに主人公が小さく見える",
      "camera_angle": "ELS",
      "camera_movement": "Slow pan right",
      "character_action": "画面左から歩いて入ってくる",
      "background_material": "白良浜2（全景）.JPG",
      "composition": "Rule of thirds - 空:海:砂浜 = 1:1:1",
      "mood": "開放感、期待",
      "lighting": "明るい昼光、快晴",
      "character_position": "画面左下 1/4位置",
      "background_treatment": "Full frame, gentle pan to reveal beach width",
      "notes": "I2V: Pan速度は非常にゆっくり。素材の白い砂浜と海のコントラストを保持。キャラクターは小さく控えめに。"
    }}
  ]
}}
```

JSON以外のテキストは出力しないでください。
"""
        return prompt

    def _parse_storyboard_response(
        self,
        response_text: str,
        story: VideoStory
    ) -> Storyboard:
        """Geminiレスポンスをパースして絵コンテ作成"""
        # JSONブロック抽出
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
            print(f"Response: {response_text[:500]}...")
            raise

        # StoryboardCutオブジェクトを作成
        cuts = []
        for cut_data in data.get('cuts', []):
            # 素材パスを取得
            material_name = cut_data.get('background_material', '')
            material = next(
                (m for m in self.material_manager.materials if m.filename == material_name),
                None
            )
            material_path = material.path if material else ""

            cut = StoryboardCut(
                cut_number=cut_data.get('cut_number', 0),
                duration=cut_data.get('duration', 3.0),
                scene_description=cut_data.get('scene_description', ''),
                camera_angle=cut_data.get('camera_angle', 'MS'),
                camera_movement=cut_data.get('camera_movement', 'Static'),
                character_action=cut_data.get('character_action', ''),
                background_material=material_name,
                background_path=material_path,
                composition=cut_data.get('composition', ''),
                mood=cut_data.get('mood', story.mood),
                lighting=cut_data.get('lighting', 'natural light'),
                notes=cut_data.get('notes', '')
            )
            cuts.append(cut)

        # Storyboardオブジェクト作成
        storyboard = Storyboard(
            video_id=story.video_id,
            title=story.title,
            theme=story.theme,
            duration=story.duration,
            total_cuts=len(cuts),
            cuts=cuts,
            materials_used=story.materials,
            created_at=datetime.now().isoformat()
        )

        return storyboard

    def save_storyboard(
        self,
        storyboard: Storyboard,
        output_path: Optional[Path] = None
    ):
        """絵コンテを保存"""
        if output_path is None:
            output_path = (
                self.project_root / "generated" / "storyboards" /
                f"video{storyboard.video_id}_storyboard.json"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(storyboard.to_dict(), f, ensure_ascii=False, indent=2)

        print(f"✓ Storyboard saved to: {output_path}")

    def generate_storyboard_report(self, storyboard: Storyboard) -> str:
        """絵コンテレポートを生成（Markdown形式）"""
        lines = []
        lines.append(f"# Video {storyboard.video_id}: {storyboard.title}\n")
        lines.append(f"**テーマ**: {storyboard.theme}")
        lines.append(f"**時間**: {storyboard.duration}秒")
        lines.append(f"**カット数**: {storyboard.total_cuts}\n")

        lines.append("---\n")

        for cut in storyboard.cuts:
            lines.append(f"## Cut {cut.cut_number} ({cut.duration}秒)\n")

            lines.append(f"### シーン")
            lines.append(f"{cut.scene_description}\n")

            lines.append(f"### カメラ")
            lines.append(f"- **アングル**: {cut.camera_angle}")
            lines.append(f"- **ムーブメント**: {cut.camera_movement}")
            lines.append(f"- **構図**: {cut.composition}\n")

            lines.append(f"### キャラクター")
            lines.append(f"{cut.character_action}\n")

            lines.append(f"### 背景素材")
            lines.append(f"- **ファイル**: `{cut.background_material}`")
            lines.append(f"- **パス**: `{cut.background_path}`\n")

            lines.append(f"### ムード・照明")
            lines.append(f"- **ムード**: {cut.mood}")
            lines.append(f"- **照明**: {cut.lighting}\n")

            lines.append(f"### I2V生成時の注意")
            lines.append(f"```")
            lines.append(f"{cut.notes}")
            lines.append(f"```\n")

            lines.append(f"**制約**:")
            lines.append(f"- 素材: {cut.material_constraints}")
            lines.append(f"- カメラ: {cut.camera_constraints}\n")

            lines.append("---\n")

        lines.append(f"\n**使用素材**: {len(storyboard.materials_used)}枚")
        lines.append(", ".join(storyboard.materials_used))

        return "\n".join(lines)


def main():
    """テスト実行"""
    import sys

    project_root = Path(__file__).parent

    # ストーリーファイルを読み込む
    stories_file = project_root / "generated" / "stories" / "stories.json"

    if not stories_file.exists():
        print("✗ Stories file not found. Please run story_generator.py first.")
        sys.exit(1)

    with open(stories_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # VideoStoryオブジェクトに変換
    from story_generator import VideoStory
    stories = []
    for video_data in data['videos']:
        story = VideoStory(
            video_id=video_data['video_id'],
            title=video_data['title'],
            theme=video_data['theme'],
            duration=video_data['duration'],
            mood=video_data['mood'],
            tempo=video_data['tempo'],
            narrative=video_data['narrative'],
            cuts=video_data['cuts'],
            materials=video_data['materials'],
            character_actions=video_data.get('character_actions', [])
        )
        stories.append(story)

    # 絵コンテ生成
    generator = StoryboardGenerator(project_root)

    for story in stories:
        storyboard = generator.generate_storyboard_from_story(story)
        generator.save_storyboard(storyboard)

        # レポート生成
        report = generator.generate_storyboard_report(storyboard)
        report_path = (
            project_root / "generated" / "storyboards" /
            f"video{storyboard.video_id}_report.md"
        )
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✓ Video {story.video_id} storyboard complete")


if __name__ == "__main__":
    main()
