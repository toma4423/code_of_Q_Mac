# MacOSデスクトップアプリケーション 開発プロセスメモ

このドキュメントは、**すごいぞコードのQちゃん！** アプリケーションをMacOS用のデスクトップアプリケーションとして開発・デプロイするためのプロセスをまとめたものです。

---

## 1. Gitの設定

### 1.1 Gitリポジトリの初期化
- プロジェクトのルートディレクトリで以下のコマンドを実行してGitリポジトリを初期化します。

```bash
git init
```

### 1.2 .gitignore の設定
- 以下のような内容で `.gitignore` ファイルを作成し、不要なファイルやディレクトリを除外します。

```gitignore
# Python関連
__pycache__/
*.pyc
*.pyo

# 仮想環境ディレクトリ（例: Poetryでは .venv/）
.venv/
env/

# PyInstaller生成ファイル
/dist/
/build/
/*.spec

# エディタ関連
*.swp
```

### 1.3 最初のコミット
- すべてのファイルをステージして初期コミットを行います。

```bash
git add .
git commit -m "Initial commit: プロジェクトの初期セットアップ"
```

---

## 2. Poetryによる環境構築

### 2.1 Poetryのインストール
- Poetryが未インストールの場合、以下のコマンドでインストールします。

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

または、pipからインストールできます。

```bash
pip install poetry
```

### 2.2 プロジェクトの初期化
- プロジェクトルートで以下を実行し、`pyproject.toml` ファイルを生成します。

```bash
poetry init
```

対話形式でプロジェクト情報を入力してください。

### 2.3 依存関係の追加
- 必要な依存ライブラリ（`opencv-python-headless`、`Pillow`、`qrcode[pil,svg]`、`svgwrite`、MacOS用に**pyobjc**）を追加します。

```bash
poetry add opencv-python-headless Pillow qrcode[pil,svg] svgwrite pyobjc
```

### 2.4 仮想環境の作成と有効化
- Poetryは自動的に仮想環境を管理します。以下のコマンドでシェルに入ります。

```bash
poetry shell
```

- 仮想環境内で `python code_of_Q.py` を実行してアプリの動作確認を行います。

---

## 3. MacOS用へのプログラム改修

### 3.1 ウィンドウ制御の実装
- `code_of_Q.py` では、MacOS専用にウィンドウを最前面に表示するため、以下のような処理を追加しました。

  - `sys.platform == "darwin"` を条件に、`AppKit` から `NSApp` や `NSApplicationActivationPolicyRegular` を利用。
  - ウィンドウをリフトし、一時的に `-topmost` 属性を付加することで前面表示しています。

  これにより、MacOS環境でのユーザー体験が向上します。

### 3.2 その他の修正
- 必要に応じ、MacOS固有の最適化や設定を追加してください。

---

## 4. MacOS用実行ファイルの生成

### 4.1 PyInstallerによるパッケージング
- MacOSビルド用の手順については、既存の `MacOS_build.md` を参照してください。  
- 例として、以下のコマンドで実行ファイルを生成します。

```bash
pyinstaller --onefile --windowed \
  --hidden-import=PIL._tkinter_finder \
  --hidden-import=qrcode.image.svg \
  --hidden-import=svgwrite \
  --add-binary '/System/Library/Frameworks/Tk.framework/Tk:tk' \
  --add-binary '/System/Library/Frameworks/Tcl.framework/Tcl:tcl' \
  code_of_Q.py
```

### 4.2 動作確認
- 生成された実行ファイル（`dist` ディレクトリ内）を実行して、以下を確認してください。
  - カメラ映像の表示
  - QRコードの読み取りと生成
  - ウィンドウが前面に表示されるか（MacOSでのテスト）

---

## 5. その他の注意事項

- **セキュリティ設定:**  
  MacOSで初回起動時に「不明な開発元からのアプリケーション」という警告が出る場合、システム環境設定 > セキュリティとプライバシーから許可してください。

- **依存性管理:**  
  Poetryによって生成される `pyproject.toml` と `poetry.lock` により、環境間での依存性の一貫性が維持されます。

- **GitとCI/CD:**  
  今後、CI/CDパイプラインに組み込む場合は、GitHub Actionsなどを利用して自動テストやビルド処理を行います。

---

## 6. まとめ

このプロセスメモに沿って、以下のステップでMacOS用デスクトップアプリケーションの開発環境を整備できます。

1. **Gitの設定:**  
   リポジトリ初期化と `.gitignore` の作成、初回コミット。

2. **Poetryによる環境構築:**  
   `poetry init` と `poetry add` による依存性管理、仮想環境の作成。

3. **プログラム改修:**  
   `code_of_Q.py` におけるMacOS専用ウィンドウ制御処理の実装。

4. **実行ファイルの生成:**  
   PyInstallerを使ったMacOS用実行ファイルのパッケージングと動作確認。

以上の手順により、MacOS上で快適に動作するデスクトップアプリケーションの開発が可能となります。 