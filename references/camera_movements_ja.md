# カメラムーブメント リファレンスガイド

自動選択ルールとItoVプロンプト最適化を含むカメラムーブメントの完全ガイド。

## シーンタイプ別自動選択

```python
movement_selection = {
    'opening': 'slow_zoom_in' or 'establishing_pan',
    'dialogue': 'static' or 'gentle_push',
    'action': 'tracking' or 'handheld',
    'revelation': 'dolly_in' or 'crane_up',
    'ending': 'slow_pull_back' or 'fade'
}
```

---

## ムーブメントタイプ

### 1. Static (固定)

**自動選択対象**: 会話、観察、フォーマルなシーン

**説明**:
カメラは完全に静止したまま。動きなし。

**視覚効果**:
- 安定した接地感
- コンテンツへの焦点を可能にする
- プロフェッショナルで統制された印象

**ItoVプロンプト**:

**基本**:
```
static camera, no movement, stable frame, locked-off shot
```

**わずかな生命感付き**:
```
static camera with subtle breathing movement, minimal natural drift
```

**非常に安定**:
```
tripod-mounted static camera, perfectly still, no shake
```

**調整例**:
- 「生命感が欲しい」→ `subtle breathing movement` を追加
- 「硬い」→ `barely perceptible drift` を追加
- 「ドキュメンタリータッチ」→ `handheld static` を使用（静止しているがヒューマン感）

**最適用途**:
- インタビュー/会話シーン
- 観察シーン
- フォーマルなプレゼンテーション
- 製品ショーケース
- コンテキストの確立

**尺**: 任意の長さ（最も汎用的）

---

### 2. Pan (パン)

**自動選択対象**: 広大な空間の開示、アクションの追跡、スキャン

**説明**:
カメラが固定軸上で水平に回転する。

**視覚効果**:
- 空間を徐々に開示する
- 移動する被写体をフォロー
- 滑らかなフローを作成

**ItoVプロンプト**:

**基本的なパンライト**:
```
camera pans right slowly, smooth horizontal movement, steady rotation
```

**基本的なパンレフト**:
```
camera pans left, sweeping across scene, horizontal tracking
```

**高速パン**:
```
quick pan right, fast horizontal sweep, dynamic movement
```

**スロー開示パン**:
```
slow deliberate pan left, revealing environment gradually, 10 seconds
```

**追跡パン**:
```
pan right following subject movement, smooth tracking, keeping subject centered
```

**調整例**:
- スピード: `slow pan` vs `fast pan` vs `medium-paced pan`
- 方向: `pan left to right` or `pan right to left`
- 目的: `revealing pan` vs `following pan` vs `searching pan`

**最適用途**:
- 広大な風景
- 空間の開示
- 歩いているキャラクターのフォロー
- 空間同士の関係性を示す
- グループシーン

**尺**: 6～12秒（広いパンはより遅く）

---

### 3. Tilt (ティルト)

**自動選択対象**: 垂直方向の開示、上下を見る

**説明**:
カメラが固定軸上で垂直に回転する。

**視覚効果**:
- 高さや深さを表示
- 垂直要素を開示
- 期待感を作成

**ItoVプロンプト**:

**ティルトアップ**:
```
camera tilts up slowly, revealing height, vertical movement from ground to sky
```

**ティルトダウン**:
```
camera tilts down, descending gaze, from sky to ground reveal
```

**高速ティルト**:
```
quick tilt up, rapid vertical movement, dramatic reveal
```

**キャラクター開示**:
```
slow tilt up from feet to face, character introduction, vertical scan
```

**調整例**:
- 「スケールを見せる」→ `tilt up revealing full height of building`
- 「ドラマチックな開示」→ `quick tilt up to face`
- 「下降」→ `tilt down following fall`

**最適用途**:
- 高い建物や木
- キャラクター紹介（下から上へ）
- 高さからの見下ろし
- 垂直アクション
- スケール表現

