# 📸 白浜写真16枚 配置ガイド

## ステップ・バイ・ステップ

### Step 1: 写真の準備

16枚の写真を以下のように**リネーム**してください：

#### 🏖️ Beach（5枚）
```
白良浜（パラソル） → beach_01_shirahama_parasol.jpg
白良浜（エメラルドの海） → beach_02_shirahama_emerald_sea.jpg
白良浜（円月島見える） → beach_03_shirahama_with_island.jpg
白良浜（俯瞰ビュー） → beach_04_shirahama_aerial_view.jpg
白良浜（三日月型全景） → beach_05_shirahama_crescent_bay.jpg
```

#### 🌊 Nature（6枚）
```
円月島（夕陽） → nature_01_engetsuto_sunset.jpg        ⭐最重要
円月島（昼） → nature_02_engetsuto_daytime.jpg
三段壁 → nature_03_sandanbeki_cliff.jpg
世界遺産（熊野古道富田坂） → nature_04_bansho_tunnel.jpg
千畳敷（波打つ岩場） → nature_05_senjojiki_rocks_1.jpg
千畳敷（平らな岩場） → nature_06_senjojiki_rocks_2.jpg
```

#### 🎡 Attractions（4枚）
```
崎の湯（足湯） → attractions_01_sakinoyu_footbath.jpg
崎の湯（露天風呂・海側） → attractions_02_sakinoyu_seaside.jpg
崎の湯（露天風呂・岩場） → attractions_03_sakinoyu_rocks.jpg
花火（白良浜） → attractions_04_fireworks_shirahama.jpg
```

#### 🍱 Culture（1枚）
```
世界遺産（熊野古道富田坂） → culture_01_kumano_kodo_tomita.jpg
```

