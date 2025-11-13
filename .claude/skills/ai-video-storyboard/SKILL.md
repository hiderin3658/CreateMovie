---
name: ai-video-storyboard
description: 1分動画（6-10カット）の絵コンテ、画像プロンプト、ItoVプロンプトを作成するAI動画制作アシスタント。Gemini API（Imagen 3）を使用してファーストフレーム画像を生成。最適な構図とカメラワークを自動選択。🆕3種類のセリフモード（ナレーション、モノローグ、ダイアログ）でキャラクター性のある動画を作成。Claude APIで自然な会話を自動生成。🆕Google Cloud Text-to-Speechで音声を自動生成（キャラクター性・ムード反映、SSML対応）。AI生成動画、絵コンテ、動画制作計画、視覚的なナラティブを持つ教育コンテンツの作成時に使用。
---

# AI動画絵コンテジェネレーター

AI画像生成、カメラワーク選択、音楽プロンプト生成で動画絵コンテ作成を自動化。

## このスキルの使い方

### Claude Skillとして使用（推奨）

これは**Claude Skill**で、Claude Code内で使用するように設計されています。作りたいものを自然言語で説明するだけです：

**Claudeとの会話例：**

```
あなた: "高校の文化祭準備を題材にした60秒の青春動画の絵コンテを作成して"

Claudeが自動で:
1. ストーリーを分析
2. 最適なカメラワークで6-10カットを作成
3. Imagen 3用の画像プロンプトを生成
4. 動画生成用のItoVプロンプトを作成
5. Suno用のBGMプロンプトを生成
6. ナレーション/セリフを自動生成（オプション）
```

**NEW! セリフ付き動画:**
```
あなた: "主人公が一人で語りかける形式で、自分探しの旅をテーマにした動画を作って"

Claudeが自動で:
1. モノローグモードで絵コンテを生成
2. 主人公のキャラクター設定
3. 各カットに主人公のセリフを追加
4. セリフの長さを自動調整
```

**会話シーン付き:**
```
あなた: "2人の友人が人生について語り合うカフェシーンの動画を作って"

Claudeが自動で:
1. ダイアログモードで絵コンテを生成
2. 2人のキャラクター設定
3. 自然な会話を生成
4. 会話の流れに合わせたカメラワーク
```

**キービジュアルあり:**
```
あなた: "このコンセプトアート(image.jpg)のスタイルで魔法学校の動画を作って"

Claudeが自動で:
1. キービジュアルのスタイルを解析
2. 全カットに一貫したスタイルを適用
3. 統一感のある絵コンテを生成
```

### Pythonスクリプトとして使用（上級者向け）

ターミナルから直接Pythonスクリプトを実行することもできます：

```bash
python scripts/generate_storyboard.py "ストーリー説明"
```

## 前提条件

### 必須: Gemini APIキー

Gemini APIキーを環境変数として設定:

```bash
export GEMINI_API_KEY='your-api-key-here'
```

または `.env` ファイルを作成:

```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

### オプション依存関係

Python依存関係をインストール:

```bash
pip install google-generativeai pillow numpy scikit-learn scipy
```

## クイックスタート

### 基本的な使い方（完全自動）

1つのコマンドで完全な絵コンテを生成:

```bash
python scripts/generate_storyboard.py "高校の文化祭準備を題材にした60秒の青春動画"
```

AIが自動的に:
- ✅ 6-10カットの構成を決定
- ✅ カメラアングルと動きを選択
- ✅ 構図を選択（三分割法、中央配置など）
- ✅ 照明とムードを設定
- ✅ Imagen 3画像を生成
- ✅ 動画生成用ItoVプロンプトを作成
- ✅ Suno用BGMプロンプトを生成

### キービジュアル参照を使用

参照画像を使用して視覚的一貫性を維持:

```bash
python scripts/generate_storyboard.py \
  "魔法学校での一日" \
  --key-visual "path/to/concept_art.jpg"
```

これにより:
- 参照からアートスタイル、色、ムードを抽出
- 全カットに一貫したスタイルを適用
- 全体を通して視覚的な一貫性を維持

### 動画モデル選択

特定のAI動画モデルに最適化されたプロンプトを生成:

```bash
# Veo 3.1用（技術的、正確）
python scripts/generate_storyboard.py "アクション動画" --model veo3

# Sora 2用（描写的、芸術的）
python scripts/generate_storyboard.py "感動的な動画" --model sora2

# 自動（両モデル）
python scripts/generate_storyboard.py "動画" --model auto
```

## ワークフロー

### 1. ストーリー入力

ストーリー説明を提供:

```python
from scripts.generate_storyboard import create_complete_storyboard