**尺**: 4～8秒

---

### 4. Zoom (ズーム)

**自動選択対象**: フォーカス強調、注意誘導、サプライズ

**説明**:
レンズが焦点距離を変更し、被写体に近づいたり、離れたりしているように見える。

**視覚効果**:
- 注意を引く
- 緊張感や開放感を作成
- 人為的だが影響力がある

**ItoVプロンプト**:

**ズームイン（スロー）**:
```
slow zoom in, gradually approaching subject, increasing tension, 8 seconds
```

**ズームイン（高速）**:
```
quick zoom in, rapid approach, dramatic emphasis
```

**ズームアウト**:
```
zoom out slowly, revealing wider context, pulling back perspective
```

**クラッシュズーム**:
```
fast dramatic zoom in, intense focus, sudden attention
```

**微妙なズーム**:
```
gentle imperceptible zoom in, slowly intensifying, very gradual
```

**調整例**:
- インテンシティ: `subtle zoom` vs `dramatic zoom` vs `crash zoom`
- スピード: `slow gradual zoom over 10 seconds` vs `quick 2-second zoom`
- 方向: `zoom in` vs `zoom out`

**最適用途**:
- リアクションの強調
- 緊張の構築
- 注意のフォーカス
- サプライズモーメント
- 時間的なトランジション

**尺**: 3～10秒（ドラマチックなら高速、微妙なら遅い）

---

### 5. Dolly / Track (ドリー/トラック)

**自動選択対象**: 没入感、アプローチ、アクション追跡

**説明**:
カメラが被写体に向かって、遠ざかって、または並行して物理的に移動する。

**視覚効果**:
- 自然な動きの感覚
- 視点と視差を変更
- ズームより有機的

**ItoVプロンプト**:

**ドリーイン**:
```
dolly forward toward subject, camera physically moving closer, smooth approach
```

**ドリーアウト**:
```
dolly back away from subject, pulling back, revealing more space
```

**トラッキングショット（フォロー）**:
```
tracking shot following character, camera moving parallel to subject, smooth glide
```

**ドリー＋ズーム（バーティゴエフェクト）**:
```
dolly in while zooming out, vertigo effect, disorienting perspective shift
```

**スロードリー**:
```
slow gentle dolly forward, subtle approach, building intimacy over 12 seconds
```

**調整例**:
- 「よりインティメート」→ `dolly in slowly toward face`
- 「ワールドを開示」→ `dolly back revealing environment`
- 「アクションをフォロー」→ `tracking dolly following movement`
- 「ヒッチコック効果」→ `dolly zoom (vertigo effect)`

**最適用途**:
- 被写体へのアプローチ
- 動きの追跡
- インティマシーの作成
- 環境の開示
- スムーズなプロフェッショナル動き

**尺**: 6～15秒（微妙な動きはより長くできる）

---

### 6. Truck (トラック)

**自動選択対象**: 横方向の動き、シーン通過

**説明**:
カメラが被写体またはシーンに平行に横方向（サイド）に移動する。

**視覚効果**:
- スムーズな横方向フロー
- 深さのレイヤーを表示
- プロフェッショナルでシネマティック

**ItoVプロンプト**:

**トラックライト**:
```
camera trucks right, smooth lateral movement, passing scene from left to right
```

**トラックレフト**:
```
camera trucks left, sideways motion, gliding past subjects
```

**被写体とトラッキング**:
```
truck right keeping subject centered, lateral tracking, smooth parallel movement
```

**調整例**:
- 「歩行をフォロー」→ `truck right with character walking`
- 「シーンを通過」→ `truck left passing stationary subjects`
- 「深さを見せる」→ `truck revealing depth layers`

**最適用途**:
- 横からのキャラクター歩行フォロー
- 複数被写体の通過
- 深さ視差の表示
- プロフェッショナルでシネマティックなショット

**尺**: 6～12秒

---

### 7. Pedestal (ペデスタル)

