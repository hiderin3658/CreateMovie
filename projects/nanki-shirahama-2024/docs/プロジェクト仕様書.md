# 白浜観光AIアニメコンペ プロジェクト仕様書

## プロジェクト概要

### コンペティション情報
- **タイトル**: 行ってみたい白浜
- **テーマ**: 白浜の観光写真をベースに30秒アニメを制作
- **目的**: 和歌山・白浜の観光資源をAIアニメで表現し、若年層から海外観光客まで白浜の魅力を拡散
- **期待効果**: AIの力で地方創生を支援

### 制作要件

#### 動画仕様
- **総時間**: 30秒
- **構成**: 10秒 × 4本の独立した動画
- **形式**: ショート動画（縦型 9:16 推奨）
- **配信**: SNS（TikTok、Instagram Reels、YouTube Shorts）

#### 素材制約
- **提供素材**: 白浜の観光写真 16枚
- **使用ルール**:
  - 写真に映っているモチーフは変更（改変）禁止
  - 写真をアニメ化して背景として使用
  - 登場人物を追加可能
  - 「白浜に行ってみたい」と思わせる演出

#### クリエイティブ要件
- 登場人物: 観光客（若者、カップル、ファミリー等）
- 視点: 観光体験を疑似体験できる一人称または三人称
- 感情: ワクワク、発見、感動、癒し
- 訴求: 「行ってみたい」「体験したい」という旅行意欲の喚起

---

## 動画構成案

### 4本のストーリーアーク

#### Video 1: "出会いの予感" (10秒)
**テーマ**: 白浜との最初の出会い
- **0-3秒**: 白良浜の白い砂浜（遠景）
- **3-7秒**: 主人公が砂浜を歩く（足元クローズアップ → 全身）
- **7-10秒**: 海を見つめる主人公（期待感）

**使用素材**: 白良浜、海岸線の写真 3-4枚

**ムード**: 期待、ワクワク
**音楽**: 爽やか、軽快なイントロ

---

#### Video 2: "自然の驚き" (10秒)
**テーマ**: 白浜の自然美との出会い
- **0-3秒**: 円月島のシルエット（夕暮れ）
- **3-7秒**: 主人公が写真を撮る動作
- **7-10秒**: 千畳敷の岩場をゆっくりパン

**使用素材**: 円月島、千畳敷、三段壁など自然景観 3-4枚

**ムード**: 感動、畏敬
**音楽**: 壮大、エモーショナル

---

#### Video 3: "体験の楽しみ" (10秒)
**テーマ**: アクティビティと地域体験
- **0-3秒**: アドベンチャーワールドのパンダ
- **3-7秒**: 主人公が温泉に浸かる（露天風呂）
- **7-10秒**: 地元グルメを食べる笑顔

**使用素材**: 観光施設、温泉、グルメの写真 3-4枚

**ムード**: 楽しい、満足
**音楽**: ポップ、リズミカル

---

#### Video 4: "もう一度来たい" (10秒)
**テーマ**: 白浜の魅力の集大成
- **0-3秒**: 夕日に染まる白良浜
- **3-7秒**: 主人公が振り返る（複数の思い出シーンの重ね合わせ）
- **7-10秒**: 「また来たい」という想いを込めて手を振る

**使用素材**: 印象的なシーンの再登場 3-4枚

**ムード**: 余韻、感謝、希望
**音楽**: エンディング、感動的

---

## 技術仕様

### 画像処理パイプライン

```
提供写真 → 背景アニメ化 → キャラクター合成 → モーション適用 → 最終レンダリング
   ↓           ↓              ↓                ↓             ↓
 16枚      AIアニメ化      Stable Diffusion    I2V変換      編集統合
         (style transfer)   (inpainting)      (Runway/Pika)
```

### 使用AIツール

1. **背景アニメ化**
   - ツール: Stable Diffusion (LoRA: anime style)
   - プロンプト: "anime style, preserving composition, [location description]"
   - 設定: img2img, denoising strength 0.3-0.5

2. **キャラクター生成**
   - ツール: Stable Diffusion XL / Midjourney
   - キャラクター一貫性: ControlNet (reference)
   - ポーズ制御: ControlNet (OpenPose)

3. **動画化**
   - ツール: Runway Gen-3 / Pika Labs / Stable Video Diffusion
   - モーション: Camera movement + character animation
   - 推奨モデル: Runway Gen-3 (高品質、カメラワーク制御)

