# トラブルシューティング ガイド

AIビデオストーリーボード生成における一般的な問題への包括的な解決策。

## 目次

1. [APIおよびセットアップの問題](#apiおよびセットアップの問題)
2. [画像生成の問題](#画像生成の問題)
3. [ビデオプロンプトの問題](#ビデオプロンプトの問題)
4. [構図とカメラの問題](#構図とカメラの問題)
5. [スタイル一貫性の問題](#スタイル一貫性の問題)
6. [音楽生成の問題](#音楽生成の問題)
7. [パフォーマンスと品質](#パフォーマンスと品質)

---

## APIおよびセットアップの問題

### 問題: "GEMINI_API_KEY not found"

**症状**: スタートアップ時のエラーメッセージ、画像生成なし

**解決策**:

1. **環境変数を設定**:
```bash
export GEMINI_API_KEY='your-api-key-here'
```

2. **.envファイルを作成**:
```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

3. **コード内で直接渡す**:
```python
generator = StoryboardGenerator(api_key='your-key')
```

4. **キーが設定されていることを確認**:
```bash
echo $GEMINI_API_KEY
```

---

### 問題: "Rate limit exceeded"

**症状**: 複数のリクエスト後のAPIエラー

**解決策**:

1. **リクエスト間に遅延を追加**:
```python
config = {"api_delay": 2.0}  # 2 seconds between calls
```

2. **少ない数のカットでバッチ処理**:
```python
config = {"num_cuts": 6}  # Reduce from default 8
```

3. **待機して再試行**:
- Gemini無料版: 毎分60リクエスト
- 60秒待ってから再試行

4. **APIプランをアップグレード**:
- より高い制限のための有料版を検討

---

### 問題: "API authentication failed"

**症状**: 401または403エラー

**解決策**:

1. **APIキーが正しいことを確認**:
- タイプミスがないか確認
- 余分なスペースがないか確認
- Google AI StudioからAPIキーをコピーし直す

2. **APIキーの権限を確認**:
- Imagen 3へのアクセスが有効化されていることを確認
- Gemini APIへのアクセスを確認

3. **APIキーを再生成**:
- Google AI Studioへ移動
- 新しいキーを生成
- 環境内で更新

---

### 問題: "Module not found errors"

**症状**: google.genaiまたは他のモジュールのImportError

**解決策**:

1. **依存関係をインストール**:
```bash
pip install google-generativeai pillow numpy scikit-learn scipy
```

2. **requirements ファイルを使用**:
```bash
pip install -r requirements.txt
```

3. **Pythonバージョンを確認**:
```bash
python --version  # Should be 3.8+
```

4. **仮想環境を使用**:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 画像生成の問題

### 問題: "Generated images are too dark"

**症状**: すべての画像が暗いまたは影がかった状態に見える

**解決策**:

1. **明示的なライティングを追加**:
```python
"bright lighting, well-lit scene, golden hour sunlight"
```

2. **光源を指定**:
```python
"natural daylight from window, soft diffused lighting"
```

3. **明るさを上げる**:
```python
"high key lighting, bright atmosphere, overexposed for brightness"
```

4. **ムード記述を調整**:
- 「moody（暗い）」から「cheerful（明るい）」に変更
- 「dramatic（劇的）」から「bright（明るい）」に変更

**修正例**:
```
# Before (too dark)
"classroom scene, students preparing"

# After (brighter)
"brightly lit classroom scene, students preparing,
sunlight streaming through windows, warm daylight,
cheerful atmosphere"
```

---

### 問題: "Not enough characters/people in scene"

**症状**: 期待した群衆だが、1～2人しか現れない

**解決策**:

1. **人数を明確に指定**:
```python
"15-20 students, crowded classroom, many people"
```

2. **群衆記述子を使用**:
```python
"busy scene, populated, bustling with activity"
```

3. **分布を説明**:
```python
"students throughout frame, some in foreground, groups in background"
```

4. **活動インジケーターを追加**:
```python
"multiple students working on different tasks, various groups"
```

**修正例**:
```
# Before (too few people)
"classroom with students"

# After (more people)
"busy classroom with 15-20 students, crowded scene,
diverse group working together, multiple clusters of activity,
students in foreground and background, bustling atmosphere"
```

---

### 問題: "Characters don't match description"

**症状**: キャラクターが指定されたものと異なる

**解決策**:

1. **非常に具体的な説明を使用**:
```python
"teenage girl, long black hair, school uniform, specific appearance"
```

2. **主要ビジュアルを参照**:
```python
# Use --key-visual flag
python scripts/generate_storyboard.py "story" --key-visual "character.jpg"
```

3. **すべてのプロンプトで指定**:
```python
"same teenage girl as before, long black hair, consistent appearance"
```

4. **キャラクターシートを使用**:
- まずキャラクター参照を生成
- その後の各カットで参照

---

### 問題: "Composition is off-center or unbalanced"

**症状**: 重要な要素がカットオフされたか、フレーミングが不十分

**解決策**:

1. **構図を明示的に指定**:
```python
"centered composition, subject in center frame"
```

2. **特定の配置を使用**:
```python
"subject on left third following rule of thirds"
```

3. **フレーミング指示を追加**:
```python
"ensure full body visible in frame, well-framed"
```

4. **ショットタイプを確認**:
- ELSは広すぎる可能性
- MSまたはLSを試す

**修正例**:
```
# Before (cut off)
"person in scene"

# After (well-framed)
"person centered in frame, medium shot,
rule of thirds composition, full body visible,
proper headroom, well-balanced framing"
```

---

### 問題: "Generated image doesn't match prompt"

**症状**: AIがキープロンプト要素を無視

**解決策**:

1. **プロンプトを単純化**:
- 複雑すぎる → AIが理解する内容を選択
- 重要な要素のみに分割

2. **要素に優先順位を付ける**:
```python
"[MOST IMPORTANT], [secondary], [nice to have]"
```

3. **矛盾する指示を削除**:
```python
# Bad: "dark mysterious bright cheerful"
# Good: "mysterious atmosphere with soft lighting"
```

4. **一貫した用語を使用**:
- 一般的な映画用語に固執
- 専門用語や混合メタファーを避ける

5. **バリエーションで再生成**:
```python
config = {"variations_per_cut": 3}
# Pick best result
```

---

### 問題: "Style inconsistency between cuts"

**症状**: 各カットが異なるアートスタイルに見える

**解決策**:

1. **主要ビジュアル参照を使用**:
```bash
python scripts/generate_storyboard.py "story" --key-visual "reference.jpg"
```

2. **すべてのプロンプトにスタイルを追加**:
```python
"anime style, cel-shaded, consistent art style"
```

3. **カラーパレットを一貫して指定**:
```python
"color palette: #FFE4B5, #87CEEB, #98FB98"
```

4. **スタイルガイドを使用**:
```python
config = {
    "visual_style": "cinematic",
    "enforce_consistency": True
}
```

---

### 問題: "Safety filter blocked generation"

**症状**: 「Content policy violation」エラー

**解決策**:

1. **機密性のある内容がないかプロンプトを確認**:
- 暴力的な用語を削除
- 成熟したテーマを避ける
- より安全な代替案を使用

2. **問題のある用語を言い換える**:
```python
# Instead of "fighting"
"sports competition, training scene"

# Instead of "weapons"
"training equipment, props"
```

3. **コンテキストが重要**:
- 「教育的」または「芸術的背景」を追加
- 「アニメーション」または「イラスト」を指定

4. **シーンを単純化**:
- 複雑なアクションを削除
- より単純な構図に焦点を当てる

---

## ビデオプロンプトの問題

### 問題: "Video doesn't follow ItoV prompt"

**症状**: 生成されたビデオの動きがプロンプトと異なる

**解決策**:

1. **動きを単純化**:
```python
# Too complex
"dolly in while panning left and tilting up"

# Simpler
"slow zoom in, 8 seconds"
```

2. **より具体的にする**:
```python
# Vague
"camera moves"

# Specific
"slow dolly forward, approaching subject, 10 seconds"
```

3. **一貫性の指示を追加**:
```python
"maintain first frame composition throughout"
```

4. **最初のフレームに合わせる**:
- 開始位置から動きが理にかなっていることを確認
- 動きを念頭に置いて最初のフレームを設計

---

### 問題: "Video movement too fast or slow"

**症状**: ペーシングがぎこちなく感じられる

**解決策**:

1. **正確な期間を指定**:
```python
"slow zoom in over exactly 12 seconds"
```

2. **速度記述子を使用**:
```python
# Slower
"very slow, gradual, barely perceptible"

# Faster
"quick, brisk, rapid"
```

3. **コンテンツに合わせて調整**:
- 感情シーン: より長く（10～15秒）
- アクションシーン: より短く（3～6秒）

4. **異なる期間をテスト**:
- 6秒、8秒、10秒版を試す
- 結果を比較

---

### 問題: "First frame changes in video"

**症状**: 開始画像がビデオの終了フレームと一致していない

**解決策**:

1. **明示的な一貫性を追加**:
```python
"maintain first frame composition, preserve starting image elements"
```

2. **サブジェクトの動きを最小化**:
```python
"subtle movement only, keep character position stable"
```

3. **ロックカメラを使用**:
```python
"static camera, no camera movement, stable frame"
```

4. **保持するものを指定**:
```python
"keep character appearance consistent, maintain lighting throughout"
```

---

## 構図とカメラの問題

### 問題: "Wrong camera angle for scene"

**症状**: クローズアップが必要な時に広角、またはその逆

**解決策**:

1. **自動選択を確認**:
```python
# Opening should be ELS
# Dialogue should be MS
# Emotion should be CU
```

2. **手動でオーバーライド**:
```python
cut.camera_angle = 'ELS'  # Force extreme long shot
```

3. **特定の角度で再生成**:
```python
"extreme wide shot, vast landscape, establishing shot"
```

4. **シーンタイプを確認**:
- 誤って分類された可能性
- シーンタイプを意図に合わせて調整

---

### 問題: "Camera movement doesn't match mood"

**症状**: 静かなシーンで高速移動、アクションシーンで静止

**解決策**:

1. **気分と動きのマトリックスを確認**:
- 落ち着き → 静止またはスローダリー
- アクション → トラッキングまたはハンドヘルド
- 感情 → スロープッシュまたは静止

2. **気分を明確に指定**:
```python
"calm atmosphere, gentle slow movement"
```

3. **動きをオーバーライド**:
```python
cut.camera_movement = 'static'
```

4. **感情に合わせて動きを合わせる**:
```python
# Tense scene
"uncomfortable static shot, building tension"

# Joyful scene
"dynamic handheld, energetic movement"
```

---

### 問題: "Composition looks amateur"

**症状**: 不均衡、ぎこちないフレーミング

**解決策**:

1. **実証済みの構図を使用**:
```python
"rule of thirds composition"  # Safe default
"centered composition"  # For portraits
"golden ratio"  # For aesthetics
```

2. **プロの用語を追加**:
```python
"proper headroom, lead room for gaze direction"
```

3. **参考資料を研究**:
- プロのストーリーボードを見る
- フレーム構成を分析
- 学んだ原理を適用

4. **構図チェックリストを使用**:
- 焦点は明確か？
- バランスは取れているか？
- ネガティブスペースに目的があるか？
- ラインは水平か？

---

## スタイル一貫性の問題

### 問題: "Colors don't match key visual"

**症状**: 生成された画像が間違ったカラーパレット

**解決策**:

1. **キービジュアル分析を確認**:
```python
python scripts/visual_reference_analyzer.py "keyvisual.jpg"
# Check extracted colors
```

2. **カラーパレットを強制**:
```python
"color palette: #FFE4B5, #87CEEB, #98FB98"
```

3. **色温を追加**:
```python
"warm color temperature, golden tones"
```

4. **色の気分を指定**:
```python
"vibrant saturated colors" or "desaturated muted colors"
```

---

### 問題: "Art style changes between cuts"

**症状**: カット1ではアニメ、カット2ではリアルなど

**解決策**:

1. **すべてのプロンプトにスタイルを追加**:
```python
"anime style, cel-shaded, 2D animation look"
```

2. **キービジュアルを使用**:
```bash
--key-visual "style_reference.jpg"
```

3. **非常に具体的にする**:
```python
"exactly same art style as previous cuts,
matching cel-shading technique, consistent line art"
```

4. **既存のカットを参照**:
```python
"matching Cut 1 visual style, same rendering technique"
```

---

## 音楽生成の問題

### 問題: "Music sections don't match video mood"

**症状**: 悲しいシーンで楽しい音楽

**解決策**:

1. **感情的なアーク を確認**:
```python
music_gen.analyze_emotional_arc(storyboard)
# Check detected moods
```

2. **カットムードを手動で設定**:
```python
cut.mood = 'melancholic'  # Override auto-detected
```

3. **音楽生成を調整**:
```python
# Regenerate with corrected moods
music_plan = music_gen.generate_complete_music_plan(storyboard)
```

4. **Sunoプロンプトを編集**:
- ジャンル、テンポ、ムードを手動で調整
- 生成後に微調整

---

### 問題: "Too many/few music sections"

**症状**: 音楽が頻繁に変わるか、ほとんど変わらない

**解決策**:

1. **セクション制御を手動で実行**:
```python
# Force 3 sections
sections = [
    {'cuts': [1,2,3], 'mood': 'hopeful'},
    {'cuts': [4,5,6], 'mood': 'energetic'},
    {'cuts': [7,8], 'mood': 'triumphant'}
]
```

2. **遷移感度を調整**:
- 低い閾値 = セクション数少ない
- 高い閾値 = セクション数多い

3. **類似のムードをグループ化**:
- 隣接する同じようなムードを手動で組み合わせ
- より長いセクションを作成

---

### 問題: "Music doesn't sync with video cuts"

**症状**: 音楽の遷移がカット変更と一致していない

**解決策**:

1. **タイミングシートを確認**:
```python
timing_sheet = music_gen.generate_timing_sheet(suno_prompts, storyboard)
# Review sync points
```

2. **カット期間を調整**:
- 音楽フレーズの長さに一致させる
- 4、8、12、16秒のパターンを使用

3. **同期ポイントを手動で設定**:
```python
# Specify exact sync points
sync_points = [0, 25, 45, 60]  # seconds
```

4. **DAWで後処理**:
- オーディオエディターで微調整
- 音楽セクションを伸縮

---

## パフォーマンスと品質

### 問題: "Generation is very slow"

**症状**: 完了に長時間かかる

**解決策**:

1. **カット数を削減**:
```bash
--cuts 6  # Instead of default 8-10
```

2. **最初は画像生成をスキップ**:
```bash
--no-images  # Generate storyboard only
```

3. **段階的にバッチ処理**:
```python
# Generate storyboard first
# Then generate images separately
```

4. **より高速なモデルを使用**:
```python
config = {"image_model": "imagen-2.0"}  # If available and faster
```

---

### 問題: "Output quality is inconsistent"

**症状**: いくつかのカットは素晴らしい、他は貧しい

**解決策**:

1. **複数のバリエーションを生成**:
```python
config = {"variations_per_cut": 3}
# Select best of each
```

2. **不良なカットを反復処理**:
```python
# Regenerate specific cuts
regenerate_cut(storyboard, cut_number=3)
```

3. **プロンプトを段階的に調整**:
- 自動生成から開始
- 問題を特定
- 特定の要素を調整
- 再生成

4. **プロンプトテンプレートを使用**:
- 実証済みテンプレートから開始
- ニーズに合わせてカスタマイズ

---

### 問題: "Results not meeting expectations"

**症状**: 全体的な品質が期待より低い

**解決策**:

1. **現実的な期待を設定**:
- AI生成には制限がある
- すべての場合にフォトリアルなわけではない
- 反復は過程の一部

2. **反復と洗練**:
- 最初の生成 = ドラフト
- 2番目の生成 = 洗練
- 3番目の生成 = ポリッシング

3. **結果から学ぶ**:
- 何が機能する？それ以上やる
- 機能しない？アプローチを調整
- 個人的なプロンプトライブラリを構築

4. **参照画像を使用**:
- キービジュアルは結果を劇的に改善
- スタイル例を提供
- 希望される品質レベルを表示

---

## クイック診断チェックリスト

何か問題が発生した場合は、以下を確認してください:

- [ ] APIキーが正しく設定されているか？
- [ ] 依存関係がインストールされているか？
- [ ] プロンプトは明確で具体的か？
- [ ] 矛盾する指示はないか？
- [ ] 期間は適切か？
- [ ] 構図が指定されているか？
- [ ] スタイルは一貫しているか？
- [ ] 気分は明確か？
- [ ] 複雑な要素が多すぎないか？
- [ ] 最初のフレームが意図された動きをサポートしているか？

---

## さらなるヘルプの取得

### ドキュメントを確認
- [Camera Shots Reference](camera_shots.md)
- [Composition Guide](composition_guide.md)
- [Camera Movements](camera_movements.md)
- [ItoV Patterns](itov_patterns.md)

### 体系的にテスト
1. 正確な問題を特定
2. 変数を分離
3. 単一の変更をテスト
4. 結果を比較
5. 反復

### 知識を構築
- 機能するプロンプトを保存
- 機能することを文書化
- 個人的なテンプレートを作成
- 反復から学ぶ

---

このトラブルシューティングガイドは、ほとんどの一般的な問題をカバーしています。リストされていない特定の問題については、問題を体系的に分解し、個々の要素をテストしてください。
