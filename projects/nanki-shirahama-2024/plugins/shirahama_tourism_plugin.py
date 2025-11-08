#!/usr/bin/env python3
"""
Shirahama Tourism Plugin

南紀白浜観光プロモーション専用プラグイン
- 素材制約の強制（拡大/縮小のみ、形状変更禁止）
- カメラワーク制限（Pan/Zoom/Tilt のみ）
- 観光ストーリー最適化
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from core.base.plugin import BasePlugin


class ShirahamaTourismPlugin(BasePlugin):
    """南紀白浜観光プロモーション専用プラグイン"""

    # 許可されるカメラワーク（素材保護のため制限）
    ALLOWED_CAMERA_MOVEMENTS = [
        'static',
        'slow_pan',
        'pan_left',
        'pan_right',
        'zoom_in',
        'zoom_out',
        'slow_zoom_in',
        'slow_zoom_out',
        'tilt_up',
        'tilt_down'
    ]

    # 禁止されるカメラワーク（素材を変形させる可能性）
    FORBIDDEN_CAMERA_MOVEMENTS = [
        'tracking',
        'dolly_in',
        'dolly_out',
        'crane',
        'handheld',
        'orbital',
        'dutch_angle'
    ]

    # 観光動画用のシーンタイプ
    TOURISM_SCENE_TYPES = [
        'arrival',           # 到着シーン
        'landscape',         # 景観
        'attraction',        # 観光施設
        'experience',        # 体験
        'emotion',          # 感情表現
        'farewell'          # 別れ
    ]

    def __init__(self):
        super().__init__(name="shirahama_tourism")
        self.material_constraints = {
            'scale_allowed': True,
            'crop_allowed': True,
            'rotate_allowed': False,
            'distort_allowed': False,
            'morph_allowed': False,
            'modification_allowed': False
        }
        self.warnings: List[str] = []

    def setup(self, generator: 'BaseVideoGenerator'):
        """プラグインをセットアップ"""
        super().setup(generator)
        print(f"[{self.name}] Shirahama Tourism Plugin initialized")
        print(f"  - Material constraints: Scale/Crop only")
        print(f"  - Camera movements: {len(self.ALLOWED_CAMERA_MOVEMENTS)} allowed types")

    def supports_stage(self, stage: str) -> bool:
        """サポートするステージ"""
        return stage in ['pre_generation', 'post_generation', 'validation', 'camera_planning']

    def process(self, data: Dict, stage: str) -> Dict:
        """ステージごとの処理"""
        if stage == 'pre_generation':
            return self._pre_generation_processing(data)
        elif stage == 'post_generation':
            return self._post_generation_processing(data)
        elif stage == 'validation':
            return self._validate_constraints(data)
        elif stage == 'camera_planning':
            return self._plan_safe_camera_work(data)
        return data

    def _pre_generation_processing(self, data: Dict) -> Dict:
        """生成前処理: 観光ストーリー最適化"""
        print(f"[{self.name}] Pre-generation: Optimizing for tourism story")

        # 観光プロモーション用のコンテキスト追加
        if 'context' not in data:
            data['context'] = {}

        data['context']['tourism_focus'] = True
        data['context']['target_emotion'] = 'desire_to_visit'
        data['context']['constraint_mode'] = 'material_preservation'

        # 素材制約をデータに埋め込み
        data['material_constraints'] = self.material_constraints

        # カメラワーク制約を追加
        data['camera_constraints'] = {
            'allowed_movements': self.ALLOWED_CAMERA_MOVEMENTS,
            'forbidden_movements': self.FORBIDDEN_CAMERA_MOVEMENTS,
            'reason': 'Preserve original photo composition and subject matter'
        }

        return data

    def _post_generation_processing(self, data: Dict) -> Dict:
        """生成後処理: 制約チェックと警告"""
        print(f"[{self.name}] Post-generation: Validating constraints")

        self.warnings = []

        # カット情報をチェック
        if 'cuts' in data:
            for i, cut in enumerate(data['cuts'], 1):
                # カメラワークチェック
                camera_movement = cut.get('camera_movement', '').lower()
                if camera_movement:
                    # 許可リストにマッチするか確認
                    allowed = any(
                        allowed_mov in camera_movement
                        for allowed_mov in self.ALLOWED_CAMERA_MOVEMENTS
                    )
                    # 禁止リストにマッチしないか確認
                    forbidden = any(
                        forbidden_mov in camera_movement
                        for forbidden_mov in self.FORBIDDEN_CAMERA_MOVEMENTS
                    )

                    if forbidden:
                        warning = (
                            f"Cut {i}: Camera movement '{camera_movement}' may distort materials. "
                            f"Recommend: {self._suggest_alternative_movement(camera_movement)}"
                        )
                        self.warnings.append(warning)
                        # 安全な代替に置き換え
                        cut['camera_movement'] = self._suggest_alternative_movement(camera_movement)
                        cut['original_camera_movement'] = camera_movement

                # 素材制約の注記を追加
                if 'notes' not in cut:
                    cut['notes'] = ""
                cut['notes'] += "\n[Material Constraint] Scale/Crop only - No shape modification allowed"

        # 警告をデータに追加
        if self.warnings:
            data['plugin_warnings'] = data.get('plugin_warnings', []) + self.warnings
            print(f"  ⚠ {len(self.warnings)} constraint warnings")

        return data

    def _validate_constraints(self, data: Dict) -> Dict:
        """制約バリデーション"""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }

        # カット数チェック（10秒動画なら3-4カット推奨）
        if 'cuts' in data:
            num_cuts = len(data['cuts'])
            duration = data.get('duration', 10)

            if duration == 10:
                if num_cuts < 2:
                    validation_result['warnings'].append(
                        f"Only {num_cuts} cuts for 10s video. Recommend 3-4 cuts."
                    )
                elif num_cuts > 5:
                    validation_result['warnings'].append(
                        f"{num_cuts} cuts for 10s video may be too fast. Recommend 3-4 cuts."
                    )

        # 素材制約の明示
        validation_result['constraints'] = self.material_constraints
        validation_result['camera_constraints'] = {
            'allowed': self.ALLOWED_CAMERA_MOVEMENTS,
            'forbidden': self.FORBIDDEN_CAMERA_MOVEMENTS
        }

        data['validation_result'] = validation_result
        return data

    def _plan_safe_camera_work(self, data: Dict) -> Dict:
        """安全なカメラワークを計画"""
        if 'cuts' not in data:
            return data

        for cut in data['cuts']:
            scene_type = cut.get('scene_type', 'landscape')

            # シーンタイプに基づいた安全なカメラワーク選択
            safe_movement = self._get_safe_camera_for_scene(scene_type)

            if 'camera_movement' not in cut or not cut['camera_movement']:
                cut['camera_movement'] = safe_movement

        return data

    def _get_safe_camera_for_scene(self, scene_type: str) -> str:
        """シーンタイプに応じた安全なカメラワーク"""
        camera_map = {
            'arrival': 'slow_pan',
            'landscape': 'slow_zoom_in',
            'attraction': 'pan_right',
            'experience': 'static',
            'emotion': 'slow_zoom_in',
            'farewell': 'static',
            'establishing': 'slow_pan',
            'character': 'static'
        }
        return camera_map.get(scene_type, 'static')

    def _suggest_alternative_movement(self, forbidden_movement: str) -> str:
        """禁止されたカメラワークの代替案を提案"""
        alternatives = {
            'tracking': 'slow_pan',
            'dolly_in': 'slow_zoom_in',
            'dolly_out': 'slow_zoom_out',
            'crane': 'tilt_up',
            'handheld': 'static',
            'orbital': 'pan_right',
            'dutch_angle': 'static'
        }

        for forbidden, alternative in alternatives.items():
            if forbidden in forbidden_movement.lower():
                return alternative

        return 'static'

    def get_material_constraints_prompt(self) -> str:
        """素材制約をプロンプト文字列として取得（AI生成時に使用）"""
        return """