storyboard = create_complete_storyboard(
    story="教育コンテンツ：水の循環を説明する60秒動画",
    config={
        "duration": 60,
        "num_cuts": 8,
        "style": "educational"
    }
)
```

### 2. 自動シーン分解

AIがストーリーを分析して作成:
- カット構成（6-10カット）
- シーン説明
- カメラアングル（ELS、LS、MS、CU、ECU）
- 構図（三分割法、黄金比など）
- カメラ動き（パン、ズーム、ドリー、トラッキング）

### 3. 画像生成

Gemini API（Imagen 3）を使用してファーストフレーム画像を生成:

```python
# 画像は自動生成され output/frames/ に保存されます
# - cut_01.jpg
# - cut_02.jpg
# - ...
```

### 4. ItoVプロンプト生成

画像から動画への変換用の動画プロンプトを作成:

```
ItoVプロンプト例:
"ゆっくりズームイン、賑やかな学生の活動、10秒、
ムードを確立、最初のフレーム構図を全体で維持"
```

### 5. BGMプロンプト生成

Suno用の音楽プロンプトを自動生成:

```python
# セクション1（カット1-3、25秒）
"[Hopeful intro] Cinematic orchestral, 80bpm, soft,
anticipation building, piano, strings, soft percussion"

# セクション2（カット4-6、20秒）
"[Energetic main] Uplifting pop-rock, 120bpm, energetic,
excitement, guitar, drums, bass, synth"
```

## 🆕 ダイアログモード（セリフ生成）

3種類のセリフモードで、キャラクター性のある動画を作成できます：

### モード1: ナレーション（Narration）
ドキュメンタリー風の語り手による説明。

**使い方:**
```
"教育動画で水の循環を説明する60秒の動画を、ナレーション付きで作って"
```

**特徴:**
- 客観的な語り
- 状況説明に最適
- ドキュメンタリー、教育コンテンツ向け

### モード2: モノローグ（Monologue）
主人公1人が自分の思いを語る形式。

**使い方:**
```
"30代の会社員が人生に疲れて自然の中で癒しを求める物語を、
主人公の独白形式で60秒の動画にして"
```

**特徴:**
- 主観的な語り
- 感情表現、内面描写に最適
- 個人の物語、心境の変化を描く

**キャラクター設定例:**
```
主人公: 田中太郎
性格: 真面目で繊細、疲れているが前向き
現在の状況: 仕事のストレスで限界、週末に一人旅を決意
```

### モード3: ダイアログ（Dialogue）
2人のキャラクターが会話する形式。

**使い方:**
```
"2人の友人がカフェで人生について語り合う60秒の動画を作って。
1人目は楽観的な性格、2人目は真面目で悩んでいる感じで"
```

**特徴:**
- 複数視点
- 対話、関係性の描写に最適
- ドラマ、人間関係を描く

**キャラクター設定例:**
```
キャラクター1: アキラ
性格: 楽観的で明るい、友人のことを心配している
話し方: フランクで親しみやすい

キャラクター2: ユキ
性格: 真面目で控えめ、最近仕事で悩んでいる
話し方: 丁寧で少し固い
```

### セリフ自動生成の仕組み

**Claude APIによる生成:**
- ストーリーコンテキストを分析
- キャラクター性を反映
- 各カットの長さに合わせて自動調整（日本語: 約300文字/分）
- 前後のカットとの流れを考慮

**生成されるもの:**
- セリフテキスト（日本語）
- 推定発話時間
- タイミング情報（start/end/throughout）

### モード選択のガイド

| モード | 用途 | 例 |
|--------|------|-----|
| **Narration** | 説明、状況描写 | ドキュメンタリー、教育動画 |
| **Monologue** | 感情、内面 | 自分探しの旅、心境の変化 |
| **Dialogue** | 対話、関係性 | 友人との会話、恋愛、議論 |

### セリフなしも可能

セリフが不要な場合は、従来通り映像のみの絵コンテを生成できます。

```
"音楽だけで魅せる、美しい風景の60秒動画を作って"
```

## 🆕 音声生成（Voice Generation）

コンテ作成後、セリフを音声化できます！Google Cloud Text-to-Speechを使用して、自然な日本語音声を自動生成します。

### 基本的な使い方

```
あなた: "海辺の物語の絵コンテを作って"
Claude: [絵コンテを作成...]

