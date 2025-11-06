# 構図ガイド

自動選択マトリックスと調整テクニックを含む、ビジュアル構図の完全ガイド。

## 自動選択マトリックス

AIはシーンタイプに基づいて構図を自動的に選択します：

```python
composition_matrix = {
    'opening': 'rule_of_thirds',      # Balanced introduction
    'character': 'centered',           # Character focus
    'dialogue': 'over_shoulder',       # Natural conversation
    'action': 'diagonal',              # Dynamic movement
    'emotion': 'centered_tight',       # Emotional focus
    'landscape': 'golden_ratio'        # Aesthetic beauty
}
```

---

## 構図タイプ

### 1. 三分割法（Rule of Thirds）

**自動適用対象**：一般的なシーン、風景、日常的な瞬間

**説明**：
フレームを3×3のグリッドに分割し、重要な要素を交差点または線に沿って配置します。

**ビジュアル効果**：
- バランスの取れた自然な見え方
- プロフェッショナルな印象
- 無理のない視覚的な快適さ

**プロンプト修飾子**：

**基本形**：
```
rule of thirds composition, balanced framing
```

**左配置**：
```
subject on left third, looking right, negative space on right
```

**右配置**：
```
subject on right third, looking left, balanced composition
```

**上部配置**：
```
subject on upper third, sky/background in lower two-thirds
```

**下部配置**：
```
ground/foreground in lower third, sky in upper two-thirds
```

**調整のコツ**：
- 「硬すぎる場合」→ `slightly off-center for dynamic balance` を追加
- 「もっと緊張感が必要」→ 交差点に移動
- 「空きスペースが多すぎる場合」→ `tighter rule of thirds` を使用

**最適な用途**：
- 地平線のある風景
- 背景に興味のあるキャラクター
- 確立ショット
- 静的なシーン

---

### 2. 黄金比（Golden Ratio）

**自動適用対象**：芸術的なシーン、美しさの強調、美的フォーカス

**説明**：
フィボナッチ数列（1:1.618）に基づいています。三分割法より洗練されています。

**ビジュアル効果**：
- 数学的に美しい
- 洗練されてエレガント
- 目の流れが自然

**プロンプト修飾子**：

**基本形**：
```
golden ratio composition, divine proportion layout
```

**スパイラル付き**：
```
fibonacci spiral composition, natural flow leading to focal point
```

**バランス型**：
```
golden ratio framing, harmonious proportions
```

**調整のコツ**：
- 「微妙すぎる場合」→ より明白な配置を使用
- 「インパクトが欲しい」→ 強い色コントラストと組み合わせる
- 「数学的精密性」→ `precise golden ratio positioning` を追加

**最適な用途**：
- ポートレート写真
- 建築シーン
- 自然写真
- 芸術的構図

---

### 3. 中心構図（Centered Composition）

**自動適用対象**：キャラクター紹介、対称性、フォーマルなシーン

**説明**：
メインの被写体をフレームの中央に配置します。

**ビジュアル効果**：
- パワフルで直接的
- フォーマルで安定している
- 即座にフォーカス

**プロンプト修飾子**：

**完全中央**：
```
centered composition, symmetrical, subject dead center
```

**ほぼ中央**：
```
near-centered composition, subtle off-center for tension
```

**対称性付き**：
```
perfectly centered, symmetrical composition, mirrored balance
```

**タイト中央**：
```
centered tight framing, minimal negative space, focused
```

**調整のコツ**：
- 「静的すぎる場合」→ `slightly off-center for subtle dynamism` を追加
- 「エネルギーが必要」→ フレーム内に対角線要素を追加
- 「フォーマルすぎる」→ わずかにオフセンターにシフト

**最適な用途**：
- ポートレート
- 製品写真
- フォーマルなプレゼンテーション
- 対称的な建築
- キャラクター紹介

---

### 4. 対角線構図（Diagonal Composition）

**自動適用対象**：アクション、ダイナミックなシーン、動き

