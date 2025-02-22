# MacOS用アプリケーションのビルド手順

## 0. 初期セットアップ（初回のみ）
```bash
# リポジトリのクローン
git clone [repository-url]
cd [repository-name]

# Poetry環境のセットアップ
poetry install
```

## 1. 環境準備

```bash
# Poetry環境に入る
poetry shell

# PyInstallerをインストール
poetry add --group dev pyinstaller
```

## 2. Info.plistの準備

`Info.plist`ファイルに以下の内容を設定：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>コードのQちゃん</string>
    <key>CFBundleExecutable</key>
    <string>コードのQちゃん</string>
    <key>CFBundleIconFile</key>
    <string>code_of_Q.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.toma.codeofq</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSCameraUsageDescription</key>
    <string>QRコードの読み取りにカメラを使用します</string>
</dict>
</plist>
```

## 3. アプリケーションのビルド

```bash
# 既存のビルドファイルを削除
rm -rf build dist *.spec

# PyInstallerでビルド
pyinstaller \
  --windowed \
  --name "コードのQちゃん" \
  --icon=code_of_Q.icns \
  --add-binary="Info.plist:." \
  --target-arch arm64 \
  --noconfirm \
  --clean \
  --hidden-import=PyQt6 \
  --hidden-import=PyQt6.QtCore \
  --hidden-import=PyQt6.QtGui \
  --hidden-import=PyQt6.QtWidgets \
  --hidden-import=PIL._tkinter_finder \
  --hidden-import=qrcode.image.svg \
  --hidden-import=svgwrite \
  code_of_Q.py

# Info.plistを正しい場所にコピー
cp Info.plist dist/コードのQちゃん.app/Contents/
```

## 4. 配布用パッケージの作成

```bash
# READMEをdistディレクトリにコピー
cp README.md dist/

# distディレクトリに移動
cd dist

# 配布用zipファイルの作成
zip -r コードのQちゃん_v1.0.0.zip コードのQちゃん.app README.md
```

## 注意事項

- ビルド時にはPoetry環境内で作業すること
- バージョン番号は`Info.plist`と`pyproject.toml`で一致させること
- アイコンファイル（.icns）が正しく配置されていることを確認
- ビルド後は必ずアプリケーションの動作確認を行うこと

## トラブルシューティング

1. カメラアクセスエラーが発生する場合：
   - Info.plistが正しい場所にあることを確認
   - NSCameraUsageDescriptionが設定されていることを確認

2. アイコンが表示されない場合：
   - .icnsファイルのパスを確認
   - Info.plistのCFBundleIconFile設定を確認
