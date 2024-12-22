# MacOSでQRコードアプリケーションを実行ファイル化する方法

## 1. 開発環境の準備

### Python環境の確認

まず、Python 3.8以上がインストールされていることを確認します：

```bash
python3 --version
```

### 仮想環境の作成（推奨）

新しい仮想環境を作成して有効化します：

```bash
python3 -m venv qrenv
source qrenv/bin/activate
```

## 2. 依存関係のインストール

### 既存の依存関係をクリーンアップ

```bash
pip uninstall -r requirements.txt
pip uninstall tk opencv-python Pillow qrcode svgwrite
```

### 新しい依存関係をインストール

requirements.txtの内容が更新されていることを確認し、インストールを実行：

```bash
pip install -r requirements.txt
```

### PyInstallerのインストール

```bash
pip install --upgrade pyinstaller
```

## 3. 実行ファイルの生成

### PyInstallerの実行

以下のコマンドを1行で実行します：

```bash
pyinstaller --onefile --windowed \
  --hidden-import=PIL._tkinter_finder \
  --hidden-import=qrcode.image.svg \
  --hidden-import=svgwrite \
  --add-binary='/System/Library/Frameworks/Tk.framework/Tk:tk' \
  --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl:tcl' \
  code_of_Q.py
```

## 4. アプリケーションの確認

### 生成されたファイルの確認

`dist`フォルダ内に生成された実行ファイルを確認します。

### 動作テスト

以下の機能が正常に動作することを確認します：

- カメラ映像の表示
- QRコードの読み取り
- QRコードの生成
- SVGファイルの保存

## 5. トラブルシューティング

### カメラアクセスの問題

MacOSでカメラが認識されない場合：

1. システム環境設定 > セキュリティとプライバシー を開く
2. カメラ のタブを選択
3. アプリケーションのカメラアクセスを許可

### 依存関係の問題

もし実行時にライブラリ関連のエラーが発生する場合：

1. .specファイルを確認

```python
# code_of_Q.spec
a = Analysis(
    ['code_of_Q.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PIL._tkinter_finder', 'qrcode.image.svg', 'svgwrite'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)
```

2.specファイルを使用してビルド

```bash
pyinstaller code_of_Q.spec
```

### その他の注意点

- アプリケーションの初回起動時はセキュリティの警告が表示される場合があります
- 開発環境とターゲット環境のPythonバージョンは揃えることを推奨します
- カメラ機能が動作しない場合は、別のカメラデバイスを試すことも検討してください

## 6. デプロイメント

### アプリケーションの配布

生成された実行ファイルを配布する際は、以下の点に注意してください：

- 実行権限の確認
- セキュリティ設定の説明
- 必要なシステム要件の明記

---
注: この手順書はMacOS向けです。他のOSでは異なる手順が必要になる場合があります。