**説明**：
主要な要素が対角線（通常は角から角）に沿って配置されます。

**ビジュアル効果**：
- ダイナミックでエネルギッシュ
- 動きの感覚
- ビジュアルな緊張感

**プロンプト修飾子**：

**強い対角線**：
```
diagonal composition, dynamic angles, 45-degree orientation
```

**微妙な対角線**：
```
subtle diagonal lines, gentle dynamic movement
```

**複数の対角線**：
```
intersecting diagonal lines, complex dynamic composition
```

**主導対角線**：
```
diagonal leading line from corner, drawing eye through frame
```

**調整のコツ**：
- 「混沌としている場合」→ `gentle diagonal` または単一の対角線を使用
- 「もっとエネルギーが必要」→ `strong diagonal lines, sharp angles` を使用
- 「傾いて見える場合」→ 地平線が水平であることを確認し、対角線はコンテンツ

**最適な用途**：
- アクションシーケンス
- スポーツ
- ダイナミックな動き
- 緊張感の作成
- 単調さを破る

---

### 5. 誘導線構図（Leading Lines）

**自動適用対象**：視聴者の目を導く、奥行き、遠近法

**説明**：
自然またはマンメイドラインを使用して、視線を被写体に導きます。

**ビジュアル効果**：
- 奥行きを作成
- 注目を導く
- 強い遠近感

**プロンプト修飾子**：

**道/パス**：
```
leading lines composition, road leading to subject, perspective depth
```

**建築**：
```
converging lines, architectural perspective leading to focal point
```

**自然な線**：
```
natural leading lines, organic flow toward subject
```

**複数の線**：
```
multiple leading lines converging at subject
```

**調整のコツ**：
- 「線が目立ちすぎる場合」→ `subtle leading lines` を使用
- 「より強い導きが必要」→ `converging perspective lines` を使用
- 「線が気を散らす」→ 被写界深度で柔らかく

**最適な用途**：
- 道とパス
- 廊下とコリドー
- 線路
- 川と海岸線
- 建築

---

### 6. 額縁構図（Frame Within Frame）

**自動適用対象**：フォーカス強調、奥行き作成、分離

**説明**：
シーン内の要素を使用して、被写体の周りに自然なフレームを作成します。

**ビジュアル効果**：
- 被写体に目を引く
- 奥行きレイヤーを作成
- コンテキストと分離を同時に追加

**プロンプト修飾子**：

**窓フレーム**：
```
frame within frame, subject framed by window, layered composition
```

**ドアフレーム**：
```
doorway framing subject, natural frame, depth layers
```

**自然なフレーム**：
```
tree branches framing subject, organic frame within frame
```

**建築フレーム**：
```
architectural elements framing subject, geometric frame
```

**調整のコツ**：
- 「フレームが暗い場合」→ `bright frame, well-lit edges` を追加
- 「被写体が失われた場合」→ `clear frame, strong subject contrast` を使用
- 「忙しすぎる場合」→ `simple frame, clean edges` を使用

**最適な用途**：
- 窓とドア
- アーチウェイ
- 枝
- ミラー
- フォーカスを作成

---

### 7. ネガティブスペース（Negative Space）

**自動適用対象**：ミニマリズム、分離、強調

**説明**：
被写体の周りの空き領域を使用して強調を作成します。

**ビジュアル効果**：
- クリーンでミニマル
- 被写体が目立つ
- ムードを作成（孤独、平和など）

**プロンプト修飾子**：

**ミニマル**：
```
negative space composition, minimalist, subject with empty space
```

**大量のスペース**：
```
vast negative space, small subject, emphasis through isolation
```

**方向的スペース**：
```
subject on left, negative space on right, directional gaze space
```

**調整のコツ**：
- 「空きすぎている場合」→ `subtle background interest` を追加
- 「被写体が小さすぎる」→ ネガティブスペースの量を削減
- 「ムードが必要」→ スペースの特性を指定：`peaceful white space`

**最適な用途**：
- ミニマリストスタイル
- 製品写真
- 感情的な分離
- クリーンな美学
- モダンデザイン