あなた: "音声を生成して"
Claude: [自動的に全カットの音声を生成...]
```

### 特徴

**✅ 自動音声スタイル選択**
- キャラクター情報（年齢、性別、性格）から最適な音声を自動選択
- シーンのムード（energetic, calm, sadなど）に応じて話し方を自動調整
- 6種類の音声プロファイルを内蔵（男性・女性 × 若い・成熟 × ナレーター・キャラクター）

**✅ 3つのダイアログモード対応**
- **Narration**: ドキュメンタリー調のナレーション
- **Monologue**: キャラクター性を反映した独白
- **Dialogue**: 会話相手に応じた自然な対話

**✅ 高品質な日本語音声**
- Google Cloud Text-to-Speech APIのNeural2音声を使用
- 自然な抑揚とイントネーション
- SSML（音声合成マークアップ言語）による細かな制御

### セットアップ

音声生成を使うには、Google Cloud認証情報が必要です：

```bash
# 1. ライブラリのインストール
pip install google-cloud-texttospeech

# 2. 環境変数を設定
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

詳細なセットアップ手順は [VOICE_GENERATION.md](../../docs/VOICE_GENERATION.md) を参照してください。

### 使用例

**ナレーション音声:**
```
あなた: "ドキュメンタリー風のナレーションで音声を生成して"
→ 落ち着いたドキュメンタリー調の音声が生成されます
```

**キャラクター音声（モノローグ）:**
```
あなた: "主人公の独白を20代の男性の声で音声化して"
→ 若い男性の声で独白を生成します
```

**会話音声（ダイアログ）:**
```
あなた: "2人の会話を音声化して。アキラは元気な男性、ユキは落ち着いた女性で"
→ それぞれのキャラクター性を反映した音声を生成します
```

### 自動選択される音声プロファイル

| プロファイル | 音声 | 用途 |
|-------------|------|------|
| narrator_male | ja-JP-Neural2-C | 男性ナレーション |
| narrator_female | ja-JP-Neural2-A | 女性ナレーション |
| character_male_young | ja-JP-Neural2-D | 若い男性キャラ |
| character_male_mature | ja-JP-Neural2-C | 成熟した男性キャラ |
| character_female_young | ja-JP-Neural2-A | 若い女性キャラ |
| character_female_mature | ja-JP-Neural2-A | 成熟した女性キャラ |

### カスタム音声設定

より細かく音声を制御したい場合：

```
あなた: "主人公の声をもっと低めにして、ゆっくり話す感じにして"
Claude: [音程とスピードを調整した音声を生成...]
```

### 出力ファイル

音声ファイルは MP3 形式で保存されます：

```
output/voices/
├── cut_01_narration.mp3              # ナレーション
├── cut_02_monologue_主人公.mp3        # モノローグ
├── cut_03_dialogue_1_アキラ.mp3       # ダイアログ（1人目）
└── cut_03_dialogue_2_ユキ.mp3         # ダイアログ（2人目）
```

### コスト

Google Cloud Text-to-Speech APIの料金（Neural2音声）：
- **$16.00 / 100万文字**
- 60秒動画（6カット、各50文字） = 約 **$0.0048**

非常に安価に音声を生成できます！

詳細: https://cloud.google.com/text-to-speech/pricing

## 高度な機能

### 反復改善

生成されたプロンプトをレビューして調整:

```python
# 1. 初期絵コンテを生成
storyboard = create_complete_storyboard(story)

# 2. 特定のカットをレビュー
print(storyboard.cuts[2].image_prompt)

# 3. 必要に応じて修正
storyboard.cuts[2].image_prompt = """
超広角ショット、ドラマチックな雲が形成、
タイムラプス効果、ボリューメトリックライティング、
壮大なスケール、詳細な積乱雲
"""

# 4. そのカットを再生成
regenerate_cut(storyboard, cut_number=3)
```

### キービジュアル解析

参照画像からスタイルを抽出:

```python
from scripts.visual_reference_analyzer import VisualReferenceAnalyzer

analyzer = VisualReferenceAnalyzer()
analysis = analyzer.analyze_key_visual("concept_art.jpg")

print(f"スタイル: {analysis.style}")
print(f"色: {analysis.colors}")
print(f"ムード: {analysis.mood}")
```

### 音楽の感情アーク

音楽セクションを分析して生成:

```python
from scripts.music_generator_suno import MusicPromptGenerator

music_gen = MusicPromptGenerator()
music_plan = music_gen.generate_complete_music_plan(storyboard)

print(f"セクション数: {len(music_plan['sections'])}")
print(f"感情アーク: {music_plan['emotional_arc']['overall_journey']}")
```

## 出力ファイル

生成後、以下が作成されます:

