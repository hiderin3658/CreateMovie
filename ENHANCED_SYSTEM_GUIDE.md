# Enhanced AI Video Storyboard System

PDFガイドとリファレンス統合による高度化システム実装ガイド

## 🎯 実装概要

本システムは、「AIアニメ勉強会2025/11/11」PDFの知見と既存リファレンスファイルを統合し、以下の高度化を実現しました：

### ✨ 主要な実装機能

1. **J-pop構成による感情設計システム** 🎵
   - サビ→Aメロ→Bメロ→サビ の4段階感情フロー
   - 1-2秒1アクションのテンポ設計
   - 感情のピークを意図的配置

2. **インテリジェント選択エンジン** 🧠  
   - ムード・ジャンル・強度に基づくカメラアングル自動選択
   - 2,375+行のリファレンス知識を活用
   - 文脈を理解した構図・カメラワーク決定

3. **縦型9:16完全対応** 📱
   - モバイルファースト視線フロー最適化
   - 上下配置ルールの自動適用
   - クローズアップ重視構図強化

4. **感情移入促進機能** 💝
   - 共感起点の自動検出・冒頭配置
   - 3層刺激（視覚・聴覚・感情）システム
   - J-pop構成による視聴者エンゲージメント向上

5. **設定資料システム基盤** 🎨
   - キャラクター・背景一貫性管理準備
   - nano-banana/SeeDream4連携想定設計

## 🚀 使用方法

### 基本的な使用例

```bash
# 縦型観光動画（推奨）
python scripts/generate_enhanced_storyboard.py \
  --story "白浜の魅力を30秒で紹介" \
  --genre tourism \
  --vertical

# 高度化機能フル活用
python scripts/generate_enhanced_storyboard.py \
  --story "新製品の魅力" \
  --genre commercial \
  --intelligence high \
  --empathy \
  --stimulation \
  --duration 45
```

### 設定オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `--genre` | tourism/educational/commercial/documentary/music/narrative | tourism |
| `--vertical` | 9:16縦型最適化 | false (16:9) |
| `--intelligence` | low/medium/high インテリジェント選択レベル | high |
| `--empathy` | 感情移入促進機能 | true |
| `--stimulation` | 3層刺激システム | true |
| `--duration` | 動画尺（秒） | 30 |
| `--cuts` | カット数 | 8 |

## 📊 システム構成

### コア実装ファイル

```
core/video/enhanced_storyboard_generator.py  # メインシステム (1,000+行)
├── JPOPEmotionalStructure                   # J-pop感情構造
├── IntelligentSelectionEngine              # インテリジェント選択
├── VerticalOptimizer                       # 縦型最適化
├── EmotionalEngagementEnhancer             # 感情移入促進
└── EnhancedStoryboardGenerator             # 統合ジェネレーター

scripts/generate_enhanced_storyboard.py      # 実行スクリプト
test_enhanced_system.py                      # テストスイート
```

### 参照リソース活用

既存リファレンスの完全統合：
- `references/camera_movements.md` (714行) → 動的選択アルゴリズム化
- `references/camera_shots.md` (345行) → ムード別マトリックス化
- `references/composition_guide.md` (612行) → インテリジェント構図選択
- `references/itov_patterns.md` (704行) → 高度プロンプト生成

## 🎵 J-pop感情構造の詳細

### 4段階フェーズ設計

| フェーズ | 時間配分 | 役割 | 強度 | 特徴 |
|---------|---------|------|------|------|
| **サビ（フック）** | 0-10秒 | 即時インパクト | 0.8 | 冒頭で強い印象、共感起点設定 |
| **Aメロ** | 10-17秒 | 説明・展開 | 0.4 | 理解促進、文脈構築 |
| **Bメロ** | 17-24秒 | 深化・多様性 | 0.6 | 複雑さ追加、エンゲージメント維持 |
| **サビ（クライマックス）** | 24-30秒 | 最大インパクト | 1.0 | 感情的ピーク、行動誘発 |

### 1-2秒1アクションテンポ

```python
ACTION_PACING = {
    'fast': {'actions_per_second': 1.0},    # 高エネルギー
    'medium': {'actions_per_second': 0.7},  # バランス型
    'slow': {'actions_per_second': 0.5}     # 思索的
}
```

## 🧠 インテリジェント選択の仕組み

### ムード別選択マトリックス

**peaceful（平和的）** シーンの場合：
- カメラ: MS, LS 優先 / ECU 回避
- 構図: rule_of_thirds, symmetry 優先
- 動き: static, slow_dolly 優先

**energetic（エネルギッシュ）** シーンの場合：
- カメラ: MS, CU 優先 / ELS 回避  
- 構図: diagonal, dynamic_angles 優先
- 動き: tracking, handheld 優先

