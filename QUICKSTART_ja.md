# クイックスタートガイド

5分でAI動画絵コンテジェネレーターを始めよう!

## ステップ1: 依存関係のインストール

```bash
cd ai-video-storyboard
pip install -r requirements.txt
```

## ステップ2: APIキーの設定

[Google AI Studio](https://makersuite.google.com/app/apikey)から無料APIキーを取得

```bash
export GEMINI_API_KEY='your-api-key-here'
```

または `.env` ファイルを作成:

```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

## ステップ3: 最初の絵コンテを生成

### 基本例

```bash
python scripts/generate_storyboard.py "高校の文化祭準備を題材にした60秒の青春動画"
```

これにより:
- ✅ ストーリーを分析
- ✅ カメラアングルで8カットを作成
- ✅ ファーストフレーム画像を生成（Imagen 3）
- ✅ 動画生成用ItoVプロンプトを作成
- ✅ Suno用BGMプロンプトを生成

### キービジュアルあり

視覚的一貫性を維持:

```bash
python scripts/generate_storyboard.py \
  "魔法学校での一日" \
  --key-visual "path/to/concept_art.jpg"
```

### カスタム設定

```bash
python scripts/generate_storyboard.py \
  "教育動画：宇宙の仕組み" \
  --duration 60 \
  --cuts 8 \
  --output my_output \
  --title "宇宙動画"
```

## ステップ4: 出力を確認

生成後、以下の場所でファイルを確認:

```
output/
├── storyboard.json          # 完全なデータ
├── storyboard_report.md     # 視覚レポート
└── frames/                  # 生成画像
    ├── cut_01.jpg
    ├── cut_02.jpg
    └── ...
```

## よく使うオプション

| フラグ | 説明 | 例 |
|------|------|-----|
| `--duration` | 動画の長さ（秒） | `--duration 60` |
| `--cuts` | カット数 | `--cuts 8` |
| `--key-visual` | 参照画像 | `--key-visual ref.jpg` |
| `--output` | 出力ディレクトリ | `--output my_video` |
| `--style` | 視覚スタイル | `--style anime` |
| `--no-images` | 画像生成をスキップ | `--no-images` |
| `--no-music` | 音楽プロンプトをスキップ | `--no-music` |

## ユースケース別の例

### 教育動画

```bash
python scripts/generate_storyboard.py \
  "教育コンテンツ：光合成の仕組み" \
  --style "educational illustration" \
  --duration 60
```

### マーケティング動画

```bash
python scripts/generate_storyboard.py \
  "新製品スマートフォンの紹介" \
  --style "dynamic cinematic" \
  --duration 30 \
  --cuts 6
```

### ナラティブショート

```bash
python scripts/generate_storyboard.py \
  "友情をテーマにした感動ストーリー" \
  --key-visual "character_design.jpg" \
  --duration 60
```

## 次のステップ

1. **出力をレビュー**: `output/storyboard_report.md`を確認
2. **必要に応じて調整**: プロンプトを修正して特定のカットを再生成
3. **動画を生成**: ItoVプロンプトを動画生成ツールで使用
4. **音楽を追加**: SunoプロンプトでBGMを生成

## トラブルシューティング

### 「APIキーが見つかりません」

```bash
export GEMINI_API_KEY='your-key'
```

### 「モジュールが見つかりません」

```bash
pip install -r requirements.txt
```

### 「画像が暗すぎる」

出力のプロンプトを調整して再生成:
```
"明るい照明、よく照らされた、ゴールデンアワーの太陽光"
```

## さらに詳しく

- **[SKILL_ja.md](SKILL_ja.md)** - 完全なドキュメント
- **[カメラショットガイド](references/camera_shots_ja.md)** - ショット選択
- **[トラブルシューティング](references/troubleshooting_ja.md)** - 一般的な問題

## サポート

ヘルプが必要ですか？以下を確認:
1. [トラブルシューティングガイド](references/troubleshooting_ja.md)
2. 詳細な使用方法は[SKILL_ja.md](SKILL_ja.md)
3. サンプル絵コンテは[Examples](assets/examples/)

楽しい制作を! 🎬
