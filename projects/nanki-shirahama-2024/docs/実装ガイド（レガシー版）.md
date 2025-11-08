# 南紀白浜観光プロモーション動画生成システム

素材から物語→絵コンテ→動画プロンプトまでを自動生成する、観光動画制作支援システムです。

## 概要

このシステムは、提供された16枚の観光写真から、4本の10秒動画（合計30秒）の絵コンテと動画プロンプトを自動生成します。

### 主な機能

1. **素材管理** - 観光写真の分類・解析・割り当て
2. **物語生成** - Gemini APIを使用した4本のストーリー自動生成
3. **絵コンテ生成** - 詳細なカット構成と演出プラン作成
4. **動画プロンプト生成** - Runway Gen-3、Pika Labs対応のI2Vプロンプト生成

### 重要な制約

**素材の扱い**:
- ✅ 拡大・縮小・トリミング OK
- ✅ アニメスタイル変換 OK
- ❌ 形状変更・歪み・変形 禁止
- ❌ モチーフ（被写体）の改変 禁止

**カメラワーク**:
- ✅ Pan（パン）、Zoom（ズーム）、Tilt（チルト）のみ
- ❌ 複雑な3Dカメラワーク禁止

## セットアップ

### 必要要件

- Python 3.8以上
- Gemini API キー（Google AI Studioから取得）
- 必要なパッケージ:
  - `google-generativeai>=0.3.0`
  - `pyyaml>=6.0.0`

### インストール

```bash
# 1. プロジェクトディレクトリに移動
cd projects/nanki-shirahama-2024/

# 2. 依存パッケージをインストール
pip install google-generativeai pyyaml

# 3. API キーを設定
export GEMINI_API_KEY='your-api-key-here'
# または .env ファイルに記載
echo "GEMINI_API_KEY=your-key" > .env
```

## 使い方

### 基本的な使用方法

```bash
# フルパイプライン実行（物語→絵コンテ→プロンプト）
python generate_tourism_videos.py
```

実行すると以下の処理が自動的に行われます：

1. **素材検証** - 16枚の写真の読み込みと検証
2. **物語生成** - Gemini APIで4本のストーリー生成（30-60秒）
3. **絵コンテ生成** - 各ストーリーの詳細なカット構成作成
4. **プロンプト生成** - I2V用プロンプトの生成

### 段階的実行

```bash
# 1. 物語生成のみ
python generate_tourism_videos.py --stories-only

# 2. 既存のストーリーから絵コンテとプロンプトを生成
python generate_tourism_videos.py --from-stories
```

### 個別モジュールの実行

```bash
# 素材管理のテスト
python material_manager.py

# 物語生成のみ
python story_generator.py

# 絵コンテ生成（ストーリーが必要）
python storyboard_generator.py

# プロンプト生成（絵コンテが必要）
python video_prompt_generator.py
```

## 出力ファイル

実行後、`generated/` ディレクトリに以下のファイルが生成されます：

```
generated/
├── stories/
│   ├── stories.json              # 4本のストーリーデータ
│   └── story_report.md           # ストーリーレポート（人間可読）
│
├── storyboards/
│   ├── video1_storyboard.json    # Video 1 絵コンテデータ
│   ├── video1_report.md          # Video 1 絵コンテレポート
│   ├── video2_storyboard.json
│   ├── video2_report.md
│   ├── video3_storyboard.json
│   ├── video3_report.md
│   ├── video4_storyboard.json
│   └── video4_report.md
│
└── video_prompts/
    ├── video1_prompts.json       # Video 1 I2Vプロンプト
    ├── video1_prompt_guide.md    # Video 1 プロンプトガイド
    ├── video2_prompts.json
    ├── video2_prompt_guide.md
    ├── video3_prompts.json
    ├── video3_prompt_guide.md
    ├── video4_prompts.json
    └── video4_prompt_guide.md
```

## ワークフロー

### 1. 準備（このシステムで完了）

```bash
python generate_tourism_videos.py
```

### 2. I2V動画生成（手動）

`generated/video_prompts/` のガイドを参照して：

**Runway Gen-3 の場合:**
1. Runway Gen-3 にアクセス
2. 各カットの背景素材画像をアップロード
3. `runway_prompt` をコピー&ペースト
4. Camera Control: `runway_camera_control` を設定
5. Motion Strength: `runway_motion_strength` を設定
6. Generate

