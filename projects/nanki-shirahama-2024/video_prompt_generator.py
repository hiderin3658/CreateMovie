"""
南紀白浜プロジェクト: 動画プロンプト生成システム

絵コンテからI2V（Image-to-Video）用のプロンプトを生成
Runway Gen-3、Pika Labs、その他のI2Vツール向けに最適化
素材制約を厳密に守る（拡大/縮小のみ、形状変更禁止）
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

from storyboard_generator import Storyboard, StoryboardCut


@dataclass
class I2VPrompt:
    """I2V用プロンプト"""
    cut_number: int
    duration: float
    input_image: str
    input_image_path: str

    # Runway Gen-3用
    runway_prompt: str
    runway_camera_control: str
    runway_motion_strength: str  # low, medium, high

    # Pika Labs用
    pika_prompt: str
    pika_motion_value: int  # 1-4
    pika_camera_motion: str

    # 汎用プロンプト
    general_prompt: str
    general_camera_instruction: str

    # 制約情報
    constraints: Dict[str, str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class VideoPromptSet:
    """動画全体のプロンプトセット"""
    video_id: int
    title: str
    duration: int
    total_cuts: int
    prompts: List[I2VPrompt]

    def to_dict(self) -> dict:
        return asdict(self)


class VideoPromptGenerator:
    """動画プロンプト生成クラス"""

    # カメラワークのマッピング
    CAMERA_MOVEMENTS = {
        'static': {
            'runway': 'static camera, no movement',
            'pika': 0,
            'general': 'Static shot, camera does not move'
        },
        'pan_right': {
            'runway': 'camera pans slowly to the right',
            'pika': 2,
            'general': 'Slow pan to the right, revealing the scene horizontally'
        },
        'pan_left': {
            'runway': 'camera pans slowly to the left',
            'pika': 2,
            'general': 'Slow pan to the left, revealing the scene horizontally'
        },
        'zoom_in': {
            'runway': 'camera slowly zooms in',
            'pika': 2,
            'general': 'Gentle zoom in to focus on subject'
        },
        'zoom_out': {
            'runway': 'camera slowly zooms out',
            'pika': 2,
            'general': 'Gentle zoom out to reveal wider scene'
        },
        'tilt_up': {
            'runway': 'camera tilts up',
            'pika': 1,
            'general': 'Camera tilts upward'
        },
        'tilt_down': {
            'runway': 'camera tilts down',
            'pika': 1,
            'general': 'Camera tilts downward'
        }
    }

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)

    def generate_prompts_from_storyboard(
        self,
        storyboard: Storyboard
    ) -> VideoPromptSet:
        """
        絵コンテから動画プロンプトセットを生成

        Args:
            storyboard: Storyboard オブジェクト

        Returns:
            VideoPromptSet オブジェクト
        """
        prompts = []

        for cut in storyboard.cuts:
            i2v_prompt = self._generate_cut_prompt(cut, storyboard)
            prompts.append(i2v_prompt)

        prompt_set = VideoPromptSet(
            video_id=storyboard.video_id,
            title=storyboard.title,
            duration=storyboard.duration,
            total_cuts=storyboard.total_cuts,
            prompts=prompts
        )

        return prompt_set

    def _generate_cut_prompt(
        self,
        cut: StoryboardCut,
        storyboard: Storyboard
    ) -> I2VPrompt:
        """
        各カット用のI2Vプロンプトを生成
        """
        # カメラワークを解析
        camera_movement = self._parse_camera_movement(cut.camera_movement)

        # モーション強度を決定
        motion_strength = self._determine_motion_strength(camera_movement)

        # 制約情報
        constraints = {
            'material_modification': 'PROHIBITED - Scale and crop only',
            'shape_change': 'PROHIBITED',
            'distortion': 'PROHIBITED',
            'allowed_operations': 'Pan, Zoom, Tilt, Crop only',
            'preserve': 'Original composition and subject matter MUST be preserved'
        }

        # Runway Gen-3用プロンプト
        runway_prompt = self._generate_runway_prompt(cut, camera_movement)
        runway_camera = self._get_camera_instruction(camera_movement, 'runway')

        # Pika Labs用プロンプト
        pika_prompt = self._generate_pika_prompt(cut, camera_movement)
        pika_motion = self._get_camera_instruction(camera_movement, 'pika')
        pika_camera = self._get_camera_instruction(camera_movement, 'general')

        # 汎用プロンプト
        general_prompt = self._generate_general_prompt(cut, camera_movement)
        general_camera = self._get_camera_instruction(camera_movement, 'general')

        return I2VPrompt(
            cut_number=cut.cut_number,
            duration=cut.duration,
            input_image=cut.background_material,
            input_image_path=cut.background_path,
            runway_prompt=runway_prompt,
            runway_camera_control=runway_camera,
            runway_motion_strength=motion_strength,
            pika_prompt=pika_prompt,
            pika_motion_value=pika_motion,
            pika_camera_motion=pika_camera,
            general_prompt=general_prompt,
            general_camera_instruction=general_camera,
            constraints=constraints
        )

    def _parse_camera_movement(self, movement_str: str) -> str:
        """カメラワーク文字列を正規化"""
        movement_str = movement_str.lower()

        if 'pan' in movement_str and 'right' in movement_str:
            return 'pan_right'
        elif 'pan' in movement_str and 'left' in movement_str:
            return 'pan_left'
        elif 'zoom in' in movement_str or 'zoom-in' in movement_str:
            return 'zoom_in'
        elif 'zoom out' in movement_str or 'zoom-out' in movement_str:
            return 'zoom_out'
        elif 'tilt up' in movement_str:
            return 'tilt_up'
        elif 'tilt down' in movement_str:
            return 'tilt_down'
        elif 'static' in movement_str or 'still' in movement_str:
            return 'static'
        else:
            return 'static'  # デフォルト

    def _get_camera_instruction(self, movement: str, platform: str) -> str:
        """プラットフォーム別のカメラ指示を取得"""
        if movement in self.CAMERA_MOVEMENTS:
            return self.CAMERA_MOVEMENTS[movement][platform]
        return self.CAMERA_MOVEMENTS['static'][platform]

    def _determine_motion_strength(self, camera_movement: str) -> str:
        """モーション強度を決定（素材保護のため低〜中のみ）"""
        if camera_movement == 'static':
            return 'low'
        elif camera_movement in ['tilt_up', 'tilt_down']:
            return 'low'
        elif camera_movement in ['pan_right', 'pan_left', 'zoom_in', 'zoom_out']:
            return 'medium'
        else:
            return 'low'

    def _generate_runway_prompt(
        self,
        cut: StoryboardCut,
        camera_movement: str
    ) -> str:
        """Runway Gen-3用プロンプトを生成"""
        parts = []

        # シーン説明
        parts.append(cut.scene_description)

        # キャラクターアクション
        if cut.character_action:
            parts.append(f"A young woman tourist {cut.character_action}")

        # 照明とムード
        parts.append(f"{cut.lighting}, {cut.mood} atmosphere")

        # アニメスタイル
        parts.append("anime illustration style, vibrant colors")

        # カメラワーク（Runwayは別パラメータだが念のため含める）
        camera_inst = self._get_camera_instruction(camera_movement, 'runway')
        parts.append(camera_inst)

        # 制約を強調
        parts.append("Preserve original composition and landmarks exactly")

        prompt = ". ".join(parts) + "."
        return prompt

    def _generate_pika_prompt(
        self,
        cut: StoryboardCut,
        camera_movement: str
    ) -> str:
        """Pika Labs用プロンプトを生成"""
        parts = []

        # シーン
        parts.append(cut.scene_description)

        # キャラクター
        if cut.character_action:
            parts.append(f"Tourist character: {cut.character_action}")

        # スタイル
        parts.append("anime style, bright and cheerful")

        # カメラワーク（Pikaはモーション値だが説明も含める）
        camera_inst = self._get_camera_instruction(camera_movement, 'general')
        parts.append(camera_inst)

        prompt = ". ".join(parts) + "."
        return prompt

    def _generate_general_prompt(
        self,
        cut: StoryboardCut,
        camera_movement: str
    ) -> str:
        """汎用I2Vプロンプトを生成"""
        parts = []

        parts.append(f"Scene: {cut.scene_description}")
        parts.append(f"Character: {cut.character_action}")
        parts.append(f"Camera: {cut.camera_angle}, {cut.camera_movement}")
        parts.append(f"Mood: {cut.mood}")
        parts.append(f"Lighting: {cut.lighting}")
        parts.append(f"Style: anime illustration, tourism promotion")
        parts.append(f"Composition: {cut.composition}")

        # 制約
        parts.append("IMPORTANT: Preserve original photo composition and landmarks")
        parts.append("Only camera movement allowed - no object morphing or distortion")

        prompt = "\n".join(parts)
        return prompt

    def save_prompts(
        self,
        prompt_set: VideoPromptSet,
        output_path: Optional[Path] = None
    ):
        """プロンプトセットを保存"""
        if output_path is None:
            output_path = (
                self.project_root / "generated" / "video_prompts" /
                f"video{prompt_set.video_id}_prompts.json"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(prompt_set.to_dict(), f, ensure_ascii=False, indent=2)

        print(f"✓ Video prompts saved to: {output_path}")

    def generate_prompt_guide(self, prompt_set: VideoPromptSet) -> str:
        """プロンプト使用ガイドを生成（Markdown）"""
        lines = []
        lines.append(f"# Video {prompt_set.video_id}: {prompt_set.title} - I2V Prompts\n")
        lines.append(f"**Total Duration**: {prompt_set.duration}秒")
        lines.append(f"**Total Cuts**: {prompt_set.total_cuts}\n")

        lines.append("---\n")

        for prompt in prompt_set.prompts:
            lines.append(f"## Cut {prompt.cut_number} ({prompt.duration}秒)\n")

            lines.append(f"### Input Image")
            lines.append(f"```")
            lines.append(f"File: {prompt.input_image}")
            lines.append(f"Path: {prompt.input_image_path}")
            lines.append(f"```\n")

            lines.append(f"### Runway Gen-3")
            lines.append(f"**Prompt**:")
            lines.append(f"```")
            lines.append(f"{prompt.runway_prompt}")
            lines.append(f"```")
            lines.append(f"**Camera Control**: {prompt.runway_camera_control}")
            lines.append(f"**Motion Strength**: {prompt.runway_motion_strength}\n")

            lines.append(f"### Pika Labs")
            lines.append(f"**Prompt**:")
            lines.append(f"```")
            lines.append(f"{prompt.pika_prompt}")
            lines.append(f"```")
            lines.append(f"**Motion Value**: {prompt.pika_motion_value}/4")
            lines.append(f"**Camera Motion**: {prompt.pika_camera_motion}\n")

            lines.append(f"### General (その他のI2Vツール)")
            lines.append(f"```")
            lines.append(f"{prompt.general_prompt}")
            lines.append(f"```\n")

            lines.append(f"### ⚠️ 制約事項")
            for key, value in prompt.constraints.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("\n")

            lines.append("---\n")

        return "\n".join(lines)


def main():
    """テスト実行"""
    import sys

    project_root = Path(__file__).parent

    # 絵コンテファイルを探す
    storyboard_dir = project_root / "generated" / "storyboards"
    if not storyboard_dir.exists():
        print("✗ Storyboards not found. Please run storyboard_generator.py first.")
        sys.exit(1)

    storyboard_files = list(storyboard_dir.glob("video*_storyboard.json"))
    if not storyboard_files:
        print("✗ No storyboard files found.")
        sys.exit(1)

    generator = VideoPromptGenerator(project_root)

    for storyboard_file in storyboard_files:
        # 絵コンテ読み込み
        with open(storyboard_file, 'r', encoding='utf-8') as f:
            storyboard_data = json.load(f)

        # Storyboardオブジェクトに変換（簡易版）
        from storyboard_generator import Storyboard, StoryboardCut

        cuts = []
        for cut_data in storyboard_data['cuts']:
            cut = StoryboardCut(**cut_data)
            cuts.append(cut)

        storyboard = Storyboard(
            video_id=storyboard_data['video_id'],
            title=storyboard_data['title'],
            theme=storyboard_data['theme'],
            duration=storyboard_data['duration'],
            total_cuts=storyboard_data['total_cuts'],
            cuts=cuts,
            materials_used=storyboard_data['materials_used'],
            character_reference=storyboard_data.get('character_reference'),
            created_at=storyboard_data.get('created_at', '')
        )

        # プロンプト生成
        prompt_set = generator.generate_prompts_from_storyboard(storyboard)
        generator.save_prompts(prompt_set)

        # ガイド生成
        guide = generator.generate_prompt_guide(prompt_set)
        guide_path = (
            project_root / "generated" / "video_prompts" /
            f"video{prompt_set.video_id}_prompt_guide.md"
        )
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)

        print(f"✓ Video {storyboard.video_id} prompts complete")


if __name__ == "__main__":
    main()