4. **音楽**
   - ツール: Suno AI
   - スタイル: J-Pop, Cinematic, 爽やか
   - BPM: 120-140 (Video 1-3), 90-100 (Video 4)

---

## 素材管理仕様

### フォルダ構造

```
projects/nanki-shirahama-2024/
├── source_materials/           # 提供素材
│   ├── raw/                    # オリジナル写真（16枚）
│   │   ├── beach/              # 白良浜系（4-5枚）
│   │   ├── nature/             # 自然景観（4-5枚）
│   │   ├── attractions/        # 観光施設（4-5枚）
│   │   └── culture/            # 文化・グルメ（2-3枚）
│   │
│   ├── analyzed/               # AI解析結果
│   │   └── material_analysis.json
│   │
│   └── metadata/               # メタデータ
│       └── photo_descriptions.yaml
│
├── generated/                  # 生成物
│   ├── backgrounds/            # アニメ化背景
│   │   ├── video1/
│   │   ├── video2/
│   │   ├── video3/
│   │   └── video4/
│   │
│   ├── characters/             # キャラクター素材
│   │   └── tourist_character_sheet.png
│   │
│   ├── storyboards/            # 絵コンテ
│   │   ├── video1_storyboard.json
│   │   ├── video2_storyboard.json
│   │   ├── video3_storyboard.json
│   │   └── video4_storyboard.json
│   │
│   ├── frames/                 # 最終フレーム
│   │   ├── video1/
│   │   ├── video2/
│   │   ├── video3/
│   │   └── video4/
│   │
│   └── music/                  # 音楽プロンプト
│       └── music_prompts.json
│
├── workspace/                  # 作業用
│   ├── composites/             # 合成作業中
│   ├── tests/                  # テスト生成
│   └── cache/                  # キャッシュ
│
├── submission/                 # 提出用
│   ├── final_videos/           # 最終動画
│   │   ├── video1_encounter.mp4
│   │   ├── video2_nature.mp4
│   │   ├── video3_experience.mp4
│   │   └── video4_farewell.mp4
│   │
│   ├── combined/               # 統合版
│   │   └── shirahama_complete_30s.mp4
│   │
│   └── documents/              # 提出書類
│       ├── concept_doc.pdf
│       └── material_usage_report.pdf
│
└── config.yaml                 # プロジェクト設定
```

### 素材分類基準

#### カテゴリ分類
```yaml
categories:
  beach:
    - 白良浜の砂浜
    - 海岸線
    - 波打ち際
    priority: high
    video_assignment: [1, 4]

  nature:
    - 円月島
    - 千畳敷
    - 三段壁
    - 自然の岩場
    priority: high
    video_assignment: [2]

  attractions:
    - アドベンチャーワールド
    - 温泉施設
    - ホテル・旅館
    priority: medium
    video_assignment: [3]

  culture:
    - 地元グルメ
    - 土産物
    - 歴史的建造物
    priority: medium
    video_assignment: [3]
```

#### 素材品質評価
```yaml
quality_criteria:
  resolution: min 1920x1080
  composition: rule_of_thirds preferred
  lighting: natural light preferred
  clarity: sharp focus required
  usage_restrictions:
    - no_logo_alteration
    - preserve_landmarks
    - maintain_original_composition
```

---

## キャラクター設計

### メインキャラクター: "旅する少女"

**ビジュアル設定**:
- 年齢: 18-22歳（大学生風）
- 髪型: ロングヘア、ポニーテール
- 服装: カジュアル（Tシャツ + デニム or ワンピース）
- 持ち物: スマホ、カメラ、バックパック
- 表情: 明るく好奇心旺盛

**キャラクター一貫性**:
```python
character_prompt = """
anime style, young woman, 20 years old,
long brown hair in ponytail,
wearing casual summer clothes (white t-shirt, denim shorts),
carrying small backpack,
bright smile, energetic expression,
tourist visiting beach resort,
consistent character design across all scenes
"""
```

**ControlNet設定**:
- Reference: キャラクターシート画像
- Weight: 0.8-1.0
- Style: Anime/illustration

---

## ワークフロー

### Phase 1: 素材準備（1日目）

1. **素材整理**
   ```bash
   python tools/organize_materials.py \
     --input /path/to/shirahama_photos \
     --output projects/nanki-shirahama-2024/source_materials/raw
   ```