---

### 8. シンメトリー（Symmetry）

**自動適用対象**：フォーマルなシーン、バランス、建築対象

**説明**：
垂直軸または水平軸全体にわたる完全または近完全なミラーバランス。

**ビジュアル効果**：
- フォーマルで安定している
- 視覚的に満足度が高い
- 強力で自信がある

**プロンプト修飾子**：

**完全な対称性**：
```
perfect symmetry, mirrored composition, bilateral balance
```

**垂直対称性**：
```
vertical symmetry, left-right mirror balance
```

**水平対称性**：
```
horizontal symmetry, top-bottom balance
```

**放射状対称性**：
```
radial symmetry, centered circular balance
```

**調整のコツ**：
- 「硬すぎる場合」→ `near-symmetry with subtle variation` を使用
- 「興味が必要」→ `asymmetric element for tension` を追加
- 「より大きなインパクト」→ `perfect bilateral symmetry` を使用

**最適な用途**：
- 建築
- フォーマルなポートレート
- 自然パターン
- リフレクション
- 宗教的または儀式的シーン

---

## 構図の組み合わせ

### 一般的な組み合わせ

**三分割法＋誘導線**：
```
subject at rule of thirds intersection, leading lines guiding to subject
```

**黄金比＋ネガティブスペース**：
```
golden ratio placement with generous negative space, minimalist elegance
```

**中心構図＋シンメトリー**：
```
perfectly centered symmetrical composition, formal balance
```

**対角線＋誘導線**：
```
diagonal leading lines creating dynamic flow, energetic movement
```

---

## ムード別構図

| ムード | プライマリ構図 | セカンダリ | 避けるべき |
|--------|-----------------|-----------|----------|
| **平穏** | 対称性、三分割法 | ネガティブスペース | 対角線 |
| **エネルギッシュ** | 対角線、ダイナミックアングル | 三分割法 | 中心構図 |
| **フォーマル** | 中心構図、対称性 | 三分割法 | 対角線 |
| **親密** | タイト中心、クローズフレーミング | 黄金比 | ネガティブスペース |
| **孤独** | ネガティブスペース、小さい中央配置 | 三分割法 | 対称性 |
| **劇的** | 対角線、ロアングル | 額縁構図 | 対称性 |
| **平穏** | 黄金比、対称性 | 水平線 | 対角線 |

---

## ジャンル別構図

### 教育動画
**プライマリ**：三分割法（明確でバランスの取れた）
**セカンダリ**：中心構図（直接的なフォーカス）
**テクニック**：シンプルで明確に保つ

### マーケティング/コマーシャル
**プライマリ**：黄金比（美的アピール）
**セカンダリ**：中心構図（製品フォーカス）、ネガティブスペース（クリーン）
**テクニック**：目を引いてクリーン

### ナラティブ/ドラマ
**プライマリ**：すべてのタイプ（ストーリーに応じて変動）
**セカンダリ**：感情に合わせる
**テクニック**：ナラティブに奉仕する

### ドキュメンタリー
**プライマリ**：三分割法（自然）
**セカンダリ**：実際の状況で利用可能な場合
**テクニック**：現実に適応

---

## クイック調整ガイド

### 問題：「構図がアンバランスに感じられる」
**解決策**：
- 視覚的な重みの分布をチェック（視覚的重みがバランスする必要がある）
- 空いている側に要素を追加
- ネガティブスペースを意図的に使用
- 三分割法を試す

### 問題：「構図が退屈に感じられる」
**解決策**：
- 対角線要素を追加
- オフセンター配置を試す
- 誘導線を使用
- 前景の興味を追加

### 問題：「構図が混沌としているように感じられる」
**解決策**：
- 要素をシンプルにする
- 中心構図または対称構図を使用
- ネガティブスペースを増やす
- 額縁構図を使用して分離

### 問題：「被写体が失われる」
**解決策**：
- 額縁構図を使用
- 背景とのコントラストを増やす
- 背景をシンプルにする
- 被写体を中央に配置
- ネガティブスペースを使用

