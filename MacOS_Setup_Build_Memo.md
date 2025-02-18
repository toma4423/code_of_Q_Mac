# MacOS 環境再構築 & ビルド手順メモ

このドキュメントは、GitHubからリポジトリをクローン後、MacOS環境でプロジェクトの再構築およびビルド作業を行うための手順をまとめたものです。

---

## 1. リポジトリのクローン

Terminal（ターミナル）を開き、以下のコマンドを実行してリポジトリをクローンします。

```bash
git clone https://github.com/toma4423/code_of_Q_Mac.git
cd code_of_Q_Mac
```

---

## 2. Poetry を使った環境の再構築

### 2.1 Poetry のインストール（未インストールの場合）
もしMacOSにPoetryがインストールされていない場合、以下のコマンドを実行してインストールします。

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

または、Homebrewを利用してインストールすることも可能です。

```bash
brew install poetry
```

### 2.2 依存パッケージのインストール
クローンしたプロジェクトディレクトリ内で、以下のコマンドを実行して依存パッケージをインストールします。

```bash
poetry install
```

### 2.3 仮想環境への入室
依存パッケージのインストールが完了したら、以下のコマンドでPoetryの仮想環境に入ります。

```bash
poetry shell
```

---

## 3. プロジェクトの動作確認

仮想環境内でアプリケーションが正しく動作するか確認してください。

```bash
python code_of_Q.py
```

※ カメラが利用可能な環境であることを確認してください。

---

## 4. ビルド作業（PyInstallerの利用）

### 4.1 PyInstaller のインストール（必要な場合）
もしPyInstallerがインストールされていない場合は、仮想環境内で以下のコマンドを実行します。

```bash
pip install pyinstaller
```

### 4.2 アプリケーションのパッケージング
以下のコマンドを実行して、MacOS用の実行ファイルを生成します。  
（必要に応じて、`--hidden-import` や `--add-binary` のパラメータは環境に合わせて調整してください。）

```bash
pyinstaller --onefile --windowed \
  --hidden-import=PIL._tkinter_finder \
  --hidden-import=qrcode.image.svg \
  --hidden-import=svgwrite \
  --add-binary '/System/Library/Frameworks/Tk.framework/Tk:tk' \
  --add-binary '/System/Library/Frameworks/Tcl.framework/Tcl:tcl' \
  code_of_Q.py
```

### 4.3 ビルド成果物の確認
ビルドが完了すると、`dist` フォルダ内に実行ファイルが生成されます。  
実行ファイルをダブルクリックするか、Terminalから実行して正しく起動するか確認してください。

---

## 5. トラブルシューティング

- **セキュリティ設定:**  
  ビルド後、初回起動時に「不明な開発元からのアプリケーション」という警告が表示された場合は、**システム環境設定 > セキュリティとプライバシー**から該当アプリケーションを許可してください。

- **依存関係:**  
  依存パッケージのインストールやビルドで問題が発生した場合、各パッケージの公式ドキュメントまたはエラーメッセージを確認してください。

- **その他:**  
  仮想環境内での動作確認やビルド作業を行う前に、リポジトリの最新状態になっていることを確認してください。

---

このメモに沿ってお作業いただければ、MacOS環境での環境再構築およびビルドがスムーズに行えるはずです。  
何か問題があれば、随時本ドキュメントを更新してください。 