2. **素材解析**
   ```bash
   python tools/analyze_materials.py \
     --project nanki-shirahama-2024
   ```

3. **カテゴリ分類**
   - AI自動分類
   - 手動確認・調整

### Phase 2: キャラクター作成（1日目）

1. **キャラクターデザイン**
   ```bash
   python tools/create_character.py \
     --style anime \
     --age 20 \
     --output projects/nanki-shirahama-2024/generated/characters/
   ```

2. **ポーズバリエーション生成**
   - 歩く、立つ、座る
   - 写真を撮る、食べる
   - 振り返る、手を振る

### Phase 3: 背景アニメ化（2日目）

1. **写真のアニメ化**
   ```bash
   python tools/anime_style_transfer.py \
     --input projects/nanki-shirahama-2024/source_materials/raw \
     --output projects/nanki-shirahama-2024/generated/backgrounds \
     --style anime \
     --preserve-composition true
   ```

2. **品質チェック**
   - モチーフの保持確認
   - 色調の統一性確認

### Phase 4: 絵コンテ生成（2日目）

1. **Video 1-4の絵コンテ作成**
   ```bash
   python scripts/generate_storyboard_v2.py \
     --project nanki-shirahama-2024 \
     --video-id 1 \
     --theme tourism-shirahama
   ```

2. **素材マッピング**
   - 各カットに最適な背景を割り当て
   - キャラクター配置を決定

### Phase 5: 合成とレンダリング（3日目）

1. **キャラクター合成**
   ```bash
   python tools/composite_character.py \
     --storyboard projects/nanki-shirahama-2024/generated/storyboards/video1_storyboard.json \
     --character projects/nanki-shirahama-2024/generated/characters/ \
     --backgrounds projects/nanki-shirahama-2024/generated/backgrounds/
   ```

2. **I2V変換**
   - Runway Gen-3で動画化
   - カメラワーク適用

### Phase 6: 編集と完成（4日目）

1. **動画編集**
   - 各10秒動画の仕上げ
   - トランジション追加
   - テキストオーバーレイ

2. **音楽統合**
   - Suno AIで生成した音楽を配置
   - タイミング調整

3. **最終レビュー**
   - 30秒統合版作成
   - 提出書類準備

---

## 制作スケジュール

| 日程 | タスク | 成果物 |
|-----|--------|--------|
| Day 1 | 素材整理・解析、キャラクター作成 | 素材分類完了、キャラクターシート |
| Day 2 | 背景アニメ化、絵コンテ生成 | アニメ背景16枚、絵コンテ4本 |
| Day 3 | 合成・I2V変換 | 動画フレーム、テスト動画 |
| Day 4 | 編集・仕上げ・提出準備 | 最終動画4本、提出書類 |

---

## チェックリスト

### 制作前確認
- [ ] 提供写真16枚の受領確認
- [ ] 各写真のメタデータ記録
- [ ] コンペ規約の最終確認
- [ ] AIツールのライセンス確認

### 制作中確認
- [ ] モチーフの改変がないか確認
- [ ] キャラクター一貫性の維持
- [ ] 各動画10秒ピッタリに調整
- [ ] 縦型フォーマット (9:16) 確認

### 提出前確認
- [ ] 全4本の動画品質チェック
- [ ] 音楽の著作権クリア確認
- [ ] ファイル形式・サイズ確認
- [ ] 素材使用レポート作成
- [ ] コンセプトドキュメント作成

---

## リスクと対策

| リスク | 発生確率 | 影響度 | 対策 |
|--------|---------|--------|-----|
| アニメ化でモチーフが変形 | 中 | 高 | denoising strength調整、手動修正 |
| キャラクター一貫性が崩れる | 中 | 中 | ControlNet強化、複数生成から選択 |
| I2V変換が不自然 | 高 | 中 | モーション強度調整、カット分割 |
| 制作時間不足 | 中 | 高 | 優先順位付け、段階的完成 |
| API制限到達 | 低 | 中 | 事前テスト、バックアッププラン |

---

## 予算見積もり

### AI生成コスト
- Runway Gen-3: $0.05/秒 × 40秒 = $2.00
- Suno AI: 無料プラン
- Stable Diffusion: ローカル実行（無料）

### 総コスト: 約$2-5 (API制限回避用の追加クレジット含む)

---

*プロジェクト仕様書 v1.0*
*作成日: 2024-11-08*
*プロジェクトID: nanki-shirahama-2024*
