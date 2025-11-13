# Research Integration Guide - Nanki Shirahama Project

このガイドでは、白浜プロジェクト用に構築されたリサーチデータベースの使い方と、それを活用した高度な素材マッチングシステムについて説明します。

## 概要

Deep Researchから抽出された構造化データ（`data/shirahama-locations-database.yaml`）を活用し、ストーリー制作と素材マッチングの精度を大幅に向上させます。

### 主な機能

1. **構造化ロケーションデータベース**: 10箇所の観光地の詳細情報
2. **ストーリーフレームワーク**: 3種類の物語構造（対比、時間、五感）
3. **リサーチ連携型マッチング**: 素材選択にリサーチデータを活用
4. **ナラティブフレーズ**: オープニング/トランジション/クロージング
5. **季節別推奨**: 最適な撮影時期とロケーション

---

## 1. リサーチデータベースの構造

### ロケーション情報（10箇所）

各ロケーションには以下の情報が含まれます：

```yaml
locations:
  - id: "sakinoyu"
    name: "崎の湯"
    category: "attractions"
    type: "露天風呂"

    core_narrative: "荒々しい自然との一体化"
    storytelling_theme: "自然への帰順"

    key_features:
      - "日本最古級の露天風呂"
      - "太平洋と一体化する野趣"

    visual_elements:
      primary: "湯舟に迫る波しぶき、湯気と潮風"
      contrast: "静（湯舟の水面）と動（波の轟音）の極端な対比"

    filming_tips:
      best_time: "早朝（光線）、または荒天時（波）"
      shot_types:
        - "三脚固定の静ショット（湯舟の水面）"
        - "波のダイナミズムを追う動ショット"
      sound_design: "太平洋の轟音（低周波）と湯の流れ（高周波）のコントラスト"

    logistics:
      price: "500円（3歳以上）"
      hours:
        summer: "7:00-19:00（7-8月）"
        winter: "8:00-17:00（10-3月）"
      access: "JR白浜駅から車で約15分"
```

### ストーリーフレームワーク（3種類）

#### A案：対比の物語
- **テーマ**: 古代と現代、静と動、自然と人工
- **ターゲット**: 知的で物事の多面性を楽しむ層
- **構成**: 対比する要素のペア（熊野古道の静 vs SUNTIDEの動）

#### B案：時間の物語（最も推奨）
- **テーマ**: 1500万年から15分まで、白浜で交錯する時間
- **ターゲット**: 歴史や地質学に興味があり、深い学びを旅に求める層
- **タイムライン**:
  - 1500万年前 → 千畳敷
  - 平安時代 → 熊野古道
  - 源平合戦 → 三段壁
  - 江戸時代 → 番所山
  - 現代 → 白良浜
  - 一瞬 → 円月島の夕日
  - 15分 → 花火ラリー

#### C案：五感の物語
- **テーマ**: 白浜で研ぎ澄まされる五感
- **ターゲット**: 癒しと感覚的な体験を最優先する層
- **マッピング**: 視覚→円月島/花火、聴覚→崎の湯/千畳敷、触覚→温泉/白良浜

---

## 2. 基本的な使い方

### 2.1 リサーチデータベースの読み込み

```python
from tools import ResearchDatabase
from pathlib import Path

# データベースの読み込み
db_path = Path("projects/nanki-shirahama-2024/data/shirahama-locations-database.yaml")
db = ResearchDatabase(db_path)

# プロジェクト情報
print(db.project)  # {'name': '南紀白浜観光プロモーション', 'theme': '...', ...}

# ロケーション一覧
print(f"Locations: {len(db.locations)}")  # 10
```

### 2.2 ロケーション検索

```python
# ID で検索
location = db.get_location("sakinoyu")
print(location.name)  # "崎の湯"
print(location.core_narrative)  # "荒々しい自然との一体化"

# 名前で検索
location = db.get_location_by_name("白良浜")

# カテゴリで検索
beach_locations = db.search_locations(category='beach')

# キーワードで検索
onsen_locations = db.search_locations(keywords=['温泉', '湯'])
```

### 2.3 シーンに基づくロケーション提案

```python
# シーン説明から推奨ロケーションを取得
suggestions = db.suggest_locations_for_scene(
    scene_description="Beautiful white sand beach with blue water",
    mood="peaceful",
    time_of_day="afternoon"
)

for location in suggestions[:3]:  # Top 3
    print(f"{location.name}: {location.core_narrative}")
```

### 2.4 ストーリーフレームワークの使用

```python
# 「時間の物語」フレームワークで構造生成
structure = db.generate_story_structure(
    framework_key='time',  # 'contrast', 'time', 'senses'
    num_cuts=7
)

for cut in structure:
    print(f"Cut {cut['cut_number']}: {cut['era']}")
    print(f"  Location: {cut['location']}")
    print(f"  Hint: {cut['narrative_hint']}")
```

---

## 3. Research-Aware Material System

