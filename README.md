# すごいぞコードのQちゃん！ (Amazing QR Code Reader)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/python-3.11-blue)

カメラを使用したリアルタイムQRコード読み取り、画像からのQRコード読み取り、およびカスタマイズ可能なQRコード生成機能を備えた多機能QRコードアプリケーションです。

[English version below](#english)

## 機能

- 📷 カメラを使用したリアルタイムQRコード読み取り
- 🖼️ 画像ファイルからのQRコード読み取り
- ✨ カスタマイズ可能なQRコード生成
  - カラーカスタマイズ
  - SVG形式での保存
- 🎨 直感的なGUIインターフェース（PyQt6使用）
- 💾 生成したQRコードのSVG形式での保存

## インストール方法

### 実行ファイルを使用する場合

1. [リリースページ](https://github.com/yourusername/amazing-qr-code-reader/releases)から最新版をダウンロード
2. ダウンロードしたファイルを実行

### ソースコードから実行する場合

#### 必要条件

- Python 3.11
- pip (Pythonパッケージマネージャー)

### セットアップ手順

1. リポジトリのクローン:

```bash
git clone https://github.com/yourusername/amazing-qr-code-reader.git
cd amazing-qr-code-reader
```

2. Poetry環境のセットアップ:

```bash
curl -sSL https://install.python-poetry.org | python3 -
poetry install
```

3. アプリケーションの実行:

```bash
poetry run python code_of_Q.py
```

## 使用方法

### アプリケーションの起動

```bash
python code_of_Q.py
```

### 実行ファイルの生成

MacOS用の実行ファイルを生成する場合:

```bash
pyinstaller --onefile --windowed \
  --hidden-import=PIL._tkinter_finder \
  --hidden-import=qrcode.image.svg \
  --hidden-import=svgwrite \
  --add-binary='/System/Library/Frameworks/Tk.framework/Tk:tk' \
  --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl:tcl' \
  code_of_Q.py
```

Windows用の実行ファイルを生成する場合:

```bash
pyinstaller --onefile --windowed code_of_Q.py
```

## 主な機能の使用方法

### QRコードの生成

1. テキストフィールドに内容を入力
2. 「QRコードの作成」ボタンをクリック
3. 必要に応じて「QRコードの色を選択」で色をカスタマイズ
4. 「QRコードをSVGで保存」でSVG形式で保存

### カメラでQRコードを読み取る

1. アプリケーション起動時にカメラが自動的に有効化
2. QRコードをカメラに向ける
3. 読み取った内容が自動的にテキストフィールドに表示

### 画像からQRコードを読み取る

1. 「画像からQRコードを読み取る」ボタンをクリック
2. QRコードを含む画像ファイルを選択
3. 読み取った内容がテキストフィールドに表示

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。

### 使用ライブラリとそのライセンス

- OpenCV (opencv-python-headless): Apache 2.0 License
- Pillow: HPND License
- qrcode: MIT License
- svgwrite: MIT License

## 依存ライブラリ

```python
opencv-python>=4.8.0
pillow>=10.0.0
qrcode>=7.4.2
PyQt6>=6.4.0
```

## 貢献について

プロジェクトへの貢献を歓迎します！以下の方法で貢献できます：

1. Issueの報告
2. 機能改善の提案
3. プルリクエストの作成

## 注意事項

- カメラへのアクセス権限が必要です
- MacOSでの初回起動時はセキュリティの確認が必要な場合があります

---

## English

## Amazing QR Code Reader (English)

A versatile QR code application featuring real-time QR code reading using camera, QR code reading from images, and customizable QR code generation capabilities.

[Details in English will be similar to the Japanese version above, formatted in English]

## Features

- 📷 Real-time QR code reading using camera
- 🖼️ QR code reading from image files
- ✨ Customizable QR code generation
  - Color customization
  - SVG format export
- 🎨 Intuitive GUI interface
- 💾 Save generated QR codes in SVG format

[Continue with installation, usage, etc. in English...]

## License

This project is released under the [MIT License](LICENSE).

### Third-party Libraries and Licenses

- OpenCV (opencv-python-headless): Apache 2.0 License
- Pillow: HPND License
- qrcode: MIT License
- svgwrite: MIT License

## Dependencies

```python
opencv-python>=4.8.0
pillow>=10.0.0
qrcode>=7.4.2
PyQt6>=6.4.0
```

## Contributing

Contributions are welcome! You can contribute by:

1. Reporting issues
2. Suggesting enhancements
3. Creating pull requests

## Notes

- Camera access permission is required
- MacOS may require security confirmation on first launch
