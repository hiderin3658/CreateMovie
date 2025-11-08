# 白浜観光AIアニメコンペ プロジェクト

> **バージョン 2.0** - コアシステム統合版
> CreateMovieプロジェクトのコアシステムを使用した観光動画生成システム

## 🎯 プロジェクト概要

提供された16枚の観光写真から、4本の10秒動画（合計30秒）の絵コンテと動画プロンプトを自動生成します。

### 設計方針（重要）

⚠️ **今後の開発における重要な原則**:

1. **コアシステムの活用**: すべての機能追加は、**CreateMovieプロジェクトのコアシステム (`core/`) を基盤として実装**すること
2. **プラグインアーキテクチャ**: プロジェクト固有の機能は、**プラグインとして実装**すること
3. **Claude Skills 対応**: すべての機能は、**Claude Code の Claude Skills として動作する前提で設計**すること

詳細は [`docs/開発ガイドライン.md`](docs/開発ガイドライン.md) を参照してください。

---

## 📚 ドキュメント

### エントリーポイント
- **README.md** (このファイル) - プロジェクト概要、クイックスタート、素材配置ガイド

### 詳細ドキュメント (`docs/` ディレクトリ)

| ドキュメント | 内容 |
|-------------|------|
| [`開発ガイドライン.md`](docs/開発ガイドライン.md) | **設計方針、アーキテクチャ、開発ルール（必読）** |
| [`コアシステム統合ガイド.md`](docs/コアシステム統合ガイド.md) | コアシステムを使った実装方法 |
| [`プロジェクト仕様書.md`](docs/プロジェクト仕様書.md) | 詳細な仕様、要件、ワークフロー |
| [`クイックスタート.md`](docs/クイックスタート.md) | 最速で始めるための手順 |
| [`素材分類ガイド.md`](docs/素材分類ガイド.md) | 写真の分類基準 |
| [`写真配置ガイド.md`](docs/写真配置ガイド.md) | 写真の配置方法 |
| [`実装ガイド（レガシー版）.md`](docs/実装ガイド（レガシー版）.md) | 旧スタンドアロン版の実装（参考） |

---

## 🚀 クイックスタート

### セットアップ

```bash
# 1. 依存パッケージのインストール
pip install -r ../../requirements-core.txt
pip install -r requirements.txt

# 2. API キー設定
export GEMINI_API_KEY='your-api-key-here'
```

### 実行

```bash
# 4本の観光動画を生成
python generate_tourism_videos_v2.py "白浜の観光体験"
```

詳細は [`docs/クイックスタート.md`](docs/クイックスタート.md) を参照してください。

---

## 📁 素材配置ガイド

### 提供写真の配置先

白浜の観光写真16枚を以下のフォルダに分類して配置してください：

```
source_materials/raw/
├── beach/              # 白良浜、海岸線の写真（4-5枚）
├── nature/             # 円月島、千畳敷、三段壁など自然景観（4-5枚）
├── attractions/        # アドベンチャーワールド、温泉施設など（4-5枚）
└── culture/            # 地元グルメ、文化施設など（2-3枚）
```

### 分類基準

#### 🏖️ beach/
- 白良浜の砂浜
- 海岸線の風景
- 波打ち際
- ビーチからの海の眺め

**使用予定動画**: Video 1「出会いの予感」、Video 4「もう一度来たい」

---

#### 🌊 nature/
- 円月島（夕日のシルエット）
- 千畳敷（岩場の景観）
- 三段壁（断崖絶壁）
- その他の自然の造形美

**使用予定動画**: Video 2「自然の驚き」

---

#### 🎡 attractions/
- アドベンチャーワールド（パンダなど）
- 温泉施設（露天風呂、浴場）
- ホテル・旅館の外観や内装
- 観光スポット

**使用予定動画**: Video 3「体験の楽しみ」

---

#### 🍱 culture/
- 地元グルメ（海鮮、クエ料理など）
- 土産物、特産品
- 歴史的建造物
- 地域の文化的要素

**使用予定動画**: Video 3「体験の楽しみ」

---

## 📝 写真の命名規則

ファイル名は以下の形式を推奨：

```
{category}_{sequence}_{description}.jpg

例：
- beach_01_shirarahama_wide.jpg
- nature_01_engetsuto_sunset.jpg
- attractions_01_adventure_world_panda.jpg
- culture_01_local_seafood.jpg
```

---

## 🎯 写真選定のポイント

### 優先度が高い写真
1. **白良浜の全景** - メインビジュアルとして使用
2. **円月島の夕暮れ** - 印象的なシーンとして使用
3. **アドベンチャーワールド** - 体験価値を訴求
4. **温泉シーン** - リラックス体験を表現

### 写真の品質要件
- **解像度**: 最低 1920x1080 (Full HD)
- **フォーカス**: シャープでクリアな画像
- **明るさ**: 適切な露出
- **構図**: 三分割法などの基本構図
- **被写体**: 明確なモチーフ

---

## 📊 素材使用計画

| 動画 | テーマ | 使用カテゴリ | 写真枚数 |
|-----|--------|-------------|---------|
| Video 1 | 出会いの予感 | beach | 3-4枚 |
| Video 2 | 自然の驚き | nature | 3-4枚 |
| Video 3 | 体験の楽しみ | attractions + culture | 3-4枚 |
| Video 4 | もう一度来たい | beach + nature (再登場) | 3-4枚 |
| **合計** | - | - | **12-16枚** |