**自動選択対象**: カメラの垂直移動

**説明**:
カメラがレベルを保ったまま垂直上下に移動する。

**視覚効果**:
- フレーミングを垂直に調整
- 垂直アクションをフォロー
- 水平線を保持

**ItoVプロンプト**:

**ペデスタルアップ**:
```
camera pedestal up, rising vertically while keeping level, smooth ascent
```

**ペデスタルダウン**:
```
camera pedestal down, lowering vertically, descending while level
```

**調整例**:
- 「被写体と共に上昇」→ `pedestal up following character standing`
- 「低い視点」→ `pedestal down for ground perspective`

**最適用途**:
- 立ったり座ったりするアクションのフォロー
- 垂直フレーミング調整
- 垂直移動時に水平を保つ

**尺**: 3～6秒

---

### 8. Crane / Jib (クレーン)

**自動選択対象**: グランドリベール、空中視点、ドラマティックムーブ

**説明**:
カメラがブームアームで移動し、垂直および水平のスイープ動きが可能。

**視覚効果**:
- エピックでシネマティック
- 神様の視点での変化
- グランドスケール感

**ItoVプロンプト**:

**クレーンアップ**:
```
crane up shot, camera rising on boom, sweeping upward reveal, majestic movement
```

**クレーンダウン**:
```
crane down from height, descending into scene, dramatic entry
```

**クレーンアーク**:
```
sweeping crane shot arcing around subject, circular reveal, epic movement
```

**調整例**:
- 「グランドなオープニング」→ `crane up from ground level to aerial view`
- 「ドラマティックな進入」→ `crane down from above into close-up`
- 「スケール開示」→ `crane back and up, revealing vast environment`

**最適用途**:
- オープニング/クロージングショット
- ドラマティックな開示
- スケール表現
- エピックモーメント
- トランジショナルショット

**尺**: 10～20秒（長い動きはインパクトがある）

---

### 9. Handheld (ハンドヘルド)

**自動選択対象**: ドキュメンタリータッチ、緊張、リアリズム、アクション

**説明**:
オペレーターが持つカメラ、自然なシェイクと動き。

**視覚効果**:
- リアルで没入的
- エネルギーと緊張を追加
- ドキュメンタリー真正性

**ItoVプロンプト**:

**基本的なハンドヘルド**:
```
handheld camera, natural shake, documentary style, organic movement
```

**アクティブなハンドヘルド**:
```
dynamic handheld, following action, energetic shake, tense atmosphere
```

**微妙なハンドヘルド**:
```
gentle handheld, slight natural movement, barely perceptible shake
```

**カオティックなハンドヘルド**:
```
intense handheld, rapid movements, shaky, high tension, action scene
```

**調整例**:
- 「よりスタビル」→ `steadicam handheld, smooth but organic`
- 「よりインテンス」→ `chaotic handheld, rapid movements`
- 「ドキュメンタリー」→ `observational handheld, natural operator movement`

**最適用途**:
- アクションシーケンス
- ドキュメンタリースタイル
- POVショット
- 緊張/緊迫感
- リアルなモーメント

**尺**: 任意の長さだが、強度は視聴者の快適さに影響

---

### 10. Steadicam / Gimbal (ステディカム)

**自動選択対象**: スムーズな複雑な動き

**説明**:
安定化されたカメラで空間をスムーズに移動可能。

**視覚効果**:
- 不可能なほどスムーズ
- 浮遊感覚
- プロフェッショナルで洗練

**ItoVプロンプト**:

**フローティング動き**:
```
steadicam shot, smooth gliding movement, floating through space, seamless flow
```

**スムーズにフォロー**:
```
gimbal-stabilized tracking, smoothly following subject, effortless movement
```

**複雑な動き**:
```
steadicam moving through environment, weaving smoothly, continuous single shot
```

