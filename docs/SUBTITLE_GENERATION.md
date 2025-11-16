# 字幕生成機能ガイド

ストーリーボードのセリフ・ナレーションから自動的に字幕を生成する機能のドキュメントです。

## 概要

CreateMovie Coreシステムは、3種類のダイアログモードに対応した字幕自動生成機能をサポートしています：

1. **Narration（ナレーション）** 🎙️ - オプション（ドキュメンタリーでは字幕なしが一般的）
2. **Monologue（モノローグ）** 💭 - 話者名なしで全文表示
3. **Dialogue（ダイアログ）** 💬 - 話者名付き/なしで表示

絵コンテ作成時に自動的に字幕が生成され、画面下部に表示される内容が決定されます。

---

## 特徴

### ✅ **ダイアログモード別の最適な字幕スタイル**
- **Narration**: ドキュメンタリーでは字幕なし、シネマティックでは全文表示
- **Monologue**: 話者名なしで字幕全文表示（映像で誰が話しているかわかるため）
- **Dialogue**: 話者名付きで表示（誰のセリフか明確化）

### ✅ **自動テキスト分割**
- 1行あたり最大40文字（日本語）
- 句読点で自然に分割
- 長文は複数行の字幕に自動分割

### ✅ **読みやすいタイミング計算**
- 日本語読解速度: 5文字/秒（快適な読みやすさ）
- セリフの長さに応じて表示時間を自動調整
- 複数行の字幕は時間を均等配分

### ✅ **SRT形式エクスポート**
- 業界標準のSubRip (.srt) 形式で出力
- 動画編集ソフトで直接使用可能
- タイムコード付き

---

## 使い方

### 基本的な使い方

```python
from core.video.subtitle_generator import SubtitleGenerator

# 字幕生成器を初期化
subtitle_gen = SubtitleGenerator()

# ストーリーボード全体の字幕を生成
cuts_with_subtitles = subtitle_gen.generate_subtitles_for_storyboard(
    cuts=storyboard.cuts,
    default_style='auto'  # 自動選択
)

# 各カットの字幕を確認
for cut in cuts_with_subtitles:
    if cut.subtitle_lines:
        print(f"Cut {cut.cut_number}: {len(cut.subtitle_lines)} subtitle lines")
        for subtitle in cut.subtitle_lines:
            print(f"  [{subtitle.start_time:.1f}s - {subtitle.end_time:.1f}s] {subtitle.text}")
```

### SRT形式でエクスポート

```python
# 字幕をSRT形式で保存
subtitle_gen.export_srt(
    cuts=cuts_with_subtitles,
    output_path="output/subtitles.srt"
)
```

生成されたSRTファイルは、Premiere Pro、Final Cut Pro、DaVinci Resolveなどの動画編集ソフトで使用できます。

---

## 字幕スタイル

### 字幕スタイルの種類

| スタイル | 説明 | 使用場面 |
|---------|------|---------|
| `auto` | モードに応じて自動選択 | 推奨（デフォルト） |
| `none` | 字幕なし | ドキュメンタリー、映像のみ |
| `full` | 全文字幕表示 | ナレーション、教育動画 |
| `with_speaker` | 話者名付き字幕 | ダイアログ（複数話者） |
| `without_speaker` | 話者名なし字幕 | モノローグ、明確な会話 |

### モード別の自動選択ルール

**Narration（ナレーション）:**
```python
cut.dialogue_mode = 'narration'
cut.narration_style = 'documentary'  # → 字幕なし (auto)
cut.narration_style = 'cinematic'    # → 全文字幕 (auto)
```

**Monologue（モノローグ）:**
```python
cut.dialogue_mode = 'monologue'
# → 話者名なし字幕 (auto)
```

**Dialogue（ダイアログ）:**
```python
cut.dialogue_mode = 'dialogue'
# → 話者名付き字幕 (auto)
```

---

## 各モードの使用例

### Mode 1: Narration（ナレーション）