### 文脈的選択アルゴリズム

```python
def select_camera_angle(context: SceneContext, scene_type: str):
    # 1. ムード優先選択
    # 2. 強度による調整 (intensity > 0.7 → CU/ECU重視)
    # 3. ジャンル特性考慮
    # 4. アスペクト比最適化
```

## 📱 縦型最適化システム

### 9:16専用エンハンス

```python
vertical_optimizations = {
    'aspect_ratio': '9:16 vertical aspect ratio',
    'flow_direction': 'vertical visual flow from top to bottom', 
    'framing': 'tight framing suitable for mobile viewing',
    'focal_point': 'subject in upper two-thirds for natural eye flow',
    'text_space': 'space at bottom for text/UI elements'
}
```

### クローズアップ重視戦略

縦型では以下を強化：
- 顔・表情のクローズアップ効果最大化
- 上部2/3への被写体配置
- モバイル視聴を考慮した背景シンプル化

## 💝 3層刺激システム

### レイヤー構造

1. **視覚層** (Visual Layer)
   - 動き: 強度に応じた動的レベル調整
   - 色彩: 高コントラスト → 暖色系 → 落ち着いた色
   - 効果: モーションブラー、ライティング演出

2. **聴覚層** (Auditory Layer)  
   - BGM: フェーズ連動スタイル提案
   - SFX: シーン別効果音ライブラリ
   - リズム: ビジュアルカットと音楽同期

3. **感情層** (Emotional Layer)
   - サプライズ: 予期しない展開要素
   - 共感: 視聴者識別ポイント
   - 満足: 視覚・ナラティブ報酬

## 🎯 ジャンル別最適化

| ジャンル | 主要構図 | カメラ特性 | 特化機能 |
|---------|---------|-----------|---------|
| **Tourism** | rule_of_thirds, golden_ratio | 美的撮影 | 旅行魅力アピール |
| **Educational** | rule_of_thirds, centered | 明確・指導的 | プロフェッショナル提示 |
| **Commercial** | golden_ratio, negative_space | 高品質 | プレミアム市場訴求 |
| **Documentary** | rule_of_thirds | 自然・リアル | 真正性重視 |

## 📈 パフォーマンス比較

### 従来システム vs 高度化システム

| 指標 | 従来 | 高度化 | 改善率 |
|------|------|-------|--------|
| **選択パターン数** | 26項目 | 200+項目 | +669% |
| **文脈考慮** | 基本ルール | 多次元分析 | 質的向上 |
| **縦型対応** | 16:9指定のみ | 完全最適化 | 新機能 |
| **感情設計** | なし | J-pop4段階 | 新機能 |
| **プロンプト精度** | 基本 | 高度化 | 定性向上 |

## 🧪 テスト結果

```
🧪 Enhanced System Basic Tests
========================================
🎵 J-pop Structure: ✅ PASSED
   Generated 8 cuts with 4 unique phases
   
🧠 Intelligent Selection: ✅ PASSED  
   Context-aware: CU | rule_of_thirds | handheld
   
📱 Vertical Optimization: ✅ PASSED
   9:16 conversion and mobile optimization
```

## 🔧 技術仕様

### 依存関係

```python
# 新規追加なし - 既存システム完全互換
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import json, re, random
```

### 設定例

```python
enhanced_config = {
    'aspect_ratio': AspectRatio.VERTICAL,  # 9:16
    'genre': VideoGenre.TOURISM,
    'intelligence_level': 'high',
    'empathy_enhancement': True,
    'three_layer_stimulation': True,
    'vertical_optimization': True
}
```

## 🚀 今後の拡張可能性

### 準備済み基盤

1. **Vコンテ生成機能**
   - Sora2連携システムの土台完成
   - 字コンテ→映像コンテ変換準備

2. **設定資料管理**
   - キャラクター一貫性システム基盤
   - nano-banana/SeeDream4連携想定

3. **ポストプロダクション統合**
   - 編集メタデータ自動生成
   - エフェクト・テロップ指示システム

### 発展方向

- **AIモデル連携拡大**: Veo3, Sora2最適化
- **リアルタイム調整**: 生成中のパラメータ調整
- **学習機能**: 成功パターンの自動学習
- **多言語対応**: 国際展開対応

## 📚 関連資料

- [既存リファレンスガイド](references/) - 2,375+行の知識ベース
- [AIアニメ勉強会PDF](#) - 実装元資料
- [従来システム](core/video/storyboard_generator.py) - 後方互換性維持

---

**📧 Contact**: システムの詳細や拡張については、開発チームまでお問い合わせください。

**⚡ Quick Start**: `python scripts/generate_enhanced_storyboard.py --story "あなたのストーリー" --genre tourism --vertical`