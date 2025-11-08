# 白浜観光AIアニメコンペ - プロジェクトINDEX

## 📚 ドキュメント一覧

### 🎯 START HERE
**まずはこれを読んでください:**
1. **[README.md](README.md)** - プロジェクト概要と素材配置の基本
2. **[PHOTO_PLACEMENT_GUIDE.md](PHOTO_PLACEMENT_GUIDE.md)** - 16枚の写真配置手順（ステップ・バイ・ステップ）

### 📋 詳細仕様
3. **[PROJECT_SPEC.md](PROJECT_SPEC.md)** - 完全な技術仕様書
   - コンペ要件
   - 4本の動画構成詳細
   - AIツール構成
   - ワークフロー
   - スケジュール

4. **[config.yaml](config.yaml)** - プロジェクト設定ファイル
   - 動画仕様
   - キャラクター設定
   - ビジュアルスタイル

### 📸 素材管理
5. **[MATERIAL_CLASSIFICATION.md](MATERIAL_CLASSIFICATION.md)** - 16枚の写真分類と分析
   - カテゴリ別の詳細
   - 動画別使用計画
   - 不足要素への対策

6. **[source_materials/metadata/photo_descriptions.yaml](source_materials/metadata/photo_descriptions.yaml)**
   - 各写真の詳細メタデータ
   - 使用推奨カット
   - 優先度情報

### 🚀 実行ガイド
7. **[QUICKSTART.md](QUICKSTART.md)** - クイックスタートガイド
   - 5分でスタート
   - コマンド実行例
   - トラブルシューティング

---

## 🎬 4本の動画概要

### Video 1: "出会いの予感" (10秒)
- **beach/** カテゴリ 3枚
- 白良浜との最初の出会い
- ワクワクする到着シーン

### Video 2: "自然の驚き" (10秒)
- **nature/** カテゴリ 3枚
- 円月島、三段壁、千畳敷
- 感動的な自然美

### Video 3: "体験の楽しみ" (10秒)
- **attractions/** + **culture/** 3枚
- 温泉体験と文化体験
- 癒しと発見

### Video 4: "もう一度来たい" (10秒)
- 印象的シーン再登場 3枚
- 思い出と余韻
- 花火で華やかなエンディング

---

## 📁 重要ファイル・フォルダ

```
projects/nanki-shirahama-2024/
├── 📄 ドキュメント（ここにいます）
├── 📸 source_materials/
│   └── raw/              ⭐ 写真をここに配置
│       ├── beach/        （5枚）
│       ├── nature/       （6枚）
│       ├── attractions/  （4枚）
│       └── culture/      （1枚）
├── 🎨 generated/         （自動生成される）
├── 🎬 submission/        （最終成果物）
└── 🔧 workspace/         （作業用）
```

---

## ⚡ クイックアクセス

### すぐに始める
```bash
# 1. 写真を配置（PHOTO_PLACEMENT_GUIDE.md 参照）
# 2. スキャン実行
python tools/material_manager.py \
  --project projects/nanki-shirahama-2024 \
  --scan --analyze --map
```

### 絵コンテ生成
```bash
python scripts/generate_storyboard_v2.py \
  --project nanki-shirahama-2024 \
  --video 1
```

---

## 🎯 制作フロー

1. **素材準備** → [PHOTO_PLACEMENT_GUIDE.md](PHOTO_PLACEMENT_GUIDE.md)
2. **スキャン** → `material_manager.py`
3. **絵コンテ** → `generate_storyboard_v2.py`
4. **キャラクター** → `create_character.py`
5. **背景アニメ化** → `anime_style_transfer.py`
6. **動画生成** → Runway Gen-3 / Pika Labs
7. **仕上げ** → 編集・音楽統合

---

## 💡 重要なポイント

### ✅ コンペ制約
- モチーフ改変禁止
- 写真をアニメ化背景として使用
- キャラクター追加OK

### 🎨 クリエイティブ方針
- **円月島の夕日** を最大活用（2回登場）
- **温泉体験** を主要コンテンツに
- **花火** でエンディング演出

### 📊 素材状況
- 全16枚を4本の動画に配分
- HD品質100%
- カテゴリバランス良好

---

## 📞 困ったら

1. **写真配置** → [PHOTO_PLACEMENT_GUIDE.md](PHOTO_PLACEMENT_GUIDE.md)
2. **全体仕様** → [PROJECT_SPEC.md](PROJECT_SPEC.md)
3. **クイックスタート** → [QUICKSTART.md](QUICKSTART.md)
4. **素材分類** → [MATERIAL_CLASSIFICATION.md](MATERIAL_CLASSIFICATION.md)

---

*プロジェクト準備完了！*
*次: [PHOTO_PLACEMENT_GUIDE.md](PHOTO_PLACEMENT_GUIDE.md) で写真を配置*