リサーチデータベースを活用した高度な素材マッチングシステム。

### 3.1 基本セットアップ

```python
from tools import (
    MaterialSystem,
    MaterialConfig,
    ResearchAwareStrategy
)
from pathlib import Path

# プロジェクト設定を読み込み
config_path = Path("projects/nanki-shirahama-2024/config.yaml")
config = MaterialConfig.from_yaml(config_path)

# Material System を初期化
system = MaterialSystem(config)

# リサーチデータベースのパス
research_db_path = Path("projects/nanki-shirahama-2024/data/shirahama-locations-database.yaml")

# 通常のストラテジーをResearchAwareStrategyに置き換え
system.strategy = ResearchAwareStrategy(config, research_db_path)

# 素材を読み込み
materials = system.load_materials()
```

### 3.2 リサーチ連携型マッチング

ResearchAwareStrategyは通常のTourismStrategyに加えて、以下のボーナススコアを追加します：

| ボーナス条件 | スコア | 説明 |
|------------|-------|------|
| コアナラティブマッチ | +8 | ロケーションの核となる物語がシーン説明に含まれる |
| ストーリーテーママッチ | +6 | テーマの言葉がシーン説明に含まれる |
| ビジュアル要素マッチ | +4 (per word) | 視覚的要素の記述がマッチ |
| 撮影時間推奨マッチ | +12 | 推奨撮影時間とシーンの時間帯が一致 |
| 撮影優先度ボーナス | +10 | 優先度が高いロケーション |
| リサーチ提案マッチ | +20/rank | DBが提案したロケーション（1位: 20pt, 2位: 10pt） |

### 3.3 実際の使用例

```python
# ストーリーボードを作成
storyboard = {
    'title': '白浜観光プロモーション',
    'cuts': [
        {
            'scene_description': '白い砂浜と青い海、リラックスする人々',
            'mood': 'peaceful',
            'time_of_day': 'afternoon',
            'categories': ['beach']
        },
        {
            'scene_description': '波しぶきが降りかかる露天風呂',
            'mood': 'natural',
            'time_of_day': 'early morning',
            'categories': ['attractions']
        }
    ]
}

# 素材をマッピング
mapped = system.map_to_storyboard(storyboard, allow_generation=False)

# 結果を確認
for i, cut in enumerate(mapped['cuts'], 1):
    print(f"Cut {i}:")
    if 'source_material' in cut:
        print(f"  ✓ {cut['source_material']['filename']}")
        print(f"    Confidence: {cut['source_material']['confidence']:.1f}")
```

---

## 4. ロケーション情報の活用

### 4.1 ロケーションコンテキストの取得

```python
# 素材に紐付いたロケーションの詳細情報を取得
context = system.strategy.get_location_context("白良浜")

print(context['core_narrative'])  # "人間の情熱が維持する完璧な美"
print(context['storytelling_theme'])  # "キュレーションされた楽園"
print(context['filming_tips']['best_time'])  # 撮影ガイド
```

### 4.2 ストーリーボードへのリサーチ統合

```python
# ストーリーボードにリサーチデータを統合
enhanced = system.strategy.enhance_storyboard_with_research(storyboard)

# プロジェクトコンテキスト
print(enhanced['research_context']['theme'])

# 各カットにリサーチ推奨が追加される
for cut in enhanced['cuts']:
    if 'research_suggestion' in cut:
        suggestion = cut['research_suggestion']
        print(f"Suggested: {suggestion['location_name']}")
        print(f"  → {suggestion['core_narrative']}")
        print(f"  Tips: {suggestion['filming_tips']['best_time']}")

# ナラティブフレーズも追加される
print(enhanced['narrative_phrases']['openings'])
```

---

## 5. ストーリー生成への活用

### 5.1 フレームワークベースの生成

```python
# 「時間の物語」フレームワークでストーリー生成
story_structure = system.strategy.generate_story_with_framework(
    framework_key='time',
    num_cuts=7
)

for cut in story_structure:
    print(f"Cut {cut['cut_number']}: {cut['era']} - {cut['location']}")
    print(f"  Visual: {cut['visual_elements']['primary']}")
    print(f"  Tips: {cut['filming_tips']['best_time']}")
    print()
```

### 5.2 ナラティブフレーズの使用

```python
from tools import ResearchDatabase

db = ResearchDatabase(research_db_path)

# オープニングナレーション用
openings = db.get_narrative_phrases('openings')
print(openings[0])
# → "白浜には、四つの顔がある。古代の聖地、地質学の博物館、歴史的要衝、そして近代的なリゾート。"

# トランジション用
transitions = db.get_narrative_phrases('transitions')
print(transitions[0])
# → "目を閉じて、白浜の『音』を聞く。"

# クロージング用
closings = db.get_narrative_phrases('closings')
print(closings[0])
# → "白浜。ここは、自然と人間の情熱が描き上げた、一枚の絵画である。"
```

---

## 6. 季節別推奨