**注意:** 熊野古道の写真は nature と culture のどちらにも配置可能です。
今回は **culture/** に配置することを推奨します。

---

### Step 2: フォルダへ配置

#### macOS / Linux の場合:

```bash
cd /Users/hiderinchan/Documents/Claude/CreateMovie/ai-video-storyboard
cd projects/nanki-shirahama-2024/source_materials/raw

# beach フォルダに5枚配置
cp ~/Downloads/beach_01_shirahama_parasol.jpg beach/
cp ~/Downloads/beach_02_shirahama_emerald_sea.jpg beach/
cp ~/Downloads/beach_03_shirahama_with_island.jpg beach/
cp ~/Downloads/beach_04_shirahama_aerial_view.jpg beach/
cp ~/Downloads/beach_05_shirahama_crescent_bay.jpg beach/

# nature フォルダに6枚配置
cp ~/Downloads/nature_01_engetsuto_sunset.jpg nature/
cp ~/Downloads/nature_02_engetsuto_daytime.jpg nature/
cp ~/Downloads/nature_03_sandanbeki_cliff.jpg nature/
cp ~/Downloads/nature_04_bansho_tunnel.jpg nature/
cp ~/Downloads/nature_05_senjojiki_rocks_1.jpg nature/
cp ~/Downloads/nature_06_senjojiki_rocks_2.jpg nature/

# attractions フォルダに4枚配置
cp ~/Downloads/attractions_01_sakinoyu_footbath.jpg attractions/
cp ~/Downloads/attractions_02_sakinoyu_seaside.jpg attractions/
cp ~/Downloads/attractions_03_sakinoyu_rocks.jpg attractions/
cp ~/Downloads/attractions_04_fireworks_shirahama.jpg attractions/

# culture フォルダに1枚配置
cp ~/Downloads/culture_01_kumano_kodo_tomita.jpg culture/
```

#### 手動で配置する場合:

Finderで以下のフォルダを開いて、ドラッグ&ドロップ：

```
/Users/hiderinchan/Documents/Claude/CreateMovie/ai-video-storyboard/
projects/nanki-shirahama-2024/source_materials/raw/

├── beach/        ← 5枚をここに
├── nature/       ← 6枚をここに
├── attractions/  ← 4枚をここに
└── culture/      ← 1枚をここに
```

---

### Step 3: 配置確認

```bash
cd /Users/hiderinchan/Documents/Claude/CreateMovie/ai-video-storyboard
cd projects/nanki-shirahama-2024/source_materials/raw

# 各フォルダの枚数確認
echo "Beach photos:"
ls -1 beach/ | wc -l

echo "Nature photos:"
ls -1 nature/ | wc -l

echo "Attractions photos:"
ls -1 attractions/ | wc -l

echo "Culture photos:"
ls -1 culture/ | wc -l

echo "Total:"
find . -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | wc -l
```

**期待される出力:**
```
Beach photos: 5
Nature photos: 6
Attractions photos: 4
Culture photos: 1
Total: 16
```

---

### Step 4: 素材スキャン実行

```bash
cd /Users/hiderinchan/Documents/Claude/CreateMovie/ai-video-storyboard

python tools/material_manager.py \
  --project projects/nanki-shirahama-2024 \
  --scan \
  --analyze \
  --map
```

**期待される出力:**
```
📁 Scanning materials...
  ✓ beach: 5 files
  ✓ nature: 6 files
  ✓ attractions: 4 files
  ✓ culture: 1 files

✅ Total materials found: 16

📊 Generating analysis report...
  ✓ Report saved to: source_materials/analyzed/material_analysis.json

🎬 Mapping materials to videos...
  video1: 出会いの予感
    Categories: beach
    Materials: 5 files

  video2: 自然の驚き
    Categories: nature
    Materials: 6 files

  video3: 体験の楽しみ
    Categories: attractions, culture
    Materials: 5 files

  video4: もう一度来たい
    Categories: beach, nature
    Materials: 11 files

  ✓ Mapping saved to: source_materials/analyzed/material_mapping.json

📋 MATERIAL SUMMARY
Total materials: 16
By category:
  attractions: 4 files
  beach: 5 files
  culture: 1 files
  nature: 6 files

Quality:
  HD (1920x1080+): 16/16
  Percentage: 100.0%

💾 Metadata saved to: source_materials/metadata/photo_descriptions.yaml

✅ Material management complete!
```

---

## 📊 動画別使用計画

### Video 1: "出会いの予感" (10秒)
**使用写真（3枚）:**
1. `beach_04_shirahama_aerial_view.jpg` - オープニング俯瞰
2. `beach_02_shirahama_emerald_sea.jpg` - エメラルドの海
3. `beach_01_shirahama_parasol.jpg` - ビーチパラソル

**ストーリー:**
- 0-3秒: 上空から白良浜全景
- 3-7秒: 主人公が砂浜に降り立つ
- 7-10秒: エメラルドの海を見つめる

---

### Video 2: "自然の驚き" (10秒)
**使用写真（3枚）:**
1. `nature_01_engetsuto_sunset.jpg` - 円月島夕日 ⭐
2. `nature_03_sandanbeki_cliff.jpg` - 三段壁
3. `nature_05_senjojiki_rocks_1.jpg` - 千畳敷

**ストーリー:**
- 0-3秒: 円月島の夕日シルエット
- 3-7秒: 主人公が写真を撮る動作
- 7-10秒: 千畳敷の岩場をパン

---

### Video 3: "体験の楽しみ" (10秒)
**使用写真（3枚）:**
1. `attractions_02_sakinoyu_seaside.jpg` - 海側露天風呂
2. `attractions_01_sakinoyu_footbath.jpg` - 足湯
3. `culture_01_kumano_kodo_tomita.jpg` - 熊野古道

**ストーリー:**
- 0-3秒: 海に面した露天風呂でリラックス
- 3-7秒: 足湯に浸かる主人公
- 7-10秒: 熊野古道の石段を歩く

---

### Video 4: "もう一度来たい" (10秒)
**使用写真（3枚）:**
1. `beach_05_shirahama_crescent_bay.jpg` - 三日月型ビーチ
2. `nature_01_engetsuto_sunset.jpg` - 円月島夕日（再登場）
3. `attractions_04_fireworks_shirahama.jpg` - 花火

**ストーリー:**
- 0-3秒: 美しい三日月型のビーチ全景
- 3-7秒: 円月島の夕日（思い出として再登場）
- 7-10秒: 花火を見上げる、手を振る主人公

---

## ✅ チェックリスト

### 写真準備
- [ ] 16枚全ての写真をダウンロード
- [ ] ファイル名を推奨名にリネーム
- [ ] ファイル形式を確認（JPG/JPEG推奨）
- [ ] 解像度を確認（1920x1080以上）

### フォルダ配置
- [ ] beach/ に5枚配置
- [ ] nature/ に6枚配置
- [ ] attractions/ に4枚配置
- [ ] culture/ に1枚配置

### 確認作業
- [ ] 各フォルダの枚数確認
- [ ] 合計16枚であることを確認
- [ ] `material_manager.py` 実行
- [ ] 解析レポート確認

### メタデータ
- [ ] `photo_descriptions.yaml` 生成確認
- [ ] `material_analysis.json` 生成確認
- [ ] `material_mapping.json` 生成確認

---

## 🎯 次のステップ

配置が完了したら、絵コンテ生成に進みます：

```bash
# Video 1 の絵コンテ生成
python scripts/generate_storyboard_v2.py \
  --project nanki-shirahama-2024 \
  --video 1 \
  --title "出会いの予感" \
  --duration 10
```

詳細は [QUICKSTART.md](QUICKSTART.md) を参照してください。

---

## 💡 トラブルシューティング

### Q: ファイル名に日本語が含まれている
**A:** 英数字のファイル名にリネームしてください。
```bash
# 例: 日本語ファイル名を英語に変更
mv "白良浜.jpg" "beach_01_shirahama_parasol.jpg"
```

### Q: 写真のサイズが大きすぎる（10MB以上）
**A:** リサイズツールで圧縮してください。
```bash
# ImageMagickを使用（要インストール）
convert input.jpg -resize 1920x1080 -quality 85 output.jpg
```

### Q: フォルダ構造が見つからない
**A:** プロジェクトディレクトリで再度フォルダを作成：
```bash
cd projects/nanki-shirahama-2024/source_materials/raw
mkdir -p beach nature attractions culture
```

---

*配置ガイド作成日: 2024-11-08*
*プロジェクト: nanki-shirahama-2024*
*素材数: 16枚*
