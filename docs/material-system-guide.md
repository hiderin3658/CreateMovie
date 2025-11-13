# 汎用マテリアルシステム 使い方ガイド

## 概要

汎用マテリアルシステムは、プロジェクトタイプ（観光、教育、マーケティング等）に応じて最適な素材マッチングを行うシステムです。

## クイックスタート

### 1. 既存プロジェクトでの使用

```bash
# 素材を解析してレポート生成
python -m tools.material_system --config projects/your-project/config.yaml
```

### 2. Pythonコードから使用

```python
from tools import MaterialSystem, MaterialConfig

# プロジェクト設定を読み込み
config = MaterialConfig.from_yaml("projects/your-project/config.yaml")

# システム初期化
system = MaterialSystem(config)

# 素材を読み込み（メタデータがなければAI解析）
materials = system.load_materials()

# ストーリーボードにマッピング
mapped_storyboard = system.map_to_storyboard(storyboard)

# レポート生成
report = system.generate_report("output/material_usage_report.json")

# 要件検証
validation = system.validate_requirements()
```

## 設定ファイル (config.yaml)

### 基本設定

```yaml
project:
  id: "my-project-2025"
  name: "My Video Project"
  type: "tourism"  # tourism, education, marketing, competition

requirements:
  materials:
    # カテゴリ定義
    categories:
      - beach
      - nature
      - attractions
      - culture

    # 使用要件
    usage_requirements:
      minimum_usage_rate: 0.75  # 75%以上使用
      allow_reuse: false        # 同じ素材の再利用

    # 制約
    constraints:
      modification_allowed: false  # 素材の改変
      aspect_ratio_fix: true       # アスペクト比固定

# スコアリング重みのカスタマイズ（オプション）
material_scoring_weights:
  keyword_match: 5.0      # キーワードマッチング
  category_match: 3.0     # カテゴリ一致
  time_match: 2.0         # 時間帯一致
  mood_match: 2.0         # ムード相性
  quality_bonus: 1.0      # 品質ボーナス
  unused_bonus: 0.5       # 未使用ボーナス
```

## プロジェクトタイプ別の特徴

### Tourism（観光）

**自動選択される戦略**: `TourismMatchingStrategy`

**ボーナス要素**:
- ランドマーク名が明確: +10.0
- 天候が良好（sunny/clear）: +5.0
- ゴールデンアワー: +5.0
- 場所名完全一致: +15.0

**推奨設定**:
```yaml
project:
  type: tourism
material_scoring_weights:
  keyword_match: 5.0
  landmark_bonus: 10.0  # カスタム重み
```

### Education（教育）

**自動選択される戦略**: `EducationMatchingStrategy`

**ボーナス要素**:
- シンプルな構図: +10.0
- 明るい画像: +5.0
- 高い教育的価値: +8.0

**推奨設定**:
```yaml
project:
  type: education
material_scoring_weights:
  keyword_match: 10.0  # 教育ではキーワード重視
  simplicity_bonus: 8.0
```

### Marketing（マーケティング）

**自動選択される戦略**: `MarketingMatchingStrategy`

**ボーナス要素**:
- 感情的訴求力: +10.0
- 商品の視認性: +8.0
- 適切な構図: +5.0

### Competition（コンペ）

**自動選択される戦略**: `CompetitionMatchingStrategy`

**ボーナス要素**:
- 未使用素材: +20.0（全素材使用を優先）

## AI解析機能

### Gemini Vision API の使用

環境変数 `GEMINI_API_KEY` を設定すると、自動的にGemini Vision APIを使用します。

```bash
export GEMINI_API_KEY='your-api-key'
```

**解析される項目**:
- description: 画像の説明文
- main_subject: 主要な被写体
- composition: 構図タイプ
- color_tone: 色調
- quality_score: 品質スコア
- location: 場所名（観光プロジェクト）
- time_of_day: 時間帯（観光プロジェクト）
- weather: 天候（観光プロジェクト）

### 手動メタデータ

Gemini APIが利用できない場合は、`source_materials/metadata/photo_descriptions.yaml` に手動でメタデータを記述します。

```yaml
project_type: tourism
total_materials: 16
photos:
  - filename: beach_01.jpg
    category: beach
    description: White sand beach with blue ocean
    main_subject: beach
    location: Shirahama Beach
    time_of_day: afternoon
    weather: sunny
    color_tone: warm
    composition: rule_of_thirds
    quality_score: 0.8
    width: 1920
    height: 1080
```