```python
# 夏の推奨ロケーション
summer = db.get_seasonal_recommendations('summer')
print(summer['best'])
# → ['白良浜（パラソルの賑わい）', '花火ラリー', 'SUNTIDE（リゾート感）']

# 春/秋の推奨ロケーション
spring_autumn = db.get_seasonal_recommendations('spring_autumn')
print(spring_autumn['best'])
# → ['円月島（穴に沈む夕日）', '熊野古道（過ごしやすい気候）']

# 冬の推奨ロケーション
winter = db.get_seasonal_recommendations('winter')
print(winter['best'])
# → ['崎の湯（温泉の湯気が美しい）', '湯けむり（ASMR的要素）']
```

---

## 7. 撮影優先度の活用

```python
# 撮影優先度の高いロケーション
priorities = db.get_filming_priority_locations()

for priority in priorities:
    print(f"{priority['location']} - {priority['priority']}")
    print(f"  Reason: {priority['reason']}")
```

出力例：
```
円月島 - 最高
  Reason: 奇跡の瞬間（春分・秋分期）は見逃せない
花火ラリー - 高
  Reason: 7-8月の日曜限定、15分間のみ
白良浜 - 高
  Reason: ブランド・アイデンティティの核
```

---

## 8. CLI使用例

### リサーチDBクエリ

```bash
# ロケーション一覧
python -m tools.research_loader \
  --database projects/nanki-shirahama-2024/data/shirahama-locations-database.yaml \
  --list-locations

# キーワード検索
python -m tools.research_loader \
  --database projects/nanki-shirahama-2024/data/shirahama-locations-database.yaml \
  --search "温泉,湯" \
  --category attractions

# ストーリーフレームワーク表示
python -m tools.research_loader \
  --database projects/nanki-shirahama-2024/data/shirahama-locations-database.yaml \
  --framework time
```

### テストスイートの実行

```bash
# 全機能のテスト
python projects/nanki-shirahama-2024/test_research_integration.py
```

---

## 9. 実装詳細

### ファイル構成

```
projects/nanki-shirahama-2024/
├── data/
│   └── shirahama-locations-database.yaml  # リサーチDB
├── docs/
│   ├── shirahama-deep-research.md         # 元のリサーチ文書
│   └── research-integration-guide.md      # このガイド
└── test_research_integration.py           # テストスイート

tools/
├── research_loader.py                     # DBローダー
└── research_aware_strategy.py             # リサーチ連携ストラテジー
```

### 主要クラス

**ResearchDatabase**
- YAML形式のリサーチデータを読み込み
- ロケーション、ストーリーフレームワーク、ナラティブフレーズを管理
- 検索・提案機能を提供

**ResearchAwareStrategy**
- TourismMatchingStrategyを拡張
- リサーチデータベースと連携して素材マッチングを強化
- スコアリングにリサーチデータを活用

---

## 10. ベストプラクティス

### ストーリー制作時

1. **フレームワーク選択**: 最初にストーリーフレームワークを決定
   - 教育的: 「時間の物語」（推奨）
   - アーティスティック: 「対比の物語」
   - 感覚的: 「五感の物語」

2. **季節考慮**: 撮影時期に応じた季節別推奨を参照

3. **優先度確認**: 撮影優先度の高いロケーションを優先的に使用

4. **ナラティブ活用**: 構造化されたフレーズを活用して統一感を演出

### 素材マッチング時

1. **ResearchAwareStrategy使用**: 通常のTourismStrategyより精度が高い

2. **ロケーション情報の参照**: マッチング後、ロケーションコンテキストを確認

3. **撮影ガイド活用**: filming_tips を参考に最適な時間帯/構図を選択

4. **コアナラティブの理解**: 各ロケーションの物語性を理解して選択

---

## 11. トラブルシューティング

### Q: リサーチDBが読み込めない

```python
# パスを確認
db_path = Path("projects/nanki-shirahama-2024/data/shirahama-locations-database.yaml")
assert db_path.exists(), f"Database not found: {db_path}"
```

### Q: スコアが低すぎる

ResearchAwareStrategyは通常のTourismStrategyより厳密です。`system.strategy.find_best_match()` の結果を確認してください。

### Q: ロケーション名が一致しない

素材のメタデータ（`location` フィールド）とリサーチDBの `name` フィールドが完全一致する必要があります。

---

## まとめ

このリサーチ統合システムにより、以下が実現されます：

✅ **構造化されたリサーチデータ**: Deep Researchの知見をプログラムから活用可能
✅ **高精度な素材マッチング**: リサーチデータに基づいた最適な素材選択
✅ **ストーリーフレームワーク**: 3種類の物語構造で多様なアプローチ
✅ **撮影ガイド統合**: 最適な時間帯・構図・音響設計の提案
✅ **季節別最適化**: 時期に応じたロケーション推奨

これにより、白浜観光プロモーション動画の制作効率と品質が大幅に向上します。
