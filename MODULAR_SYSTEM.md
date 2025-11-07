# モジュラー動画生成システム

## 概要

このプロジェクトは、AI動画生成のコア機能を抽出し、プロジェクトごとに機能を追加できるモジュラーシステムにリファクタリングされました。

## ディレクトリ構造

```
CreateMovie/
├── core/                      # コア機能（共通基盤）
│   ├── base/                 # 基底クラス
│   │   ├── generator.py      # BaseVideoGenerator
│   │   └── plugin.py         # BasePlugin
│   ├── video/                # 動画生成
│   │   ├── storyboard_generator.py
│   │   └── image_generator.py
│   ├── analysis/             # 解析機能
│   │   └── visual_analyzer.py
│   └── music/                # 音楽生成
│       └── music_generator.py
│
├── tools/                    # 管理ツール
│   └── project_manager.py    # プロジェクト管理
│
├── projects/                 # プロジェクト別管理
│   └── template/             # プロジェクトテンプレート
│
└── scripts/                  # 実行スクリプト
    ├── generate_storyboard.py      # 旧バージョン（互換性のため保持）
    └── generate_storyboard_v2.py   # 新バージョン（モジュラー）
```

## 主な変更点

### 1. コア機能の抽出

**以前**: すべての機能が`scripts/generate_storyboard.py`に統合されていました

**現在**: 機能ごとにモジュール化
- `core/base/`: 基底クラス（フックとプラグイン機能）
- `core/video/`: ストーリーボード生成と画像生成
- `core/analysis/`: ビジュアル解析
- `core/music/`: 音楽プロンプト生成

### 2. 拡張可能なアーキテクチャ

#### 基底クラス: BaseVideoGenerator

```python
from core.base import BaseVideoGenerator, GeneratorConfig

class MyCustomGenerator(BaseVideoGenerator):
    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        # カスタムフックを登録
        self.register_hook('pre_generation', self.my_preprocessing)

    def my_preprocessing(self, data):
        # カスタム前処理
        return data

    def generate_storyboard(self, input_data):
        # カスタムストーリーボード生成
        pass
```

#### プラグインシステム

```python
from core.base import BasePlugin

class MyCustomPlugin(BasePlugin):
    def setup(self, generator):
        self.generator = generator

    def supports_stage(self, stage):
        return stage in ['analysis', 'generation']

    def process(self, data, stage):
        # カスタム処理
        return data
```

### 3. プロジェクト管理

```python
from tools import ProjectManager

manager = ProjectManager(workspace=".")
project_id = manager.create_project(
    name="my_video_project",
    project_type="client",
    requirements={
        'duration': 60,
        'platform': 'youtube'
    }
)
```

## 使用方法

### 基本的な使用方法

```bash
# モジュラーバージョンを使用
python scripts/generate_storyboard_v2.py "魔法少女のオープニング" \
  --duration 60 \
  --cuts 8 \
  --output output/magical_girl \
  --title "魔法少女OP" \
  --style anime
```

### Pythonコードから使用

```python
from core.base import GeneratorConfig
from core.video import CoreStoryboardGenerator, ImageGenerator
from core.analysis import VisualAnalyzer
from core.music import MusicGenerator

# 設定
config = GeneratorConfig(
    duration=60,
    num_cuts=8,
    visual_style='anime',
    title='My Video'
)

# ストーリーボード生成
generator = CoreStoryboardGenerator(config)
storyboard = generator.generate_storyboard({
    'story_description': '魔法少女の物語'
})

# 画像生成
image_gen = ImageGenerator()
image_gen.generate_images(storyboard.cuts, 'output')

# 音楽プロンプト生成
music_gen = MusicGenerator()
music_plan = music_gen.generate_music_plan(storyboard.to_dict())

# 保存
generator.save_storyboard(storyboard, 'output')
```

### カスタムフックの使用

```python
from core.video import CoreStoryboardGenerator

generator = CoreStoryboardGenerator(config)

# カスタムフックを登録
def add_custom_processing(data):
    print("カスタム処理を実行中...")
    # データをカスタマイズ
    return data

generator.register_hook('pre_generation', add_custom_processing)
generator.register_hook('post_generation', add_custom_processing)

# 通常通り生成
storyboard = generator.generate_storyboard(input_data)
```

## プロジェクトごとの拡張

### 教育コンテンツ用カスタマイズ例

```python
from core.video import CoreStoryboardGenerator

class EducationVideoGenerator(CoreStoryboardGenerator):
    def __init__(self, config, audience="general"):
        super().__init__(config)
        self.audience = audience
        self.register_hook('post_generation', self.add_summary_slide)

    def add_summary_slide(self, storyboard):
        # まとめスライドを追加
        storyboard['cuts'].append({
            'type': 'summary',
            'duration': 10,
            'content': 'まとめ'
        })
        return storyboard
```

### 観光PR用カスタマイズ例

```python
from core.video import CoreStoryboardGenerator

class TourismVideoGenerator(CoreStoryboardGenerator):
    def __init__(self, config, destination):
        super().__init__(config)
        self.destination = destination
        self.register_hook('pre_generation', self.add_location_info)

    def add_location_info(self, data):
        data['location'] = self.destination
        return data
```

## 互換性

旧バージョンのスクリプト（`scripts/generate_storyboard.py`）は互換性のために保持されています。新しいプロジェクトでは `generate_storyboard_v2.py` の使用を推奨します。

## 依存関係

```bash
# コア依存関係のインストール
pip install -r requirements-core.txt
```

## 今後の拡張

- テーマ別拡張（`themes/`ディレクトリ）
- プラグインシステムの充実
- プロジェクトテンプレートの追加
- 素材管理機能の実装
- 複数プラットフォーム対応

## 設計ドキュメント

詳細な設計については `docs/design/modular-video-system-design.md` を参照してください。