```python
# ナレーション付きカット
cut.dialogue_mode = 'narration'
cut.narration_text = "物語は、静かな海辺から始まる。夕日が水平線に沈み、一日が終わりを告げる。"
cut.narration_duration = 8.0
cut.narration_style = 'cinematic'

# 字幕生成（シネマティックなので字幕あり）
subtitle_gen = SubtitleGenerator()
cut.subtitle_lines = subtitle_gen.generate_narration_subtitles(cut, style='auto')

# 結果:
# [0.0s - 4.0s] 物語は、静かな海辺から始まる。
# [4.0s - 8.0s] 夕日が水平線に沈み、一日が終わりを告げる。
```

**ドキュメンタリースタイルの場合:**
```python
cut.narration_style = 'documentary'
# → 字幕なし（autoモード）
```

### Mode 2: Monologue（モノローグ）

```python
# モノローグ付きカット
cut.dialogue_mode = 'monologue'
cut.monologue_character = "主人公"
cut.monologue_text = "ここに来ると、いつも心が落ち着く。都会の喧騒から離れて、自分と向き合える場所。"
cut.monologue_duration = 10.0

# 字幕生成（話者名なし）
cut.subtitle_lines = subtitle_gen.generate_monologue_subtitles(cut, style='auto')

# 結果:
# [0.0s - 5.0s] ここに来ると、いつも心が落ち着く。
# [5.0s - 10.0s] 都会の喧騒から離れて、自分と向き合える場所。
```

**特徴:**
- 話者名は表示されない（映像で明らか）
- セリフのみを字幕として表示

### Mode 3: Dialogue（ダイアログ）

```python
from core.video.storyboard_generator import DialogueLine

# ダイアログ付きカット
cut.dialogue_mode = 'dialogue'
cut.dialogue_characters = ['アキラ', 'ユキ']
cut.dialogue_lines = [
    DialogueLine(speaker='アキラ', text='最近、どう？元気にしてた？', duration=3.0),
    DialogueLine(speaker='ユキ', text='まあまあかな。仕事が忙しくて。', duration=3.5),
    DialogueLine(speaker='アキラ', text='そうか。無理しないでね。', duration=2.5)
]

# 字幕生成（話者名付き）
cut.subtitle_lines = subtitle_gen.generate_dialogue_subtitles(cut, style='auto')

# 結果:
# [0.0s - 3.0s] アキラ: 最近、どう？元気にしてた？
# [3.0s - 6.5s] ユキ: まあまあかな。仕事が忙しくて。
# [6.5s - 9.0s] アキラ: そうか。無理しないでね。
```

**話者名なしで表示:**
```python
cut.subtitle_lines = subtitle_gen.generate_dialogue_subtitles(cut, style='without_speaker')

# 結果:
# [0.0s - 3.0s] 最近、どう？元気にしてた？
# [3.0s - 6.5s] まあまあかな。仕事が忙しくて。
# [6.5s - 9.0s] そうか。無理しないでね。
```

---

## 高度な使い方

### 字幕の有効/無効を制御

```python
# 特定のカットで字幕を無効化
cut.subtitle_enabled = False

# 字幕スタイルを手動指定
cut.subtitle_style = 'none'  # 字幕なし
cut.subtitle_style = 'full'  # 全文表示
cut.subtitle_style = 'with_speaker'  # 話者名付き
```

### テキスト分割のカスタマイズ

```python
subtitle_gen = SubtitleGenerator()

# 長いテキストを分割
text = "これは非常に長いテキストで、字幕として表示するには長すぎます。適切に分割する必要があります。"
lines = subtitle_gen.split_text_into_lines(text, max_chars=40)

# 結果:
# ['これは非常に長いテキストで、字幕として表示するには長すぎます。',
#  '適切に分割する必要があります。']
```

### タイミング計算のカスタマイズ

```python
# 字幕の表示タイミングを計算
text = "こんにちは、元気ですか？"
start_time, end_time = subtitle_gen.calculate_timing(
    text=text,
    total_duration=10.0,  # 利用可能な時間
    num_lines=1,          # 字幕の総行数
    line_index=0          # この字幕のインデックス
)

print(f"表示時間: {start_time:.1f}s - {end_time:.1f}s")
```

---

## データ構造

### SubtitleLine

```python
@dataclass
class SubtitleLine:
    """単一の字幕行"""
    text: str              # 字幕テキスト
    start_time: float      # 開始時間（カットの開始からの秒数）
    end_time: float        # 終了時間（カットの開始からの秒数）
    speaker: Optional[str] = None  # 話者名（dialogueモードの場合）
```