**調整例**:
- 「ドアを通して」→ `steadicam gliding through doors and corridors`
- 「被写体の周囲」→ `circular steadicam move around subject`
- 「不可能なほどスムーズ」→ `gimbal-stabilized perfect smoothness`

**最適用途**:
- ロングテイク
- 空間を通してのフォロー
- 複雑なコレオグラフィー
- プロフェッショナルで洗練された感覚
- イマーシブなPOV

**尺**: 10～60秒（非常に長くできる）

---

## ムーブメントの組み合わせ

### 一般的な組み合わせ

**ドリー＋パン**:
```
dolly forward while panning left, complex approach, revealing subject
```

**クレーン＋パン**:
```
crane up while panning across scene, sweeping majestic reveal
```

**トラック＋ティルト**:
```
truck right while tilting up, dynamic compound movement
```

**ズーム＋トラック（バーティゴエフェクト）**:
```
dolly in while zooming out, vertigo effect, psychological disorientation
```

---

## 感情別ムーブメント

| 感情 | プライマリームーブメント | セカンダリー | 避けるべき |
|---------|-----------------|-----------|-------|
| **落ち着き** | Static, Slow dolly | Gentle pan | Handheld, Fast |
| **緊張** | Handheld, Slow zoom in | Static (uncomfortable) | Smooth crane |
| **興奮** | Tracking, Handheld | Fast pan | Static |
| **インティメート** | Slow dolly in, Static | Subtle zoom | Crane, Fast |
| **エピック** | Crane, Sweeping | Slow dolly | Static, Handheld |
| **神秘的** | Slow dolly, Creeping | Gentle pan | Fast, Jerky |
| **カオティック** | Intense handheld, Fast | Quick pan/tilt | Static, Smooth |

---

## ムーブメントスピードガイド

| スピード | 尺（フルムーブ） | ユースケース |
|-------|-------------------------|----------|
| **非常に遅い** | 15～20秒 | 微妙、知覚不可能 |
| **遅い** | 10～15秒 | 意図的、統制された |
| **中程度** | 6～10秒 | 標準的、自然 |
| **速い** | 3～5秒 | ドラマティック、注目を集める |
| **非常に速い** | 1～2秒 | ショック、サプライズ、ホイップ |

---

## トラブルシューティング

### 「動きが速すぎる」
**ソリューション**:
- 尺を増やす: `over 12 seconds`
- `slow`, `gentle`, `gradual` を追加
- 動きの量を減らす

### 「動きが遅すぎる」
**ソリューション**:
- 尺を短くする
- `dynamic`, `energetic` を追加
- 動きの範囲を増やす

### 「動きが機械的に感じる」
**ソリューション**:
- `slight ease in/out` を追加
- `natural acceleration` を使用
- 有機的な感覚のためハンドヘルドやギンバルを試す

### 「動きが被写体から気を散らす」
**ソリューション**:
- スピードを落とす
- Static または微妙な動きを使用
- 動きをアクションと一致させる

### 「エネルギーが必要」
**ソリューション**:
- ハンドヘルドまたはトラッキングを使用
- スピードを上げる
- 動的な複合ムーブメントを追加

---

## プロのヒント

### 1. ストーリービートにムーブメントを合わせる
- **始まり**: 遅く、探索的（slow dolly, pan）
- **構築**: 増加するペース（medium tracking）
- **クライマックス**: 速く、強烈（handheld, fast movements）
- **解決**: 落ち着く（slow pull back, static）

### 2. カメラムーブメントを動機付ける
常に理由がある：
- **アクション追跡**: キャラクターと一緒にトラック
- **情報開示**: 新しい要素にパン
- **キャラクターPOV**: 彼らがどのように見るかを真似る
- **感情的シフト**: 認識時にズーム

### 3. イージーインとイージーアウト
ムーブメントは自然に加速して減速すべき：
```
slow dolly in, ease in at start, ease out at end, natural acceleration
```