---

## 🔄 ワークフロー

### Step 1: 写真の配置
```bash
# 写真を適切なフォルダに配置
cp /path/to/your/photos/beach*.jpg source_materials/raw/beach/
cp /path/to/your/photos/nature*.jpg source_materials/raw/nature/
cp /path/to/your/photos/attractions*.jpg source_materials/raw/attractions/
cp /path/to/your/photos/culture*.jpg source_materials/raw/culture/
```

### Step 2: メタデータ記録
```bash
# 写真のメタデータを自動生成
python tools/generate_metadata.py \
  --project nanki-shirahama-2024
```

### Step 3: 素材解析
```bash
# AI解析を実行
python tools/analyze_materials.py \
  --project nanki-shirahama-2024 \
  --output source_materials/analyzed/
```

### Step 4: 絵コンテ生成
```bash
# 各動画の絵コンテを生成
python scripts/generate_storyboard_v2.py \
  --project nanki-shirahama-2024 \
  --video 1
```

---

## 📷 メタデータファイル

`source_materials/metadata/photo_descriptions.yaml` に以下の情報を記録：

```yaml
photos:
  - filename: "beach_01_shirarahama_wide.jpg"
    category: "beach"
    location: "白良浜"
    description: "白い砂浜の全景、遠くに海と空"
    time_of_day: "昼"
    weather: "晴れ"
    main_subject: "砂浜、海"
    composition: "rule_of_thirds"
    color_tone: "bright, blue sky"
    assigned_video: 1
    usage_notes: "オープニングシーンとして使用"

  - filename: "nature_01_engetsuto_sunset.jpg"
    category: "nature"
    location: "円月島"
    description: "夕日に照らされた円月島のシルエット"
    time_of_day: "夕方"
    weather: "晴れ"
    main_subject: "円月島、夕日"
    composition: "centered"
    color_tone: "warm, orange sunset"
    assigned_video: 2
    usage_notes: "感動的なシーンとして使用"
```

---

## 🎨 アニメ化の方針

### 保持すべき要素
- ✅ 建物・岩場などの形状
- ✅ 海・空の配置
- ✅ 全体的な構図
- ✅ 認識可能なランドマーク

### 変更可能な要素
- ✅ 色調（アニメ風に調整）
- ✅ テクスチャ（手描き風）
- ✅ 細部のディテール
- ✅ 光と影の表現

### 変更禁止
- ❌ モチーフの形状変更
- ❌ ランドマークの改変
- ❌ 写真に写っていない要素の追加

---

## ✅ チェックリスト

### 素材準備
- [ ] 写真16枚を確認
- [ ] 各カテゴリに4枚ずつ分類
- [ ] ファイル名をわかりやすく変更
- [ ] 解像度・品質を確認
- [ ] バックアップを作成

### メタデータ
- [ ] photo_descriptions.yaml を作成
- [ ] 各写真の説明を記入
- [ ] 使用予定の動画を割り当て
- [ ] 特記事項を記録

### 品質確認
- [ ] 全写真がFull HD以上
- [ ] ブレやボケがない
- [ ] 適切な明るさ
- [ ] 主要被写体が明確
- [ ] 構図が整っている

---

## 📞 サポート

問題が発生した場合：
1. [`docs/開発ガイドライン.md`](docs/開発ガイドライン.md) で設計方針を確認
2. [`docs/コアシステム統合ガイド.md`](docs/コアシステム統合ガイド.md) で実装方法を確認
3. [`docs/プロジェクト仕様書.md`](docs/プロジェクト仕様書.md) で仕様を確認
4. `config.yaml` の設定を確認
5. エラーログを確認

---

## 📂 プロジェクト構成

```
nanki-shirahama-2024/
├── README.md                          # このファイル（エントリーポイント）
├── config.yaml                        # プロジェクト設定
├── requirements.txt                   # 依存パッケージ
│
├── docs/                              # 📚 ドキュメント集約
│   ├── 開発ガイドライン.md             # 設計方針、アーキテクチャ
│   ├── コアシステム統合ガイド.md
│   ├── プロジェクト仕様書.md
│   ├── クイックスタート.md
│   ├── 素材分類ガイド.md
│   └── 写真配置ガイド.md
│
├── plugins/                           # 🔌 プラグイン
│   └── shirahama_tourism_plugin.py    # 南紀白浜専用プラグイン
│
├── generate_tourism_videos_v2.py      # ⚡ メインスクリプト（v2.0）
├── material_manager.py                # 素材管理
│
├── source_materials/                  # 📷 素材（16枚の観光写真）
│   ├── raw/                           # オリジナル写真
│   ├── metadata/                      # メタデータ
│   └── analyzed/                      # 解析結果
│
├── generated_v2/                      # 📤 生成ファイル（実行後に作成）
│   ├── video1/
│   ├── video2/
│   ├── video3/
│   └── video4/
│
└── legacy/                            # 📦 旧スタンドアロン版（非推奨）
```

---

*Last updated: 2024-11-08*
*Version: 2.0 (コアシステム統合版)*
*Project: nanki-shirahama-2024*