*** 重要: 素材制約（Material Constraints） ***

このプロジェクトでは提供された観光写真を背景として使用します。
以下の制約を厳守してください：

✅ 許可される操作:
  - 拡大・縮小（Scale）
  - トリミング（Crop）
  - カメラワーク: Pan（パン）、Zoom（ズーム）、Tilt（チルト）のみ

❌ 禁止される操作:
  - 形状変更・変形（Distortion）
  - 回転・歪み（Rotation, Warping）
  - モチーフ（被写体）の改変
  - 複雑な3Dカメラワーク（Tracking, Dolly, Crane, Orbital など）

理由: 観光写真のオリジナルな構図とランドマークを保護するため

カメラワークは必ず Pan/Zoom/Tilt のみを使用し、
素材の形状を変えないように注意してください。
"""

    def generate_i2v_constraints_note(self) -> str:
        """I2V生成時の制約ノート"""
        return """
I2V Generation Constraints:
- Motion Strength: LOW to MEDIUM only (to preserve material integrity)
- Camera Motion: Pan/Zoom/Tilt ONLY
- Subject Morphing: PROHIBITED
- Background Distortion: PROHIBITED
- Original composition MUST be preserved
"""


def create_plugin() -> ShirahamaTourismPlugin:
    """プラグインインスタンスを作成（ファクトリー関数）"""
    return ShirahamaTourismPlugin()


if __name__ == "__main__":
    # テスト
    plugin = create_plugin()
    print(f"Plugin: {plugin.name}")
    print(f"Material Constraints: {plugin.material_constraints}")
    print(f"\nMaterial Constraints Prompt:")
    print(plugin.get_material_constraints_prompt())
    print(f"\nI2V Constraints Note:")
    print(plugin.generate_i2v_constraints_note())