### 4. ムーブメントを控えめに使用
すべてのショットが動く必要はない：
- Static ショットは力を持つ
- ムーブメントは目的に応じるべき
- 過度なムーブメント = めまいを感じる視聴者

### 5. 音楽リズムとマッチする
カメラムーブをミュージックビートに同期させる：
- ビートでムーブメント開始
- アクセントでキーポイントを打つ
- ペースをテンポに合わせる

---

## ItoVプロンプト式

最適なイメージ・トゥ・ビデオ結果のために、この構造を使用：

```
[Movement Type] + [Speed/Quality] + [Subject Action] + [Duration] + [Mood] + [Consistency Note]
```

**例**:
```
Slow dolly forward, smooth approach, character turning to camera,
8 seconds, building tension, maintain composition balance throughout
```

---

## ムーブメントチェックリスト

カメラムーブメントを最終化する前に：

- [ ] ムーブメントはストーリーに役立つか？
- [ ] スピードはムードに適切か？
- [ ] 視るのが快適か？
- [ ] 情報を適切に開示するか？
- [ ] 尺はムーブメント範囲に適切か？
- [ ] 意図した音楽/ペーシングと機能するか？
- [ ] ビジュアルスタイルと一致するか（ドキュメンタリー vs シネマティック）？
- [ ] 最初のフレームはムーブメントに対してよく構成されているか？

---

## 一般的な間違い

### 1. ムーブメントが多すぎる
**問題**: すべてのショットが動き、視聴者がめまいを感じる
**修正**: Static ショットで視聴者をグラウンド

### 2. 目的のない動き
**問題**: カメラが目的なく動く
**修正**: 常にストーリーの理由でムーブメントを動機付ける

### 3. 間違ったスピード
**問題**: ムーブメントがコンテキストに対して速すぎたり遅すぎたり
**修正**: スピードを感情とペーシングと一致させる

### 4. アクションと対抗する動き
**問題**: カメラが被写体と反対に動く
**修正**: 被写体の動きと共に移動またはコンプリメント

### 5. 最初のフレームを無視
**問題**: ムーブメントが最初のコンポジションと機能しない
**修正**: ムーブメントがどこに行くか知りながら最初のフレームを設計

---

## クイックリファレンステーブル

| ムーブメント | 難易度 | インパクト | 最適用途 | 避けるべき用途 |
|----------|-----------|--------|----------|-----------|
| **Static** | 簡単 | 低～中 | 会話、フォーマル | ダイナミックアクション |
| **Pan** | 簡単 | 中程度 | 開示、フォロー | クローズ感情 |
| **Tilt** | 簡単 | 中程度 | 垂直開示 | 水平 |
| **Zoom** | 簡単 | 高 | 強調、緊張 | 自然なリアリズム |
| **Dolly** | 中程度 | 高 | アプローチ、没入 | 速いアクション |
| **Track** | 中程度 | 高 | フォロー | Static 被写体 |
| **Crane** | 難しい | 非常に高 | エピック、グランド | インティメート |
| **Handheld** | 簡単 | 中程度 | リアリズム、緊張 | フォーマル、落ち着き |
| **Steadicam** | 難しい | 高 | 複雑スムーズ | シンプルショット |

---

## ムーブメントインテンシティラダー

最も落ち着きから最もエネルギッシュまで：

1. **Static** - ムーブメントなし
2. **微妙なドリー** - ほぼ知覚不可能なアプローチ
3. **スロー パン** - やさしい開示
4. **中程度のドリー** - 明確だがスムーズ
5. **トラッキング** - アクティブなフォロー
6. **高速 パン/ティルト** - クイック開示
7. **ダイナミッククレーン** - スイープムーブメント
8. **ハンドヘルド** - エネルギッシュなシェイク
9. **インテンスなハンドヘルド** - カオティック、緊急

シーンエネルギーニーズに基づいてラダーのポジションを選択。

---

このガイドはダイナミックなストーリーテリングのためにAI選択カメラムーブメントを理解および調整するのに役立ちます。
