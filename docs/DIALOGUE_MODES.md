# ダイアログモード機能ガイド

ストーリーボードに3種類のセリフモードを追加する機能のドキュメントです。

## 概要

CreateMovie Coreシステムは、3種類のセリフモードをサポートしています：

1. **Narration（ナレーション）** 🎙️ - 語り手によるボイスオーバー
2. **Monologue（モノローグ）** 💭 - 主人公1人が喋る
3. **Dialogue（ダイアログ）** 💬 - 登場人物2人が会話する

---

## データ構造

### DialogueLine

1つの発言を表すデータクラス：

```python
from core.video.storyboard_generator import DialogueLine

line = DialogueLine(
    speaker="アキラ",      # 発言者名
    text="こんにちは",     # セリフ内容
    duration=2.5          # 発言時間（秒）
)
```

### CutData

各カットには以下のフィールドが追加されています：

```python
from core.video.storyboard_generator import CutData

cut = CutData(
    # ... 既存フィールド ...

    # セリフモード選択
    dialogue_mode='narration',  # 'narration', 'monologue', 'dialogue'のいずれか

    # Mode 1: Narration（ナレーション）
    narration_text="物語は静かに始まる。",
    narration_duration=5.0,
    narration_timing="start",  # 'start', 'end', 'throughout'
    narration_style="documentary",

    # Mode 2: Monologue（モノローグ）
    monologue_character="主人公",
    monologue_text="ここに来ると、心が落ち着く。",
    monologue_duration=7.2,

    # Mode 3: Dialogue（ダイアログ）
    dialogue_lines=[
        DialogueLine(speaker="アキラ", text="最近どう？", duration=2.5),
        DialogueLine(speaker="ユキ", text="元気だよ", duration=2.0)
    ],
    dialogue_characters=["アキラ", "ユキ"]
)
```

---

## 使い方

### 基本的な使い方

```python
from core.narration.narration_generator import NarrationGenerator
from core.video.storyboard_generator import CutData

# ジェネレーターの初期化（Claude API必須）
narration_gen = NarrationGenerator()

# ストーリーコンテキスト
story_context = "内なる平和を見つける物語"

# カットリストを用意
cuts = [...]  # CutDataのリスト
```

### Mode 1: Narration（ナレーション）

既存の機能と同じ使い方：

```python
# ナレーションを生成
cuts = narration_gen.generate_dialogue_for_storyboard(
    cuts=cuts,
    story_context=story_context,
    dialogue_mode='narration',
    style='documentary'  # 'documentary', 'poetic', 'dramatic' など
)

# 結果
for cut in cuts:
    if cut.narration_text:
        print(f"Cut {cut.cut_number}:")
        print(f"  {cut.narration_text}")
        print(f"  Duration: {cut.narration_duration}s")
```

### Mode 2: Monologue（モノローグ）

主人公1人が喋るパターン：

```python
# キャラクター情報
character_info = {
    'character1': {
        'name': '主人公',
        'context': '30代の会社員。人生に疲れ、自然の中で癒しを求めている。'
    }
}

# モノローグを生成
cuts = narration_gen.generate_dialogue_for_storyboard(
    cuts=cuts,
    story_context=story_context,
    dialogue_mode='monologue',
    character_info=character_info
)

# 結果
for cut in cuts:
    if cut.monologue_text:
        print(f"Cut {cut.cut_number} ({cut.monologue_character}):")
        print(f"  {cut.monologue_text}")
        print(f"  Duration: {cut.monologue_duration}s")
```

### Mode 3: Dialogue（ダイアログ）

2人の登場人物が会話するパターン：

```python
# キャラクター情報（2人）
character_info = {
    'character1': {
        'name': 'アキラ',
        'context': '楽観的で明るい性格。友人のことを心配している。'
    },
    'character2': {
        'name': 'ユキ',
        'context': '真面目で控えめ。最近仕事で悩んでいる。'
    }
}

# ダイアログを生成
cuts = narration_gen.generate_dialogue_for_storyboard(
    cuts=cuts,
    story_context=story_context,
    dialogue_mode='dialogue',
    character_info=character_info
)

# 結果
for cut in cuts:
    if cut.dialogue_lines:
        print(f"Cut {cut.cut_number} ({' & '.join(cut.dialogue_characters)}):")
        for line in cut.dialogue_lines:
            print(f"  {line.speaker}: {line.text} ({line.duration:.1f}s)")
```

---

## 手動設定

AI生成を使わずに、手動でセリフを設定することも可能です：

### 手動ナレーション設定