---

## 技術的考慮事項

### アスペクト比

**16:9（標準）**：
- すべての構図がよく機能
- 水平強調
- 風景とグループに適している

**9:16（垂直/電話）**：
- 垂直構図が優れている
- 中心構図がよく機能
- 広い対角線構図を避ける

**1:1（正方形）**：
- 対称性に最適
- 中心構図が輝く
- 黄金比スパイラルが美しく機能

**2.35:1（シネマティック）**：
- 水平要素を強調
- 誘導線が優れて機能
- より広い構図が必要

---

## プロのヒント

### 1. 構図をレイヤー化する
前景、中景、背景を構図ルールと組み合わせる：
```
rule of thirds with layered depth, foreground framing, subject in midground
```

### 2. 動きの方向を考慮する
被写体が動く場合、動きの方向に空きスペースを残す：
```
subject on left third, moving right, space ahead
```

### 3. アイラインの方向
ポートレートでは、被写体が見ている方向に空きスペースを残す：
```
subject on right third, looking left, gaze space
```

### 4. 奇数を使用する
3つまたは5つのグループは2つまたは4つより視覚的に興味深い：
```
three subjects in rule of thirds composition, triangular arrangement
```

### 5. ルールを意図的に破る
- キャラクターを中央に配置して、周囲のアクションにもかかわらず分離を示す
- 穏やかなシーンで対角線を使用して、来たる葛藤を予示
- アクションシーンで対称性を使用して「嵐の前の静けさ」効果を作成

---

## 構図チェックリスト

ショットを最終化する前に、確認してください：

- [ ] 構図がストーリー/感情をサポートしているか？
- [ ] フォーカルポイントが明確か？
- [ ] ビジュアルバランスがあるか（意図的なアンバランスは目的があれば問題ない）？
- [ ] ネガティブスペースが目的を果たしているか？
- [ ] 線（地平線、建築）が水平か、または意図的に傾いているか？
- [ ] 構図が視聴者の目をあなたが望む場所に導くか？
- [ ] 適切な奥行きがあるか（前景/背景の興味）？
- [ ] 意図された視聴サイズで機能するか？

---

## よくある間違い

### 1. 常に同じ構図を使用する
**問題**：単調な視聴体験
**対策**：ストーリーボード全体を通して構図を変える

### 2. 構図と戦う
**問題**：被写体配置が自然な線と競合
**対策**：環境要素に対して、環境要素に逆らわずに機能

### 3. 三分割グリッドを無視する
**問題**：重要な要素がデッドスペースに落ちる
**対策**：主要な要素をグリッド交差点に配置

### 4. すべてを中央に配置する
**問題**：静的でつまらない
**対策**：中心構図は適切な場合のみ使用（フォーマル、対称性）

### 5. 複雑すぎる
**問題**：複数の競合する構図テクニック
**対策**：1つのプライマリテクニックを選択し、他は微妙なサポートとして使用

---

## クイックリファレンステーブル

| 構図 | 強み | 用途 | 避けるべき用途 |
|------|------|------|-------------|
| **三分割法** | 多機能、自然 | ほとんどのシーン | フォーマルなモーメント |
| **黄金比** | 美的、エレガント | 美、アート | 高速アクション |
| **中心構図** | 強力、直接的 | ポートレート、フォーマル | ダイナミックアクション |
| **対角線** | ダイナミック、エネルギー | アクション、緊張 | 穏やか、平穏 |
| **誘導線** | 奥行き、導き | 遠近法 | クローズアップ |
| **額縁構図** | フォーカス、奥行き | 分離、強調 | 広い確立 |
| **ネガティブスペース** | ミニマル、クリーン | 分離、モダン | 忙しいアクション |
| **対称性** | フォーマル、バランス | 建築 | 自然、カジュアル |

---

このガイドは、AIが選択した構図を理解し、パワフルなビジュアルストーリーテリングのために調整するのに役立ちます。
