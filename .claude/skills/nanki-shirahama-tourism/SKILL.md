---
name: nanki-shirahama-tourism
description: 南紀白浜の観光プロモーション動画のストーリーを生成。実際の16枚の素材写真（白良浜、円月島、三段壁、崎の湯など）を基に、4カット×10秒の観光動画ストーリーを作成。Claude解析済みメタデータ活用。
---

# 南紀白浜観光プロモーション動画スキル

白浜の実際の観光写真（16枚）を基に、「行ってみたい」と思わせる4カット構成の動画ストーリーを自動生成します。

## プロジェクトパス

**プロジェクトルート**: `/home/user/CreateMovie`
**白浜プロジェクト**: `/home/user/CreateMovie/projects/nanki-shirahama-2024`

### 重要なファイルパス
- **素材写真**: `projects/nanki-shirahama-2024/source_materials/raw/`
- **メタデータ**: `projects/nanki-shirahama-2024/source_materials/metadata/photo_descriptions.yaml`
- **設定ファイル**: `projects/nanki-shirahama-2024/config.yaml`
- **生成スクリプト**: `projects/nanki-shirahama-2024/generate_tourism_videos_v2.py`

## このスキルができること

✅ **実際の素材に基づいたストーリー生成**
- 16枚の実写真を活用（白良浜、円月島、三段壁、崎の湯、千畳敷、番所山隧道、熊野古道）
- Claude解析済みの詳細メタデータを参照
- 存在しない場所（アドベンチャーワールドなど）を除外

✅ **4カット構成（各10秒）**
- 4カット × 10秒 = 40秒コンテンツ（編集後約30秒）
- SNS向け（TikTok, Instagram Reels, YouTube Shorts）
- ストーリーアーク: 出会い → 自然の驚き → 体験の楽しみ → もう一度来たい

✅ **観光プロモーション最適化**
- 白浜の魅力を効果的に訴求
- カテゴリ別素材配分（beach, nature, attractions, culture）
- 提供写真のモチーフ変更禁止（コンペ制約遵守）

## 使い方

### 前提条件

このスキルを使用する際は、以下を確認してください：
- **作業ディレクトリ**: `/home/user/CreateMovie` （プロジェクトルート）
- **素材の配置**: `projects/nanki-shirahama-2024/source_materials/raw/` に16枚の写真
- **メタデータ**: `projects/nanki-shirahama-2024/source_materials/metadata/photo_descriptions.yaml` が存在

### 基本的な使い方

```
白浜プロジェクトで観光に行ってみたいと思わせる動画のストーリーを4カット構成で5つ考えて
```

このスキルは自動的に：
1. `/home/user/CreateMovie/projects/nanki-shirahama-2024` のメタデータを読み込み
2. 16枚の実際の素材リストを参照
3. Claude解析済みメタデータから詳細情報を取得
4. 4カット構成で複数のストーリー案を生成
5. 各カットに実際の場所（白良浜、円月島など）を割り当て

### より具体的な指定

```
白浜プロジェクトで夕日をテーマにした4カット構成の動画を作って
```

```
白浜プロジェクトで白良浜と円月島を中心にした4カット構成のストーリーを3つ考えて
```

## 利用可能な素材（16枚）

### Beach（5枚）
- **白良浜**: 白い砂浜、エメラルドグリーンの海、リゾートホテル（空撮、高台、ビーチレベル）
- **ビーチカフェ**: モダンな白い建物

### Nature（6枚）
- **三段壁**: 50m断崖絶壁、層状の岩
- **円月島**: 穴の開いた象徴的な岩の島（日中＋夕日シルエット）
- **千畳敷**: 波の浸食で作られた平らな岩の地形
- **番所山隧道**: 歴史的なレンガのトンネル

### Attractions（4枚）
- **崎の湯**: 海辺の露天風呂、ダイナミックな波
- **白良浜花火**: 夜の花火大会

### Culture（1枚）
- **熊野古道富田坂**: 世界遺産、石段の巡礼路

## 技術仕様

