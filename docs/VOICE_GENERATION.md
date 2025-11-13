# 音声生成機能ガイド

ストーリーボードのセリフ・ナレーションをGoogle Cloud Text-to-Speech APIで音声化する機能のドキュメントです。

## 概要

CreateMovie Coreシステムは、3種類のセリフモードに対応した音声生成機能をサポートしています：

1. **Narration（ナレーション）** 🎙️ - ドキュメンタリー風の語り手による説明
2. **Monologue（モノローグ）** 💭 - 主人公1人の独白
3. **Dialogue（ダイアログ）** 💬 - 2人の登場人物の会話

コンテを作成した後に「音声を生成して」とプロンプト指定するだけで、自動的にセリフが音声化されます。

---

## 特徴

### ✅ **自動音声スタイル選択**
- キャラクター情報（年齢、性別、性格）から最適な音声を自動選択
- シーンのムード（energetic, calm, sadなど）に応じて話し方を自動調整
- 6種類の音声プロファイルを内蔵

### ✅ **3つのダイアログモード対応**
- **Narration**: ドキュメンタリー調のナレーション
- **Monologue**: キャラクター性を反映した独白
- **Dialogue**: 会話相手に応じた自然な対話

### ✅ **高品質な日本語音声**
- Google Cloud Text-to-Speech APIのNeural2音声を使用
- 自然な抑揚とイントネーション
- SSML（音声合成マークアップ言語）による細かな制御

### ✅ **ムードに応じた音声調整**
- Excited（興奮）: 速いテンポ、高めの音程
- Calm（落ち着き）: ゆっくりしたテンポ、低めの音程
- Dramatic（ドラマチック）: 強調された音量

---

## 使い方

### 基本的な使い方

```python
from core.audio.voice_generator import VoiceGenerator

# 音声生成器を初期化
voice_gen = VoiceGenerator()

# ストーリーボードの全カットの音声を生成
generated_files = voice_gen.generate_voices_for_storyboard(
    cuts=storyboard.cuts,
    output_dir="output/voices",
    use_ssml=True  # SSMLを使って抑揚を調整
)

# 生成されたファイル一覧
print(generated_files)
# {
#   'narration': ['cut_01_narration.mp3', ...],
#   'monologue': ['cut_02_monologue_主人公.mp3', ...],
#   'dialogue': ['cut_03_dialogue_1_アキラ.mp3', ...]
# }
```

### Claude Skillsから使う（自然言語）

```
あなた: "海辺の物語の絵コンテを作って"
Claude: [絵コンテを作成...]

あなた: "音声を生成して"
Claude: [自動的に全カットの音声を生成...]
```

---

## セットアップ

### 1. ライブラリのインストール

```bash
pip install google-cloud-texttospeech
```

### 2. Google Cloud認証情報の設定

