# 南紀白浜観光プロモーション動画生成システム v2.0

**コアシステム統合版** - CreateMovieプロジェクトのコアシステムを使用した観光動画生成

## 概要

このプロジェクトは、提供された16枚の観光写真から4本の10秒動画（合計30秒）の絵コンテと動画プロンプトを自動生成します。

### アーキテクチャ

```
コアシステム (core/)
  ├── BaseVideoGenerator      # 基底クラス
  ├── CoreStoryboardGenerator # 絵コンテ生成
  └── Plugin システム          # 拡張機能

南紀白浜プロジェクト (projects/nanki-shirahama-2024/)
  ├── plugins/
  │   └── shirahama_tourism_plugin.py  # 観光特化 + 素材制約
  ├── material_manager.py               # 素材管理
  └── generate_tourism_videos_v2.py     # メインスクリプト
```

### 主な特徴

1. **コアシステム統合**
   - `CoreStoryboardGenerator` による絵コンテ生成
   - プラグインシステムで南紀白浜特有の制約を実装

2. **素材制約の厳格な管理**
   - ✅ 拡大・縮小・トリミングのみ許可
   - ❌ 形状変更・歪み・変形は禁止
   - プラグインが自動的に制約をチェック

3. **観光プロモーション最適化**
   - 観光ストーリーに特化した処理
   - カメラワークを Pan/Zoom/Tilt に制限

## セットアップ

### 必要要件

```bash
# コアシステムの依存パッケージ
pip install -r ../../requirements-core.txt

# プロジェクト固有の依存パッケージ
pip install -r requirements.txt
```

### API キー設定

```bash
export GEMINI_API_KEY='your-api-key-here'
# または .env ファイルに記載
```

## 使い方

### 基本的な使用方法

```bash
# 4本の観光動画を生成
python generate_tourism_videos_v2.py "白浜の観光体験"
```

### オプション指定

```bash
# カスタム設定
python generate_tourism_videos_v2.py "白浜旅行の魅力" \
  --duration 30 \
  --num-videos 4 \
  --character-ref character.png \
  --output my_output
```

### パラメータ

- `story`: ストーリーの説明（必須）
- `--duration`: 総時間（秒）デフォルト: 30
- `--num-videos`: 動画本数。デフォルト: 4
- `--character-ref`: キャラクター参照画像のパス
- `--output`: 出力ディレクトリ

## プロジェクト構成

```
nanki-shirahama-2024/
├── plugins/
│   ├── __init__.py
│   └── shirahama_tourism_plugin.py   # 南紀白浜専用プラグイン
│
├── generate_tourism_videos_v2.py     # メインスクリプト（コアシステム統合）
├── material_manager.py               # 素材管理
├── requirements.txt                  # プロジェクト固有の依存関係
├── config.yaml                       # プロジェクト設定
│
├── source_materials/                 # 素材（16枚の観光写真）
│   ├── raw/
│   │   ├── beach/
│   │   ├── nature/
│   │   ├── attractions/
│   │   └── culture/
│   ├── metadata/
│   └── analyzed/
│
├── generated_v2/                     # 生成ファイル（実行後に作成）
│   ├── video1/
│   │   ├── storyboard.json
│   │   └── i2v_prompts.json
│   ├── video2/
│   ├── video3/
│   └── video4/
│
└── legacy/                           # 旧スタンドアロン版（非推奨）
```

## プラグインの仕組み

### ShirahamaTourismPlugin

南紀白浜観光に特化したプラグイン：

```python
from plugins.shirahama_tourism_plugin import create_plugin

# プラグイン作成
plugin = create_plugin()

# 素材制約
plugin.material_constraints  # {'scale_allowed': True, 'distort_allowed': False, ...}

# 許可されるカメラワーク
plugin.ALLOWED_CAMERA_MOVEMENTS  # ['static', 'pan', 'zoom', 'tilt']

# 禁止されるカメラワーク
plugin.FORBIDDEN_CAMERA_MOVEMENTS  # ['tracking', 'dolly', 'crane', ...]
```

### プラグインの処理ステージ

1. **pre_generation**: 生成前の最適化
2. **post_generation**: 制約チェックと警告
3. **validation**: バリデーション
4. **camera_planning**: 安全なカメラワーク計画

## ワークフロー

### 1. 絵コンテ生成（自動）

```bash
python generate_tourism_videos_v2.py "白浜観光"
```

出力:
- `generated_v2/video1-4/storyboard.json` - 詳細な絵コンテ
- `generated_v2/video1-4/i2v_prompts.json` - I2V用プロンプト

### 2. 動画生成（手動 - Runway Gen-3 など）

1. Runway Gen-3 にアクセス
2. `i2v_prompts.json` のプロンプトを使用
3. 各カットを動画化
4. 素材制約を厳守（Scale/Crop のみ）

### 3. 編集と仕上げ（手動）

1. 動画編集ソフトで結合
2. BGM追加（Suno AI）
3. 最終書き出し（9:16, 1080x1920, 30fps）

## コアシステムとの違い

| 項目 | スタンドアロン版（旧） | コアシステム統合版（新） |
|------|---------------------|----------------------|
| 絵コンテ生成 | 独自実装 | `CoreStoryboardGenerator` 使用 |
| 拡張性 | 低い | プラグインで高い拡張性 |
| 再利用性 | 南紀白浜専用 | 他プロジェクトでも使用可能 |
| 制約管理 | ハードコード | プラグインで動的管理 |
| メンテナンス | 個別 | コアシステムの改善が反映 |

## トラブルシューティング

### プラグインの警告が表示される

**問題**: `⚠️ 2 件の警告`

**解決**: これは正常です。プラグインが禁止されたカメラワークを安全な代替に自動置換しています。

### 素材使用率が低い

**問題**: 素材使用率が75%未満

**解決**: `config.yaml` の各動画の `materials_count` を増やしてください。

### APIエラー

**問題**: `GEMINI_API_KEY is required`

**解決**:
```bash
export GEMINI_API_KEY='your-key'
```

## 開発者向け情報

### カスタムプラグインの作成

```python
from core.base.plugin import BasePlugin

class MyTourismPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="my_plugin")

    def supports_stage(self, stage: str) -> bool:
        return stage in ['pre_generation', 'post_generation']

    def process(self, data: Dict, stage: str) -> Dict:
        # カスタム処理
        return data
```

### コアシステムのカスタマイズ

コアシステムは `core/` ディレクトリにあり、全プロジェクトで共有されます。
プロジェクト固有の処理は必ずプラグインで実装してください。

## ライセンス

このプロジェクトは南紀白浜観光プロモーションコンペ用に作成されました。

## 参考ドキュメント

- [README.md](README.md) - 素材配置ガイド
- [PROJECT_SPEC.md](PROJECT_SPEC.md) - プロジェクト仕様書
- [QUICKSTART.md](QUICKSTART.md) - クイックスタートガイド
- [IMPLEMENTATION_README.md](IMPLEMENTATION_README.md) - 旧スタンドアロン版のドキュメント（参考）

---

**バージョン**: 2.0 (コアシステム統合版)
**作成日**: 2024-11-08
**プロジェクトID**: nanki-shirahama-2024