**Pika Labs の場合:**
1. Pika Labs にアクセス
2. 背景素材画像をアップロード
3. `pika_prompt` をコピー&ペースト
4. Motion: `pika_motion_value` を設定
5. Camera: `pika_camera_motion` を参考に設定
6. Generate

### 3. 編集と仕上げ（手動）

1. **動画編集**:
   - Adobe Premiere Pro / DaVinci Resolve / Final Cut Pro
   - 各カットを時間通りに配置（絵コンテの duration 参照）
   - トランジション追加
   - カラーグレーディング

2. **BGM追加**:
   - Suno AI でBGM生成
   - ムードとテンポは `stories.json` を参照

3. **最終書き出し**:
   - 形式: MP4
   - 解像度: 1080x1920 (9:16)
   - フレームレート: 30fps

## プロジェクト構成

```
nanki-shirahama-2024/
├── generate_tourism_videos.py    # 統合実行スクリプト（メイン）
├── material_manager.py           # 素材管理
├── story_generator.py            # 物語生成
├── storyboard_generator.py       # 絵コンテ生成
├── video_prompt_generator.py     # 動画プロンプト生成
│
├── source_materials/             # 素材ディレクトリ
│   ├── raw/                      # オリジナル写真
│   │   ├── beach/                # ビーチ写真
│   │   ├── nature/               # 自然景観
│   │   ├── attractions/          # 観光施設
│   │   └── culture/              # 文化・歴史
│   ├── metadata/
│   │   └── photo_descriptions.yaml
│   └── analyzed/
│       ├── material_analysis.json
│       └── material_mapping.json
│
├── generated/                    # 生成ファイル（実行後に作成）
│   ├── stories/
│   ├── storyboards/
│   └── video_prompts/
│
├── config.yaml                   # プロジェクト設定
├── PROJECT_SPEC.md               # プロジェクト仕様書
├── QUICKSTART.md                 # クイックスタートガイド
└── IMPLEMENTATION_README.md      # このファイル
```

## トラブルシューティング

### API エラー

**問題**: `GEMINI_API_KEY is required`

**解決**:
```bash
export GEMINI_API_KEY='your-key-here'
# または
echo "GEMINI_API_KEY=your-key" > .env
```

**問題**: API rate limit exceeded

**解決**: 少し待ってから再実行。または `--from-stories` で続きから実行。

### 素材エラー

**問題**: `Metadata file not found`

**解決**: `source_materials/metadata/photo_descriptions.yaml` が存在するか確認。

**問題**: 素材使用率が75%未満

**解決**: ストーリー生成時により多くの素材を使用するよう調整される。再生成してください。

### 生成品質

**問題**: 生成されたストーリーが気に入らない

**解決**:
- `story_generator.py` のプロンプトを調整
- 再実行: `python generate_tourism_videos.py --stories-only`

**問題**: カメラワークが素材を変形させている

**解決**:
- `video_prompt_generator.py` のモーション強度を `low` に設定
- プロンプトに制約を追加強調

## 開発者向け情報

### モジュールの拡張

各モジュールは独立しており、拡張が容易です：

```python
# カスタム物語生成プロンプト
from story_generator import StoryGenerator

generator = StoryGenerator(project_root)
# _create_story_prompt() をオーバーライドして独自プロンプトを使用
```

### プラグインシステム（今後の拡張）

config.yaml の `plugins` セクションでプラグインを追加可能（将来実装）。

## コスト見積もり

### Gemini API 使用量
- 物語生成: 1回（約2,000トークン）
- 絵コンテ生成: 4回（各約1,500トークン）
- **合計**: 約8,000トークン ≈ $0.01以下（無料枠内）

### I2V動画生成（手動）
- Runway Gen-3: $0.05/秒 × 30秒 = **$1.50**
- Pika Labs: 無料プランで可能（1日250クレジット）

## ライセンスと注意事項

- このシステムは南紀白浜観光プロモーションコンペ用に作成
- 生成された動画は提供素材のライセンスに従う
- Gemini API、Runway、Pikaの利用規約を遵守してください

## サポート

問題が発生した場合：
1. `generated/` ディレクトリのレポートファイルを確認
2. エラーメッセージを読む
3. 各モジュールを個別に実行してどこで問題が起きているか特定

---

**作成日**: 2024-11-08
**バージョン**: 1.0
**プロジェクト**: nanki-shirahama-2024