### プロジェクト構造
```
/home/user/CreateMovie/projects/nanki-shirahama-2024/
├── source_materials/
│   ├── raw/                    # 16枚の実写真
│   │   ├── beach/              # 白良浜（5枚）
│   │   ├── nature/             # 円月島、三段壁、千畳敷など（6枚）
│   │   ├── attractions/        # 崎の湯、花火（4枚）
│   │   └── culture/            # 熊野古道（1枚）
│   └── metadata/
│       └── photo_descriptions.yaml  # Claude解析メタデータ
├── config.yaml                 # プロジェクト設定（4カット構成）
└── generate_tourism_videos_v2.py   # 生成スクリプト
```

### 実行スクリプト（Pythonで実行する場合）
```bash
cd /home/user/CreateMovie/projects/nanki-shirahama-2024
python generate_tourism_videos_v2.py "ストーリーの説明"
```

または絶対パス指定：
```bash
python /home/user/CreateMovie/projects/nanki-shirahama-2024/generate_tourism_videos_v2.py "ストーリーの説明"
```

### 画像生成
- **ツール**: Gemini 2.5 Flash Image
- **参照画像**: 最大3枚まで使用可能
- **コスト**: $0.039/画像

### 動画化（I2V）
- **推奨**: Sora 2（$0.10/秒、720p）
- **代替**: Veo 3.1（$0.10-0.40/秒）
- **総コスト**: 約$4.16-7（4カット分）

## Claude解析メタデータ活用

各素材には以下の詳細情報が記録されています：

```yaml
- filename: 円月島夕日１.jpeg
  location: 円月島
  description: 円月島の夕景。夕日が島の穴を通過するシルエット、
               オレンジ・ピンク・金色のグラデーション空、海面の反射。
  time_of_day: sunset
  weather: clear
  main_subject: 円月島と夕日
  composition: silhouette
  color_tone: orange_pink_gold
```

## 制約事項

### 素材制約（コンペルール）
- ⚠️ 提供写真のモチーフ（被写体）変更**禁止**
- ✅ 写真の拡大・縮小・トリミング**許可**
- ✅ アニメスタイルへの変換**許可**（構図保持）
- ✅ キャラクターの追加**許可**（背景として使用）

### カメラワーク制約
- ✅ 使用可能: Pan, Zoom, Tilt
- ⚠️ 禁止: 素材の形状を変形させるモーション

## 出力形式

### ストーリー構成
各動画（4カット × 10秒）：
1. **出会いの予感** (beach): 白良浜の美しさ
2. **自然の驚き** (nature): 円月島、三段壁、千畳敷
3. **体験の楽しみ** (attractions/culture): 崎の湯、熊野古道
4. **もう一度来たい** (beach/nature): 印象的シーン再登場

### 生成物
```
generated_v2/
├── video1/
│   ├── storyboard.json         # 絵コンテデータ
│   └── i2v_prompts.json        # I2V生成用プロンプト
├── video2/
├── video3/
└── video4/
```

## 参考リンク

- プロジェクト仕様書: `/home/user/CreateMovie/projects/nanki-shirahama-2024/docs/プロジェクト仕様書.md`
- 素材メタデータ: `/home/user/CreateMovie/projects/nanki-shirahama-2024/source_materials/metadata/photo_descriptions.yaml`
- 設定ファイル: `/home/user/CreateMovie/projects/nanki-shirahama-2024/config.yaml`
- 素材写真: `/home/user/CreateMovie/projects/nanki-shirahama-2024/source_materials/raw/`

## トラブルシューティング

### プロジェクトが見つからない
→ **作業ディレクトリを確認してください**: `/home/user/CreateMovie`
→ メタデータファイルの絶対パス: `/home/user/CreateMovie/projects/nanki-shirahama-2024/source_materials/metadata/photo_descriptions.yaml`

### 存在しない場所が生成される
→ このスキルは実際の素材リストをプロンプトに含めるため、存在しない場所（アドベンチャーワールドなど）の生成を自動的に防ぎます。
→ メタデータが正しく読み込まれているか確認: `photo_descriptions.yaml` が存在するか

### カット数が4でない
→ プロンプトに「4カット構成」を明記してください。自動検出されます。
→ 例: 「白浜プロジェクトで**4カット構成**のストーリーを5つ考えて」

### 素材が見つからない
→ 素材ディレクトリを確認: `/home/user/CreateMovie/projects/nanki-shirahama-2024/source_materials/raw/`
→ 16枚の写真が以下のカテゴリに配置されているか確認:
  - `beach/` (5枚)
  - `nature/` (6枚)
  - `attractions/` (4枚)
  - `culture/` (1枚)