```python
cut.dialogue_mode = 'narration'
cut.narration_text = "物語は静かに始まる。"
cut.narration_duration = 5.0
cut.narration_timing = "start"
cut.narration_style = "documentary"
```

### 手動モノローグ設定

```python
cut.dialogue_mode = 'monologue'
cut.monologue_character = "主人公"
cut.monologue_text = "ここに来ると、心が落ち着く。"
cut.monologue_duration = 7.2
```

### 手動ダイアログ設定

```python
from core.video.storyboard_generator import DialogueLine

cut.dialogue_mode = 'dialogue'
cut.dialogue_characters = ['アキラ', 'ユキ']
cut.dialogue_lines = [
    DialogueLine(speaker='アキラ', text='最近どう？', duration=2.5),
    DialogueLine(speaker='ユキ', text='元気だよ', duration=2.0),
    DialogueLine(speaker='アキラ', text='良かった！', duration=1.5)
]
```

---

## 混在モード

1つのストーリーボードで複数のモードを混在させることができます：

```python
# Cut 1: ナレーション
cuts[0].dialogue_mode = 'narration'
cuts[0].narration_text = "物語は海辺から始まる。"
cuts[0].narration_duration = 5.0

# Cut 2: モノローグ
cuts[1].dialogue_mode = 'monologue'
cuts[1].monologue_character = "主人公"
cuts[1].monologue_text = "ここで何を探しているんだろう。"
cuts[1].monologue_duration = 7.5

# Cut 3: ダイアログ
cuts[2].dialogue_mode = 'dialogue'
cuts[2].dialogue_characters = ['アキラ', 'ユキ']
cuts[2].dialogue_lines = [
    DialogueLine(speaker='アキラ', text='見つかった？', duration=2.0),
    DialogueLine(speaker='ユキ', text='まだ。', duration=2.0)
]
```

---

## マークダウンレポートでの表示

生成されたストーリーボードレポートでは、各モードに応じた表示がされます：

### Narration表示例

```markdown
**🎙️ Narration** (start - 5.0s):
\`\`\`
物語は静かに始まる。
\`\`\`
> 💡 Style: documentary | Timing: start | Duration: ~5.0s
```

### Monologue表示例

```markdown
**💭 Monologue** - 主人公 (7.5s):
\`\`\`
ここに来ると、心が落ち着く。
\`\`\`
> 💡 Character: 主人公 | Duration: ~7.5s
```

### Dialogue表示例

```markdown
**💬 Dialogue** - アキラ & ユキ (5.5s):
\`\`\`
アキラ: 最近どう？
          (2.5s)
ユキ: 元気だよ
          (2.0s)
アキラ: 良かった！
          (1.0s)
\`\`\`
> 💡 Characters: アキラ, ユキ | Total Duration: ~5.5s
```

---

## セリフ時間の推定

日本語テキストの発音時間は自動的に計算されます：

- **基準**: 約300文字/分（日本語の標準的な読み上げ速度）
- **句読点による間**:
  - 「。」= +0.5秒
  - 「、」= +0.3秒

### 例

```python
text = "こんにちは、元気ですか。"
# 文字数: 12文字
# 句読点: 、1個 + 。1個
# 推定時間: (12/300)*60 + 0.3 + 0.5 = 2.4 + 0.8 = 3.2秒
```

---

## キャラクター情報の設計

### character_info構造

```python
character_info = {
    'character1': {
        'name': 'キャラクター名',
        'context': 'キャラクターの背景・性格・現在の状況など'
    },
    'character2': {  # dialogueモードの場合のみ必要
        'name': 'キャラクター名2',
        'context': 'キャラクター2の背景・性格・現在の状況など'
    }
}
```

### キャラクターコンテキストの書き方

効果的なキャラクターコンテキスト：

```python
# 良い例
'context': '30代の会社員。人生に疲れ、自然の中で癒しを求めている。内向的で思慮深い性格。'

# 悪い例（情報不足）
'context': '会社員'
```

キャラクターコンテキストには以下を含めると良い：
- 年齢・職業
- 性格・特徴
- 現在の状況・心境
- 話し方の特徴（あれば）

---

## API要件

セリフ生成にはClaude API（Anthropic）が必要です：

```bash
# 環境変数で設定
export ANTHROPIC_API_KEY="your-api-key-here"

# または .env ファイル
ANTHROPIC_API_KEY=your-api-key-here
```

APIが利用できない場合、手動設定を使用してください。

---

## 完全なサンプルコード

