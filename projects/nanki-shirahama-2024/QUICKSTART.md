# 白浜プロジェクト クイックスタートガイド

## 🚀 5分でスタート

### Step 1: 写真を配置（2分）

白浜の写真16枚を以下のフォルダに分類して配置：

```bash
cd projects/nanki-shirahama-2024/source_materials/raw/

# 例: 写真をコピー
cp ~/Downloads/shirahama_beach*.jpg beach/
cp ~/Downloads/shirahama_nature*.jpg nature/
cp ~/Downloads/shirahama_panda*.jpg attractions/
cp ~/Downloads/shirahama_food*.jpg culture/
```

**分類の目安:**
- `beach/` → 白良浜、海の写真
- `nature/` → 円月島、千畳敷、三段壁
- `attractions/` → アドベンチャーワールド、温泉
- `culture/` → グルメ、文化施設

---

### Step 2: 素材をスキャン（30秒）

```bash
cd /Users/hiderinchan/Documents/Claude/CreateMovie/ai-video-storyboard

python tools/material_manager.py \
  --project projects/nanki-shirahama-2024 \
  --scan \
  --analyze \
  --map
```

**出力:**
- ✅ 写真の枚数確認
- ✅ カテゴリ別の集計
- ✅ 品質チェック（解像度確認）
- ✅ 動画への自動マッピング

---

### Step 3: 絵コンテ生成（各1分 × 4本）

#### Video 1: 出会いの予感
```bash
python scripts/generate_storyboard_v2.py \
  --project nanki-shirahama-2024 \
  --video 1 \
  --title "出会いの予感" \
  --duration 10 \
  --theme "arrival"
```

#### Video 2: 自然の驚き
```bash
python scripts/generate_storyboard_v2.py \
  --project nanki-shirahama-2024 \
  --video 2 \
  --title "自然の驚き" \
  --duration 10 \
  --theme "nature"
```

#### Video 3: 体験の楽しみ
```bash
python scripts/generate_storyboard_v2.py \
  --project nanki-shirahama-2024 \
  --video 3 \
  --title "体験の楽しみ" \
  --duration 10 \
  --theme "experience"
```

#### Video 4: もう一度来たい
```bash
python scripts/generate_storyboard_v2.py \
  --project nanki-shirahama-2024 \
  --video 4 \
  --title "もう一度来たい" \
  --duration 10 \
  --theme "farewell"
```

---

## 📂 生成されるファイル

```
projects/nanki-shirahama-2024/
├── source_materials/
│   ├── analyzed/
│   │   ├── material_analysis.json      # 素材解析結果
│   │   └── material_mapping.json       # 動画マッピング
│   └── metadata/
│       └── photo_descriptions.yaml     # 写真メタデータ
│
└── generated/
    └── storyboards/
        ├── video1_storyboard.json
        ├── video2_storyboard.json
        ├── video3_storyboard.json
        └── video4_storyboard.json
```

---

## 🎨 次のステップ

### 1. 絵コンテ確認
```bash
# JSONファイルを確認
cat projects/nanki-shirahama-2024/generated/storyboards/video1_storyboard.json
```

### 2. キャラクター作成
```bash
python tools/create_character.py \
  --project nanki-shirahama-2024 \
  --style anime \
  --description "young woman, 20 years old, tourist"
```

### 3. 背景アニメ化
```bash
python tools/anime_style_transfer.py \
  --input projects/nanki-shirahama-2024/source_materials/raw \
  --output projects/nanki-shirahama-2024/generated/backgrounds \
  --preserve-composition
```

### 4. 動画生成
- 各絵コンテをもとに Runway Gen-3 / Pika Labs で生成
- キャラクターと背景を合成
- 音楽を追加

---

## 💡 よくある質問

### Q: 写真が16枚より少ない場合は？
**A:** 最低12枚あれば制作可能です。不足分は:
- 既存写真の別アングル生成
- AIで背景生成（Midjourney等）

### Q: 写真の品質が低い場合は？
**A:** AI超解像で品質向上:
```bash
python tools/upscale_image.py \
  --input source_materials/raw/beach/low_quality.jpg \
  --scale 2
```

### Q: カテゴリ分類が難しい
**A:** AI自動分類を使用:
```bash
python tools/auto_categorize.py \
  --input source_materials/raw
```

### Q: モチーフが改変されてしまう
**A:** `denoising_strength` を調整:
- 推奨値: 0.3-0.5
- 低いほど元の画像を保持
- 高いほどアニメ風に変化

---

## ✅ チェックリスト

### 素材準備
- [ ] 写真16枚を確認
- [ ] カテゴリ別に分類
- [ ] `material_manager.py` 実行
- [ ] 解析レポート確認

### 絵コンテ生成
- [ ] Video 1 生成完了
- [ ] Video 2 生成完了
- [ ] Video 3 生成完了
- [ ] Video 4 生成完了

### 品質確認
- [ ] 各動画10秒ピッタリ
- [ ] ストーリーアークが繋がっている
- [ ] 写真のモチーフが保持されている
- [ ] キャラクターが一貫している

---

## 📞 トラブルシューティング

### エラー: "材料が見つかりません"
```bash
# フォルダ構造を確認
ls -la projects/nanki-shirahama-2024/source_materials/raw/
```

### エラー: "メタデータが読み込めません"
```bash
# メタデータを再生成
python tools/material_manager.py \
  --project projects/nanki-shirahama-2024 \
  --scan
```

### 生成が遅い
- 画像サイズを確認（大きすぎる場合はリサイズ）
- バッチ処理に変更
- GPUを使用

---

## 🎯 完成までの目安時間

| フェーズ | 時間 | 内容 |
|---------|------|------|
| 素材準備 | 30分 | 写真整理、分類、スキャン |
| 絵コンテ | 1時間 | 4本の絵コンテ生成 |
| キャラクター | 1時間 | デザイン、ポーズ生成 |
| 背景制作 | 2時間 | アニメ化、品質調整 |
| 動画生成 | 4時間 | I2V変換、合成 |
| 編集 | 2時間 | 仕上げ、音楽追加 |
| **合計** | **10-12時間** | 1-2日で完成 |

---

*Last updated: 2024-11-08*
*Project: nanki-shirahama-2024*
