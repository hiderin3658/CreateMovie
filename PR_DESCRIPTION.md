# プルリクエスト: Modular Video Generation System Refactor

## 概要

動画生成システムをモジュラーアーキテクチャにリファクタリングし、プロジェクトごとに機能を追加できるように改善しました。
設計書 `docs/design/modular-video-system-design.md` に基づいて実装しています。

## 主な変更点

### 🏗️ コアシステム（core/）

#### **base/** - 基底クラスとプラグインシステム
- `BaseVideoGenerator`: すべての動画生成器の基底クラス
- `BasePlugin`: 機能拡張のためのプラグインシステム
- `GeneratorConfig`: 設定管理用データクラス
- フックシステムによるカスタマイズポイント提供

#### **video/** - 動画生成機能
- `CoreStoryboardGenerator`: モジュール化されたストーリーボード生成
- `ImageGenerator`: Gemini APIを使用した画像生成

#### **analysis/** - ビジュアル解析機能
- `VisualAnalyzer`: キービジュアルからスタイル要素を抽出
- `VisualAnalysis`: 解析結果のデータクラス
- オプショナル依存関係の優雅なフォールバック

#### **music/** - 音楽生成機能
- `MusicGenerator`: ストーリーボード用の音楽プロンプト生成
- `MoodType`: 感情的なムードカテゴリのEnum

### 🛠️ プロジェクト管理（tools/）
- `ProjectManager`: 動画生成プロジェクトの管理
  - プロジェクト構造の作成
  - 素材のインポートと整理
  - 設定管理

### ✨ 新機能

1. **フックシステム**: 前処理/後処理のカスタマイズポイント
2. **プラグインアーキテクチャ**: 機能拡張のためのプラグインシステム
3. **プロジェクトベース管理**: プロジェクトごとの設定と素材管理
4. **モジュール化**: 再利用可能なコンポーネント
5. **オプショナル依存関係**: 依存関係がない場合の優雅なフォールバック

### 📝 互換性

- 新しいモジュラースクリプト: `scripts/generate_storyboard_v2.py`
- 既存スクリプトは後方互換性のために保持
- コア依存関係は `requirements-core.txt` に分離

### 📚 ドキュメント

- `MODULAR_SYSTEM.md`: 使用ガイドとアーキテクチャ概要
- システム拡張のための設計パターン
- カスタムジェネレーターの実装例

## メリット

- ✅ 異なる動画タイプ（教育、観光など）への拡張が容易
- ✅ コアコードを変更せずにプロジェクト固有のカスタマイズが可能
- ✅ より良いコード構成と保守性
- ✅ 異なるプロジェクト間で再利用可能なコンポーネント
- ✅ 新機能追加のためのプラグインシステム

## テスト結果

- ✅ すべてのモジュールが構文チェックをパス
- ✅ インポートテスト成功
- ✅ CLIヘルプメニューが正常に動作
- ✅ オプショナル依存関係の優雅な処理

## 使用例

### 基本的な使用

```bash
python scripts/generate_storyboard_v2.py "魔法少女のオープニング" \
  --duration 60 \
  --cuts 8 \
  --output output/magical_girl \
  --title "魔法少女OP" \
  --style anime
```

### カスタムジェネレーター

```python
from core.video import CoreStoryboardGenerator

class EducationVideoGenerator(CoreStoryboardGenerator):
    def __init__(self, config):
        super().__init__(config)
        self.register_hook('post_generation', self.add_summary_slide)

    def add_summary_slide(self, storyboard):
        # まとめスライドを追加
        return storyboard
```

## ファイル統計

- 新規ファイル: 16個
- 追加行数: 1,534行
- モジュール: 4個（base, video, analysis, music）

## 今後の拡張

- テーマ別拡張（education, tourism, marketing）
- より多くのプラグイン
- プロジェクトテンプレート
- 素材管理機能
- 複数プラットフォーム対応

## レビューポイント

1. ✅ アーキテクチャ設計の妥当性
2. ✅ モジュール間の依存関係
3. ✅ 拡張性と保守性
4. ✅ ドキュメントの充実度
5. ✅ 既存機能との互換性

---

## GitHub上でプルリクエストを作成する方法

以下のリンクからプルリクエストを作成できます：

https://github.com/hiderin3658/CreateMovie/pull/new/claude/modular-video-system-refactor-011CUscFwzJxXqi1vZuFRfky

または、以下の手順で手動作成：

1. https://github.com/hiderin3658/CreateMovie にアクセス
2. "Pull requests" タブをクリック
3. "New pull request" をクリック
4. base: `main` ← compare: `claude/modular-video-system-refactor-011CUscFwzJxXqi1vZuFRfky` を選択
5. タイトル: "Modular Video Generation System Refactor"
6. 上記の内容をコピーして貼り付け
7. "Create pull request" をクリック
