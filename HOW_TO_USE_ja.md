# 使い方ガイド

## 📝 概要

このClaude Skillは**2つの方法**で使用できます：

### 方法1: Claude Skillとして使用（推奨）🌟

Claude Codeの中で自然言語で話しかけるだけで、Claudeが自動的にこのスキルを使って絵コンテを作成します。

### 方法2: Pythonスクリプトとして直接実行（上級者向け）

ターミナルから直接Pythonスクリプトを実行します。

---

## 🎬 方法1: Claude Skillとして使用（推奨）

### セットアップ

1. **このフォルダをClaude Codeで開く**

```bash
# VS CodeでClaude Code拡張を有効にして、このフォルダを開く
code /path/to/ai-video-storyboard
```

2. **Gemini APIキーを設定**

```bash
export GEMINI_API_KEY='your-api-key-here'
```

または `.env` ファイルに追加:
```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

3. **依存関係をインストール**

```bash
pip install -r requirements.txt
```

### 使い方

Claude Codeのチャットで以下のように話しかけるだけです：

#### 例1: 基本的な絵コンテ作成

```
あなた: 高校の文化祭準備を題材にした60秒の青春動画の絵コンテを作成して
```

**Claudeの動作:**
1. ストーリーを分析
2. 6-10カットの構成を決定
3. 各カットのカメラアングル、構図、動きを選択
4. Imagen 3で画像を生成
5. ItoVプロンプトを作成
6. Suno用BGMプロンプトを生成
7. 結果を `output/` フォルダに保存

#### 例2: キービジュアルを使用

```
あなた: このコンセプトアート(concept.jpg)のスタイルで、魔法学校での一日をテーマにした動画の絵コンテを作って
```

**Claudeの動作:**
1. concept.jpgを解析（スタイル、色、ムード）
2. 全カットに一貫したスタイルを適用
3. 統一感のある絵コンテを生成

#### 例3: カスタム設定

```
あなた: 教育動画「水の循環」の絵コンテを作成。
- 60秒
- 8カット
- 教育イラストスタイル
- 明るくクリーンな雰囲気
```

#### 例4: 特定のシーンだけ作成

```
あなた: オープニングシーン（10秒）の絵コンテだけ作って。
超広角で朝の教室を映すシーン。
```

### 出力の確認

生成後、以下のファイルが作成されます：

```
output/
├── storyboard.json          # JSONデータ
├── storyboard_report.md     # 画像付きレポート
├── music_plan.json          # BGM情報（オプション）
└── frames/                  # 生成画像
    ├── cut_01.jpg
    ├── cut_02.jpg
    └── ...
```

### 調整と再生成

```
あなた: Cut 3の画像が暗すぎるので、明るい照明で再生成して
```

```
あなた: 全体的にもっとアニメスタイルにして
```

---

## 💻 方法2: Pythonスクリプトとして直接実行

### 基本コマンド

```bash
python scripts/generate_storyboard.py "ストーリー説明"
```

### オプション付きコマンド

```bash
python scripts/generate_storyboard.py \
  "高校の文化祭準備を題材にした60秒の青春動画" \
  --duration 60 \
  --cuts 8 \
  --output my_storyboard \
  --title "文化祭動画"
```

### キービジュアル使用

```bash
python scripts/generate_storyboard.py \
  "魔法学校での一日" \
  --key-visual "path/to/concept.jpg"
```

### 全オプション

| オプション | 説明 | デフォルト |
|-----------|------|----------|
| `--duration` | 動画の長さ（秒） | 60 |
| `--cuts` | カット数 | 自動（6-10） |
| `--key-visual` | 参照画像パス | なし |
| `--output` | 出力ディレクトリ | output |
| `--title` | タイトル | AI Generated Storyboard |
| `--style` | 視覚スタイル | cinematic |
| `--no-images` | 画像生成スキップ | False |
| `--no-music` | 音楽生成スキップ | False |

### Pythonコードから使用

```python
from scripts.generate_storyboard import create_complete_storyboard

# 基本使用
storyboard = create_complete_storyboard(
    story="高校の文化祭準備を題材にした60秒の青春動画"
)

# カスタム設定
storyboard = create_complete_storyboard(
    story="教育動画：宇宙の仕組み",
    config={
        "duration": 60,
        "num_cuts": 8,
        "visual_style": "educational",
        "generate_images": True,
        "generate_music": True
    }
)

# キービジュアル使用
storyboard = create_complete_storyboard(
    story="ファンタジー冒険",
    key_visual_path="concept.jpg",
    config={
        "enforce_visual_consistency": True
    }
)
```

---

## 🎯 どちらを選ぶべき？

### Claude Skillとして使用（推奨）👍

**メリット:**
- 自然言語で簡単に指示できる
- Claudeが最適な設定を自動選択
- 反復改善が簡単
- 対話的に調整可能

**こんな人におすすめ:**
- プログラミング経験が少ない
- 素早くプロトタイプを作りたい
- 対話的に調整したい

### Pythonスクリプトとして使用

**メリット:**
- 完全なコントロール
- バッチ処理可能
- 自動化/スクリプト化できる
- パイプラインに組み込める

**こんな人におすすめ:**
- プログラミング経験がある
- 大量のコンテンツを自動生成
- CI/CDパイプラインに組み込みたい

---

## 💡 使用例シナリオ

### シナリオ1: 教育YouTuber

**Claude Skillとして使用:**

```
あなた: "光合成の仕組み"の60秒説明動画の絵コンテを作って。
明るくて分かりやすいイラストスタイルで。
```

↓ Claudeが自動生成 ↓

```
あなた: Cut 3の図をもっと詳しくして
```

↓ 調整 ↓

```
あなた: OKこれで画像を全部生成して
```

### シナリオ2: マーケティングチーム

**Pythonスクリプトで一括生成:**

```bash
# 複数の商品動画を一括生成
for product in smartphone tablet laptop; do
  python scripts/generate_storyboard.py \
    "新製品${product}の魅力を伝える30秒CM" \
    --duration 30 \
    --output "output/${product}" \
    --style "dynamic cinematic"
done
```

### シナリオ3: 個人クリエイター

**Claude Skillで対話的に:**

```
あなた: 友情をテーマにした感動的な60秒ショートフィルムの絵コンテを作って
```

```
Claude: [絵コンテを生成]
```

```
あなた: いい感じ！でももう少し感情的な瞬間を増やして
```

```
Claude: [調整版を生成]
```

---

## 🔧 トラブルシューティング

### 「APIキーが見つかりません」

```bash
export GEMINI_API_KEY='your-key'
```

### 「モジュールが見つかりません」

```bash
pip install -r requirements.txt
```

### Claude Skillが認識されない

1. このフォルダがClaude Codeで開かれているか確認
2. SKILL.mdファイルが存在するか確認
3. Claude Codeを再起動

---

## 📚 さらに詳しく

- **[SKILL_ja.md](SKILL_ja.md)** - 完全なスキルドキュメント
- **[QUICKSTART_ja.md](QUICKSTART_ja.md)** - クイックスタート
- **[references/](references/)** - 詳細リファレンス

---

**推奨**: まずは**Claude Skillとして**使ってみてください！
対話的に使えて、とても簡単です。 🎬✨