```
output/
├── storyboard.json              # 完全な絵コンテデータ
├── storyboard_report.md         # 画像付き視覚レポート
├── music_plan.json              # BGMセクションデータ
├── suno_prompts.md              # すぐに使えるSunoプロンプト
└── frames/                      # 生成画像
    ├── cut_01.jpg
    ├── cut_02.jpg
    └── ...
```

## カメラワークリファレンス

### 自動ショット選択

AIはシーンタイプに基づいて適切なショットを自動選択:

- **確立シーン** → ELS（超遠景）
- **キャラクター紹介** → MS（中景）
- **対話** → MS/MCU（中景/ミディアムクローズアップ）
- **アクションシーケンス** → LS/MS（遠景/中景）
- **感情的な瞬間** → CU/ECU（クローズアップ/超クローズアップ）
- **結論** → LS/ELS

### カメラ動き

ムードとアクションに基づいて自動選択:

- **静止**: 対話、観察
- **パン**: 広い空間の紹介
- **ズーム**: 注意を引く、驚き
- **ドリー**: 没入感、接近
- **トラッキング**: アクションの追跡

詳細は [references/camera_shots.md](references/camera_shots.md) を参照。

## 構図ガイド

### 自動選択される構図

- **三分割法**: 一般的なシーン、風景
- **黄金比**: 芸術的なシーン、美しさの強調
- **中央配置**: キャラクター紹介、フォーマルなシーン
- **対角線**: アクション、ダイナミックなシーン

詳細は [references/composition_guide.md](references/composition_guide.md) を参照。

## トラブルシューティング

### APIエラー

**エラー: APIキーが見つかりません**
```bash
# APIキーを設定
export GEMINI_API_KEY='your-key'
```

**エラー: レート制限超過**
```python
# リクエスト間に遅延を追加
config = {"api_delay": 2.0}  # 呼び出し間に2秒
```

### 画像生成の問題

**問題: 画像が暗すぎる**
```python
# 照明修飾子を追加
"明るい照明、よく照らされた、ゴールデンアワー"
```

**問題: キャラクターが足りない**
```python
# 数を指定
"混雑したシーン、15-20人、忙しい雰囲気"
```

**問題: 構図が中心からずれている**
```python
# 構図を明示的に指定
"中央配置構図、対称的なレイアウト"
```

### プロンプト最適化

より良い結果を得るために:

1. **具体的に**: "窓からの柔らかい朝日" > "良い照明"
2. **文脈を追加**: "制服を着た生徒が文化祭の飾り付けを準備"
3. **ムードを含める**: "明るい雰囲気、暖かい色、楽観的なムード"
4. **スタイルを指定**: "アニメスタイル、セルシェーディング、鮮やかな色"

詳細なソリューションは [references/troubleshooting.md](references/troubleshooting.md) を参照。

## 例

### 教育動画

```python
storyboard = create_complete_storyboard(
    "宇宙の仕組みを説明する60秒の教育動画",
    config={
        "style": "educational",
        "pacing": "steady",
        "visual_style": "clear and informative"
    }
)
```

### マーケティング動画

```python
storyboard = create_complete_storyboard(
    "新製品スマートフォンの魅力を伝える60秒CM",
    config={
        "style": "marketing",
        "pacing": "fast",
        "visual_style": "dynamic and engaging"
    }
)
```

### ナラティブ動画

```python
storyboard = create_complete_storyboard(
    "友情をテーマにした感動的な60秒ショートフィルム",
    config={
        "style": "narrative",
        "pacing": "varies with story",
        "visual_style": "cinematic"
    }
)
```

## APIコスト

Gemini API（Imagen 3）の使用:

- **画像生成**: 1画像あたり約$0.03
- **8カット動画**: 合計約$0.24
- **10カット動画**: 合計約$0.30

ビジョン解析（キービジュアル用）:
- **画像あたり**: 約$0.001

## ベストな結果を得るためのヒント

1. **シンプルに始める**: 最初はAIに基本を任せる
2. **徐々に反復**: 一度に1つの要素を調整
3. **参照を使用**: キービジュアルは一貫性を向上
4. **構図をチェック**: 自動選択されたカメラワークをレビュー
5. **音楽の同期をテスト**: BGMが感情の流れに合っているか確認
6. **反復を保存**: 比較のためにバージョン履歴を保持

## サポート

詳細なドキュメント:
- [カメラショットリファレンス](references/camera_shots.md)
- [構図ガイド](references/composition_guide.md)
- [カメラ動き](references/camera_movements.md)
- [ItoVパターン](references/itov_patterns.md)
- [動画モデル最適化](references/video_model_patterns.md)
- [トラブルシューティングガイド](references/troubleshooting.md)

## ライセンス

MITライセンス