### CutData字幕フィールド

```python
@dataclass
class CutData:
    # ... 他のフィールド ...

    # 字幕システム
    subtitle_enabled: bool = True           # 字幕を生成するか
    subtitle_style: str = 'auto'           # 字幕スタイル
    subtitle_lines: Optional[List[SubtitleLine]] = None  # 生成された字幕
```

---

## SRT形式の詳細

### SRTフォーマット

生成されるSRTファイルは以下の形式：

```srt
1
00:00:00,000 --> 00:00:05,000
物語は、静かな海辺から始まる。

2
00:00:05,000 --> 00:00:10,000
夕日が水平線に沈み、一日が終わりを告げる。

3
00:00:10,000 --> 00:00:13,000
アキラ: 最近、どう？

4
00:00:13,000 --> 00:00:16,500
ユキ: まあまあかな。
```

### 動画編集ソフトでの使用

**Premiere Pro:**
1. プロジェクトパネルに `.srt` ファイルをインポート
2. タイムラインの字幕トラックにドラッグ
3. 自動的にタイミング通りに配置される

**Final Cut Pro:**
1. `ファイル` → `読み込み` → `字幕`
2. `.srt` ファイルを選択
3. タイムラインに自動配置

**DaVinci Resolve:**
1. メディアプールに `.srt` ファイルを追加
2. タイムラインの字幕トラックにドラッグ

---

## API仕様

### SubtitleGenerator

#### `__init__()`

字幕生成器を初期化。

```python
subtitle_gen = SubtitleGenerator()
```

#### `generate_narration_subtitles(cut, style='auto') -> List[SubtitleLine]`

ナレーションモードの字幕を生成。

**Args:**
- `cut`: CutDataオブジェクト
- `style`: 字幕スタイル (`'auto'`, `'none'`, `'full'`)

**Returns:** SubtitleLineオブジェクトのリスト

#### `generate_monologue_subtitles(cut, style='auto') -> List[SubtitleLine]`

モノローグモードの字幕を生成。

**Args:**
- `cut`: CutDataオブジェクト
- `style`: 字幕スタイル (通常 `'auto'` または `'without_speaker'`)

**Returns:** SubtitleLineオブジェクトのリスト

#### `generate_dialogue_subtitles(cut, style='auto') -> List[SubtitleLine]`

ダイアログモードの字幕を生成。

**Args:**
- `cut`: CutDataオブジェクト
- `style`: 字幕スタイル (`'auto'`, `'with_speaker'`, `'without_speaker'`)

**Returns:** SubtitleLineオブジェクトのリスト

#### `generate_subtitles_for_cut(cut, style=None) -> List[SubtitleLine]`

単一カットの字幕を生成（モード自動判別）。

**Args:**
- `cut`: CutDataオブジェクト
- `style`: 字幕スタイル（省略時は `cut.subtitle_style` を使用）

**Returns:** SubtitleLineオブジェクトのリスト

#### `generate_subtitles_for_storyboard(cuts, default_style='auto') -> List[CutData]`

ストーリーボード全体の字幕を生成。

**Args:**
- `cuts`: CutDataオブジェクトのリスト
- `default_style`: デフォルトの字幕スタイル

**Returns:** 字幕が追加されたCutDataオブジェクトのリスト

#### `split_text_into_lines(text, max_chars=40) -> List[str]`

長いテキストを字幕用に分割。

**Args:**
- `text`: 分割するテキスト
- `max_chars`: 1行あたりの最大文字数

**Returns:** 分割されたテキストのリスト

#### `calculate_timing(text, total_duration, num_lines, line_index) -> tuple`

字幕の表示タイミングを計算。

**Args:**
- `text`: 字幕テキスト
- `total_duration`: 利用可能な総時間（秒）
- `num_lines`: 字幕の総行数
- `line_index`: この字幕のインデックス（0始まり）

**Returns:** `(start_time, end_time)` のタプル（秒）

#### `format_subtitle_srt(cut, cut_start_time=0.0) -> str`

単一カットの字幕をSRT形式にフォーマット。

**Args:**
- `cut`: CutDataオブジェクト
- `cut_start_time`: 動画全体でのこのカットの開始時間（秒）