## レポート

### 使用レポートの構造

```json
{
  "summary": {
    "used": 15,
    "total": 16,
    "rate": 0.9375,
    "percentage": "93.8%"
  },
  "by_category": {
    "beach": {
      "used": 4,
      "total": 5,
      "rate": 0.8,
      "percentage": "80.0%"
    }
  },
  "used_materials": [
    {
      "cut_number": 1,
      "filename": "beach_01.jpg",
      "category": "beach",
      "match_score": 125.5,
      "path": "..."
    }
  ],
  "unused_materials": [
    {
      "filename": "beach_05.jpg",
      "category": "beach",
      "reason": "Category oversupplied (5 beach materials, only 4 needed)",
      "quality_score": 0.85,
      "suggestions": [
        "Consider using in video variation",
        "Could be recategorized to better match scenes"
      ]
    }
  ]
}
```

## ストーリーボードへのマッピング

### 入力（ストーリーボード）

```python
storyboard = {
    'cuts': [
        {
            'cut_number': 1,
            'scene_description': '白良浜の美しい景色',
            'categories': ['beach'],
            'mood': 'hopeful',
            'time_of_day': 'afternoon'
        },
        # ...
    ]
}
```

### 出力（マッピング済み）

```python
mapped_storyboard = {
    'cuts': [
        {
            'cut_number': 1,
            'scene_description': '白良浜の美しい景色',
            'source_material': {
                'filename': 'beach_01.jpg',
                'path': '...',
                'category': 'beach',
                'confidence': 125.5  # マッチスコア
            },
            'generation_required': False
        },
        # ...
    ],
    'material_usage': {
        'used': 15,
        'total': 16,
        'rate': 0.9375,
        'percentage': '93.8%'
    }
}
```

## トラブルシューティング

### Gemini APIが使えない

**症状**: `⚠️ google-generativeai not installed`

**解決**:
```bash
pip install google-generativeai
export GEMINI_API_KEY='your-api-key'
```

### 素材が見つからない

**症状**: `No suitable material found`

**原因**:
1. カテゴリが一致しない
2. 全て使用済み（allow_reuse: false）
3. スコアが低すぎる

**解決**:
1. カテゴリを見直す
2. `allow_reuse: true` に設定
3. スコアリング重みを調整

### 使用率が低い

**原因**:
- 素材の品質が低い
- カテゴリが偏っている
- スコアリングロジックが厳しい

**解決**:
1. レポートの `unused_materials` を確認
2. 改善提案に従う
3. スコアリング重みを調整

## 高度な使い方

### カスタムストラテジーの作成

```python
from tools.matching_strategies import MaterialMatchingStrategy

class CustomStrategy(MaterialMatchingStrategy):
    def find_best_match(self, cut, materials, matcher):
        # カスタムマッチングロジック
        candidates = matcher.find_candidates(cut, materials)

        def custom_bonus(material, cut):
            # カスタムボーナス
            return 10.0 if material.custom_field else 0.0

        return self._score_and_select(candidates, cut, matcher, custom_bonus)

# システムに登録
system.strategy = CustomStrategy(config)
```

### プロジェクトマネージャーとの統合

```python
from tools import ProjectManager, MaterialSystem, MaterialConfig

# プロジェクト作成
manager = ProjectManager(workspace=".")
project_id = manager.create_project(
    name="my-project",
    project_type="tourism",
    requirements={...},
    materials=Path("provided_photos")
)

# 素材システム初期化
project_path = manager.projects_dir / "active" / project_id
config = MaterialConfig.from_yaml(project_path / "config.yaml")
system = MaterialSystem(config)

# 自動解析
materials = system.load_materials()
```

## 参考資料

- [設計書](design/generic-material-system-design.md)
- [南紀白浜プロジェクト](../projects/nanki-shirahama-2024/)
- [Gemini Vision API ドキュメント](https://ai.google.dev/gemini-api/docs/vision)

## よくある質問

### Q: 既存のプロジェクトに導入できますか？

A: はい。`config.yaml` を作成するだけで使えます。既存の `material_manager.py` と並行して使用できます。

### Q: プロジェクトタイプを追加できますか？

A: はい。新しい `MaterialMatchingStrategy` を作成して登録します。

### Q: コストはどのくらいですか？

A: Gemini Vision API使用時、1画像あたり約$0.001です。16枚で約$0.016です。

### Q: オフラインで使えますか？

A: 基本機能は使えますが、AI解析は手動でメタデータを作成する必要があります。