1. [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
2. Text-to-Speech APIを有効化
3. サービスアカウントを作成し、JSON認証情報をダウンロード
4. 環境変数を設定：

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

### 3. 動作確認

```bash
python tests/test_voice_generation.py
```

---

## 音声プロファイル

### 内蔵プロファイル（6種類）

| プロファイル | 音声 | 性別 | 用途 |
|-------------|------|------|------|
| `narrator_male` | ja-JP-Neural2-C | 男性 | ドキュメンタリーナレーション |
| `narrator_female` | ja-JP-Neural2-A | 女性 | ドキュメンタリーナレーション |
| `character_male_young` | ja-JP-Neural2-D | 男性 | 若い元気なキャラクター |
| `character_male_mature` | ja-JP-Neural2-C | 男性 | 落ち着いた大人のキャラクター |
| `character_female_young` | ja-JP-Neural2-A | 女性 | 若い明るいキャラクター |
| `character_female_mature` | ja-JP-Neural2-A | 女性 | 落ち着いた大人のキャラクター |

### 自動選択の仕組み

```python
# キャラクター情報から自動的に音声を選択
profile = voice_gen.select_voice_profile(
    dialogue_mode='monologue',
    character_context='20代の明るい女性、元気な性格',
    mood='energetic'
)
# → character_female_young（テンポ速め）
```

**自動検出キーワード:**
- 性別: 「男性」「女性」「男」「女」「彼」「彼女」
- 年齢: 「若い」「10代」「20代」「30代」「中年」「学生」
- ムード: 「元気」「興奮」「静か」「落ち着」「悲しい」

---

## 高度な使い方

### カスタム音声プロファイル

キャラクターごとに細かく音声を指定できます：

```python
# カスタムプロファイルを定義
character_voices = {
    '主人公': {
        'voice_name': 'ja-JP-Neural2-D',
        'pitch': 0.0,           # 音程 (-20.0 ~ 20.0)
        'speaking_rate': 0.95,  # 話速 (0.25 ~ 4.0)
        'description': 'Calm thoughtful male'
    },
    'アキラ': {
        'voice_name': 'ja-JP-Neural2-C',
        'pitch': 2.0,
        'speaking_rate': 1.1,
        'description': 'Energetic cheerful male'
    },
    'ユキ': {
        'voice_name': 'ja-JP-Neural2-A',
        'pitch': 0.0,
        'speaking_rate': 0.95,
        'description': 'Gentle mature female'
    }
}

# カスタムプロファイルで音声生成
generated_files = voice_gen.generate_voices_for_storyboard(
    cuts,
    output_dir="output/voices",
    character_voices=character_voices,
    use_ssml=True
)
```

### 単一セリフの音声生成

```python
# 1つのセリフだけを音声化
text = "こんにちは、今日はいい天気ですね。"
profile = voice_gen.select_voice_profile('narration')

success = voice_gen.generate_voice(
    text=text,
    output_path="output/test.mp3",
    voice_profile=profile,
    use_ssml=True,
    mood='cheerful'
)
```

### SSML（音声合成マークアップ）

SSMLを使うと、さらに細かい音声制御が可能です：

```python
# ムードに応じてSSMLを自動生成
ssml = voice_gen.generate_ssml(
    text="これは重要なポイントです。",
    mood='dramatic',
    emphasis_words=['重要']  # 強調したい単語
)

# 結果:
# <speak>
#   <prosody rate="medium" pitch="+1st" volume="loud">
#     これは<emphasis level="strong">重要</emphasis>なポイントです。
#   </prosody>
# </speak>
```

---

## 各モードの使用例

### Mode 1: Narration（ナレーション）

```python
# ナレーション付きカット
cut.dialogue_mode = 'narration'
cut.narration_text = "物語は、静かな海辺から始まる。"
cut.narration_duration = 5.0
cut.mood = 'peaceful'

# 音声生成（自動的にドキュメンタリー調の音声が選択される）
voice_gen.generate_voices_for_storyboard([cut], "output/voices")
# → cut_01_narration.mp3
```

### Mode 2: Monologue（モノローグ）

```python
# モノローグ付きカット
cut.dialogue_mode = 'monologue'
cut.monologue_character = "主人公"
cut.monologue_text = "ここに来ると、いつも心が落ち着く。"
cut.monologue_duration = 7.2
cut.mood = 'contemplative'

# キャラクター情報を含むシーン説明から自動的に音声を選択
voice_gen.generate_voices_for_storyboard([cut], "output/voices")
# → cut_02_monologue_主人公.mp3
```

### Mode 3: Dialogue（ダイアログ）

```python
from core.video.storyboard_generator import DialogueLine

# ダイアログ付きカット
cut.dialogue_mode = 'dialogue'
cut.dialogue_characters = ['アキラ', 'ユキ']
cut.dialogue_lines = [
    DialogueLine(speaker='アキラ', text='最近、どう？', duration=2.5),
    DialogueLine(speaker='ユキ', text='元気だよ', duration=2.0)
]
cut.mood = 'warm'

# 各キャラクターの音声を自動生成
voice_gen.generate_voices_for_storyboard([cut], "output/voices")
# → cut_03_dialogue_1_アキラ.mp3
# → cut_03_dialogue_2_ユキ.mp3
```

---

## 出力ファイル構成

```
output/voices/
├── cut_01_narration.mp3              # ナレーション
├── cut_02_monologue_主人公.mp3        # モノローグ
├── cut_03_dialogue_1_アキラ.mp3       # ダイアログ（1人目）
├── cut_03_dialogue_2_ユキ.mp3         # ダイアログ（2人目）
└── cut_03_dialogue_3_アキラ.mp3       # ダイアログ（1人目・2回目）
```

各ファイル形式：
- **フォーマット**: MP3（Audio Encoding: MP3）
- **サンプルレート**: 24,000Hz（デフォルト）
- **ビットレート**: 可変（VBR）
- **モノラル音声**

---

## API仕様

### VoiceGenerator

#### `__init__(credentials_path: Optional[str] = None)`

音声生成器を初期化。

**Args:**
- `credentials_path`: Google Cloud認証情報JSONファイルのパス（省略時は環境変数 `GOOGLE_APPLICATION_CREDENTIALS` を使用）

#### `select_voice_profile(dialogue_mode, character_context, mood, gender_preference) -> Dict`

最適な音声プロファイルを自動選択。

**Args:**
- `dialogue_mode`: `'narration'`, `'monologue'`, `'dialogue'`
- `character_context`: キャラクター説明（オプション）
- `mood`: シーンのムード（オプション）
- `gender_preference`: `'male'`, `'female'`, `None`（オプション）

**Returns:**
```python
{
    'voice_name': 'ja-JP-Neural2-C',
    'pitch': 0.0,
    'speaking_rate': 1.0,
    'description': 'Documentary-style male narrator'
}
```

#### `generate_voice(text, output_path, voice_profile, use_ssml, mood) -> bool`

単一のテキストを音声化。

**Args:**
- `text`: 音声化するテキスト
- `output_path`: 出力ファイルパス（MP3）
- `voice_profile`: 音声プロファイル辞書
- `use_ssml`: SSMLを使用するか（デフォルト: `False`）
- `mood`: ムード（オプション）

**Returns:** 成功時 `True`、失敗時 `False`

#### `generate_voices_for_storyboard(cuts, output_dir, character_voices, use_ssml) -> Dict`

ストーリーボード全体の音声を生成。

**Args:**
- `cuts`: `CutData` オブジェクトのリスト
- `output_dir`: 出力ディレクトリ
- `character_voices`: カスタム音声プロファイル辞書（オプション）
- `use_ssml`: SSMLを使用するか（デフォルト: `True`）

**Returns:**
```python
{
    'narration': ['cut_01_narration.mp3', ...],
    'monologue': ['cut_02_monologue_主人公.mp3', ...],
    'dialogue': ['cut_03_dialogue_1_アキラ.mp3', ...]
}
```

---

## コスト

Google Cloud Text-to-Speech APIの料金（2025年1月現在）：

| 音声タイプ | 料金（100万文字あたり） |
|-----------|-------------------|
| Neural2 (推奨) | $16.00 |
| WaveNet | $16.00 |
| Standard | $4.00 |

**例:**
- 60秒の動画（6カット、各カット50文字のセリフ）: 300文字 = 約 $0.0048
- 音声だけなら非常に安価！

詳細: https://cloud.google.com/text-to-speech/pricing

---

## トラブルシューティング

### Google TTS APIが利用できない

**エラー**: `⚠️ Google Cloud Text-to-Speech not available`

**対処法**:
```bash
pip install google-cloud-texttospeech
```

### 認証情報が見つからない

**エラー**: `Failed to initialize Google TTS: Could not automatically determine credentials`

**対処法**:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-project-credentials.json"
```

または、コードで直接指定：
```python
voice_gen = VoiceGenerator(credentials_path="/path/to/credentials.json")
```

### APIが有効化されていない

**エラー**: `PERMISSION_DENIED: Cloud Text-to-Speech API has not been used`

**対処法**:
1. https://console.cloud.google.com/ にアクセス
2. プロジェクトを選択
3. 「APIとサービス」→「ライブラリ」
4. "Cloud Text-to-Speech API" を検索して有効化

### 音声が不自然

**問題**: 音声が機械的すぎる、抑揚がない

**対処法**:
1. `use_ssml=True` を指定してSSMLを有効化
2. カスタム音声プロファイルで `pitch` と `speaking_rate` を調整
3. テキストに句読点（「、」「。」）を適切に配置

---

## テスト

テストスイートで動作を確認できます：

```bash
python tests/test_voice_generation.py
```

テストでは以下を確認：
- 音声プロファイル自動選択
- SSML生成
- 単一音声生成
- ストーボード全体の音声生成
- カスタム音声プロファイル

---

## まとめ

### 音声生成の流れ

1. **ストーリーボード作成** → セリフ付き絵コンテを生成
2. **音声生成器初期化** → Google Cloud認証情報を設定
3. **音声生成** → `generate_voices_for_storyboard()` で自動生成
4. **出力** → MP3ファイルとして保存

### 自動化されること

- ✅ キャラクター情報から音声タイプを自動選択
- ✅ ムードに応じて話し方を自動調整
- ✅ ナレーション・モノローグ・ダイアログを自動判別
- ✅ ファイル名を自動生成

### 次のステップ

1. `tests/test_voice_generation.py` でサンプルを確認
2. Google Cloud認証情報をセットアップ
3. 実際のプロジェクトで試してみる
4. カスタム音声プロファイルで品質向上

---

## 参考リンク

- [Core Audio Module](../core/audio/voice_generator.py)
- [Test Suite](../tests/test_voice_generation.py)
- [Dialogue Modes Guide](DIALOGUE_MODES.md)
- [Google Cloud Text-to-Speech Documentation](https://cloud.google.com/text-to-speech/docs)
- [SSML Reference](https://www.w3.org/TR/speech-synthesis11/)
