# 白浜プロジェクト - 写真配置ガイド

## 📸 写真の配置場所

白浜の観光写真16枚を以下のフォルダに配置してください：

### 🏖️ beach/ - 白良浜・海岸線（4-5枚）

**配置先:** `source_materials/raw/beach/`

**推奨する写真:**
- 白良浜の白い砂浜（全景）
- 海岸線の風景
- 波打ち際のクローズアップ
- ビーチからの海の眺め
- 夕暮れの海岸

**使用動画:**
- Video 1「出会いの予感」- オープニングシーン
- Video 4「もう一度来たい」- エンディングシーン

---

### 🌊 nature/ - 自然景観（4-5枚）

**配置先:** `source_materials/raw/nature/`

**推奨する写真:**
- 円月島（特に夕日のシルエット）
- 千畳敷の岩場
- 三段壁の断崖
- 自然の造形美
- 海と空の風景

**使用動画:**
- Video 2「自然の驚き」- メインシーン
- Video 4「もう一度来たい」- 印象的シーン再登場

---

### 🎡 attractions/ - 観光施設（4-5枚）

**配置先:** `source_materials/raw/attractions/`

**推奨する写真:**
- アドベンチャーワールド（パンダ等）
- 温泉施設（露天風呂、浴場）
- ホテル・旅館の外観や内装
- その他観光スポット
- アクティビティシーン

**使用動画:**
- Video 3「体験の楽しみ」- アクティビティシーン

---

### 🍱 culture/ - 文化・グルメ（2-3枚）

**配置先:** `source_materials/raw/culture/`

**推奨する写真:**
- 地元グルメ（海鮮、クエ料理等）
- 土産物、特産品
- 歴史的建造物
- 地域の文化的要素

**使用動画:**
- Video 3「体験の楽しみ」- グルメ・文化体験シーン

---

## ✅ 配置後の確認

写真を配置したら、以下のコマンドで確認：

```bash
# フォルダ内の写真を確認
ls -la source_materials/raw/beach/
ls -la source_materials/raw/nature/
ls -la source_materials/raw/attractions/
ls -la source_materials/raw/culture/

# 素材マネージャーでスキャン
cd /Users/hiderinchan/Documents/Claude/CreateMovie/ai-video-storyboard
python tools/material_manager.py \
  --project projects/nanki-shirahama-2024 \
  --scan \
  --analyze \
  --map
```

---

## 📋 写真の命名例

わかりやすいファイル名にすると管理が楽になります：

```
beach_01_shirarahama_wide.jpg
beach_02_coastline_sunset.jpg
nature_01_engetsuto_silhouette.jpg
nature_02_senjojiki_rocks.jpg
attractions_01_adventure_world_panda.jpg
attractions_02_onsen_rotenburo.jpg
culture_01_seafood_kaiseki.jpg
culture_02_local_souvenir.jpg
```

---

## 🎯 重要な注意事項

1. **解像度**: 最低 1920x1080 (Full HD) を推奨
2. **ファイル形式**: JPG, PNG推奨
3. **ファイルサイズ**: 5MB以下が望ましい
4. **構図**: 被写体が明確で、ブレがないこと
5. **モチーフ**: 後でアニメ化しても認識できる明確さ

---

*配置が完了したら QUICKSTART.md の Step 2 に進んでください*