**Returns:** SRT形式の文字列

#### `export_srt(cuts, output_path) -> bool`

字幕をSRTファイルとしてエクスポート。

**Args:**
- `cuts`: CutDataオブジェクトのリスト
- `output_path`: 出力SRTファイルのパス

**Returns:** 成功時 `True`、失敗時 `False`

---

## 設定とカスタマイズ

### 読解速度の調整

デフォルトの読解速度は 5文字/秒 です。変更する場合：

```python
subtitle_gen = SubtitleGenerator()
subtitle_gen.CHARS_PER_SECOND = 6.0  # 高速読者向け
subtitle_gen.CHARS_PER_SECOND = 4.0  # ゆっくり読む視聴者向け
```

### 最大文字数の調整

デフォルトの最大文字数は 40文字/行 です。変更する場合：

```python
subtitle_gen.MAX_CHARS_PER_LINE = 35  # 短め
subtitle_gen.MAX_CHARS_PER_LINE = 45  # 長め
```

---

## トラブルシューティング

### 字幕が生成されない

**問題:** `cut.subtitle_lines` が空

**原因と対処法:**
1. `cut.subtitle_enabled = False` になっている → `True` に設定
2. ナレーションスタイルが `documentary` → `style='full'` を指定
3. セリフテキストがない → `narration_text`, `monologue_text`, `dialogue_lines` を設定

### 字幕が長すぎる/短すぎる

**問題:** 字幕の行が多すぎる、または少なすぎる

**対処法:**
```python
# 最大文字数を調整
subtitle_gen.MAX_CHARS_PER_LINE = 35  # より多く分割
subtitle_gen.MAX_CHARS_PER_LINE = 50  # 分割を減らす
```

### 字幕のタイミングがずれる

**問題:** 字幕の表示時間が適切でない

**対処法:**
```python
# 読解速度を調整
subtitle_gen.CHARS_PER_SECOND = 4.0  # より長く表示
subtitle_gen.CHARS_PER_SECOND = 6.0  # より短く表示

# または手動でタイミングを調整
for subtitle in cut.subtitle_lines:
    subtitle.end_time += 1.0  # 1秒延長
```

### SRTファイルが動画編集ソフトで認識されない

**問題:** SRTファイルをインポートできない

**対処法:**
1. ファイルのエンコーディングを確認（UTF-8であること）
2. ファイル名に特殊文字が含まれていないか確認
3. タイムコードが正しい形式か確認（HH:MM:SS,mmm）

---

## テスト

テストスイートで動作を確認できます：

```bash
python tests/test_subtitle_generation.py
```

テストでは以下を確認：
- ナレーション字幕生成
- モノローグ字幕生成
- ダイアログ字幕生成
- テキスト分割
- タイミング計算
- ストーリーボード全体の字幕生成
- SRTエクスポート

---

## まとめ

### 字幕生成の流れ

1. **ストーリーボード作成** → セリフ付き絵コンテを生成
2. **字幕生成器初期化** → `SubtitleGenerator()` インスタンス作成
3. **字幕生成** → `generate_subtitles_for_storyboard()` で自動生成
4. **SRTエクスポート** → `export_srt()` でファイル出力
5. **動画編集** → SRTファイルを動画編集ソフトにインポート

### 自動化されること

- ✅ ダイアログモードに応じた最適な字幕スタイル選択
- ✅ 長文の自動分割（読みやすい長さに）
- ✅ 読解速度に基づく表示タイミング計算
- ✅ 話者名の自動付与/省略
- ✅ SRT形式への自動変換

### 次のステップ

1. `tests/test_subtitle_generation.py` でサンプルを確認
2. 実際のプロジェクトで字幕を生成
3. SRTファイルを動画編集ソフトで使用
4. 必要に応じて読解速度や最大文字数を調整

---

## 参考リンク

- [Core Video Module](../core/video/subtitle_generator.py)
- [Test Suite](../tests/test_subtitle_generation.py)
- [Dialogue Modes Guide](DIALOGUE_MODES.md)
- [Voice Generation Guide](VOICE_GENERATION.md)
- [SRT Format Specification](https://en.wikipedia.org/wiki/SubRip)