```python
#!/usr/bin/env python3
"""
Complete example of using all 3 dialogue modes
"""
from core.video.storyboard_generator import CoreStoryboardGenerator, CutData, DialogueLine
from core.narration.narration_generator import NarrationGenerator
from core.base import GeneratorConfig

# 1. ストーリーボード設定
config = GeneratorConfig(
    title="三つのモードのテスト",
    duration=24,
    num_cuts=3,
    visual_style="cinematic"
)

# 2. カットを作成
generator = CoreStoryboardGenerator(config)
input_data = {
    'story_description': "内なる平和を見つける物語"
}
storyboard = generator.generate_storyboard(input_data)

# 3. ナレーション生成（全カット）
narration_gen = NarrationGenerator()

# Mode 1: Narration
cuts = narration_gen.generate_dialogue_for_storyboard(
    cuts=storyboard.cuts,
    story_context="内なる平和を見つける物語",
    dialogue_mode='narration',
    style='documentary'
)

# または Mode 2: Monologue
character_info = {
    'character1': {
        'name': '主人公',
        'context': '30代の会社員。人生に疲れ、自然の中で癒しを求めている。'
    }
}

cuts = narration_gen.generate_dialogue_for_storyboard(
    cuts=storyboard.cuts,
    story_context="主人公の内的な旅",
    dialogue_mode='monologue',
    character_info=character_info
)

# または Mode 3: Dialogue
character_info = {
    'character1': {
        'name': 'アキラ',
        'context': '楽観的で明るい性格。友人のことを心配している。'
    },
    'character2': {
        'name': 'ユキ',
        'context': '真面目で控えめ。最近仕事で悩んでいる。'
    }
}

cuts = narration_gen.generate_dialogue_for_storyboard(
    cuts=storyboard.cuts,
    story_context="二人の友人が人生について語り合う",
    dialogue_mode='dialogue',
    character_info=character_info
)

# 4. ストーリーボードを保存
storyboard.cuts = cuts
generator.save_storyboard(storyboard, "output/dialogue_test")

print("✅ Storyboard with dialogue generated successfully!")
```

---

## トラブルシューティング

### Claude APIが利用できない

**エラー**: `⚠️  Claude API not available, skipping dialogue generation`

**対処法**:
1. 環境変数 `ANTHROPIC_API_KEY` を設定
2. または手動でセリフを設定

### セリフが長すぎる

**警告**: `⚠️  Warning: Narration (10.5s) exceeds cut duration (8s)`

**対処法**:
1. カットの duration を増やす
2. より短いセリフを手動で設定
3. カットを分割する

### キャラクター情報が不足

**エラー**: `⚠️  Character info required for monologue/dialogue mode`

**対処法**:
`character_info` パラメータを正しく設定：

```python
character_info = {
    'character1': {'name': '...', 'context': '...'},
    'character2': {'name': '...', 'context': '...'}  # dialogueの場合
}
```

---

## 制限事項

- **Dialogueモード**: 現在2人までの会話をサポート（3人以上は未対応）
- **言語**: 日本語での使用を前提に設計（他言語は未検証）
- **API依存**: AI生成にはClaude APIが必須（手動設定は可能）

---

## テスト

テストスイートで動作を確認できます：

```bash
python tests/test_dialogue_modes.py
```

テストでは以下を確認：
- ナレーションモードの生成
- モノローグモードの生成
- ダイアログモードの生成
- 混在モードの動作
- マークダウンレポートの表示

---

## まとめ

### 3つのモード比較

| モード | 用途 | 必要なcharacter_info | 特徴 |
|--------|------|---------------------|------|
| **Narration** | ドキュメンタリー、説明 | 不要 | 客観的な語り |
| **Monologue** | 内的独白、感情表現 | character1のみ | 主観的な語り |
| **Dialogue** | 会話、対話 | character1 + character2 | 複数視点 |

### 使い分けのガイド

- **Narration**: 状況説明、場面転換、オープニング/エンディング
- **Monologue**: 感情表現、内面描写、決意の表明
- **Dialogue**: 対立、情報交換、関係性の描写

### 次のステップ

1. `tests/test_dialogue_modes.py` でサンプルを確認
2. 実際のプロジェクトで試してみる
3. キャラクター情報を詳細に設定して品質向上
4. 混在モードで物語に変化をつける

---

## 参考リンク

- [Core Storyboard Generator](../core/video/storyboard_generator.py)
- [Narration Generator](../core/narration/narration_generator.py)
- [Test Suite](../tests/test_dialogue_modes.py)
- [Generated Report Example](../tests/output/dialogue_modes_test/storyboard_report.md)
