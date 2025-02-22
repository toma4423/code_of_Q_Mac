# MacOS アプリケーション GitHub リリース トラブルシューティング

このドキュメントは、MacOSアプリケーションをGitHubでリリースする際に発生した問題と、その解決策をまとめたものです。

## 1. 「壊れています」エラー

### 問題
- Google DriveやGitHubからダウンロードしたアプリケーションを実行すると「壊れています」というエラーが表示される
- これはmacOSのGatekeeperとQuarantine属性による保護機能が原因

### 解決策
1. GitHub Actionsでのビルド時に拡張属性を削除：
```yaml
- name: Remove extended attributes
  run: |
    xattr -rc dist/
```

2. zip圧縮前に属性を削除することで、ダウンロード後のアプリケーションでも問題が発生しないように対応

### 実装詳細
```yaml
steps:
  # ビルド後の処理
  - name: Remove extended attributes
    run: |
      xattr -rc dist/
  
  - name: Create ZIP archive
    run: |
      cd dist
      zip -r "../コードのQちゃん.zip" .
```

## 2. バージョン管理の整合性

### 問題
- 複数の設定ファイルでバージョン番号を管理する必要がある
- バージョン番号の不一致によりユーザーの混乱を招く可能性

### 影響を受けるファイル
- `pyproject.toml`
- `Info.plist`
- `CHANGELOG.md`

### 解決策
バージョン更新時のチェックリスト：
1. `pyproject.toml`のバージョン更新
```toml
[project]
version = "0.1.1"  # バージョン番号を更新
```

2. `Info.plist`のバージョン更新
```xml
<key>CFBundleShortVersionString</key>
<string>0.1.1</string>
```

3. `CHANGELOG.md`に新バージョンの記録を追加
```markdown
## [v0.1.1] - 2024-03-xx
### 改善
- 変更内容を記録
```

## 3. ビルド環境の指定

### 問題
- macOSのバージョンによる互換性の問題
- ビルド環境とターゲット環境の不一致

### 解決策
1. `Info.plist`で最小システム要件を指定：
```xml
<key>LSMinimumSystemVersion</key>
<string>10.13.0</string>
```

2. GitHub Actionsで最新の安定版を使用：
```yaml
jobs:
  build:
    runs-on: macos-latest
```

## 4. アプリケーションの権限設定

### 問題
- カメラアクセスの許可が必要
- 初回起動時の権限設定が必要

### 解決策
1. `Info.plist`にカメラ使用の説明を追加：
```xml
<key>NSCameraUsageDescription</key>
<string>QRコードの読み取りにカメラを使用します</string>
```

2. ユーザーへの説明をREADMEに追加：
- 初回起動時は右クリック→「開く」で実行
- カメラアクセスの許可が必要

## 推奨事項

1. リリース前のチェックリスト：
   - すべての設定ファイルでバージョン番号が一致していることを確認
   - CHANGELOGが適切に更新されていることを確認
   - ビルドスクリプトの設定を確認

2. バージョン管理：
   - セマンティックバージョニングの採用
   - タグ名とバージョン番号の一致確認

3. ドキュメント：
   - インストール手順の明確な記載
   - 必要な権限設定の説明
   - トラブルシューティングガイドの提供

## 拡張属性のトラブルシューティング

### com.apple.provenance属性について
- macOSがファイルの出所を追跡するための属性
- 配布時には削除することが推奨
- `xattr -d com.apple.provenance ファイル名`で削除可能
- `xattr -cr ファイル名`で全ての拡張属性を削除可能

### com.apple.provenance属性の完全な削除方法
1. `-X`オプションを使用したzip作成：
   ```bash
   zip -X -r ファイル名.zip ソースディレクトリ/
   ```

2. 既存の属性の直接削除：
   ```bash
   xattr -d com.apple.provenance ファイル名.zip
   ```

注意: 一部の拡張属性は通常の方法では削除できない場合があります。その場合は上記の手順を組み合わせて使用してください。


### 頑固な拡張属性の対処方法
一時ディレクトリを使用した完全なクリーンビルド：
```bash
mkdir temp_zip
cp -r dist/* temp_zip/
xattr -cr temp_zip
cd temp_zip
zip -X -r ../コードのQちゃん_new.zip .
cd ..
mv コードのQちゃん_new.zip コードのQちゃん.zip
rm -rf temp_zip
```

この方法は、既存の拡張属性が完全に削除できない場合の最終手段として有効です。


### com.apple.provenance属性の特殊な動作について
macOS Sonoma (14.0) 以降、`com.apple.provenance`属性は特に保護されており、通常の方法では完全に削除できない場合があります。

この属性は：
- システムのセキュリティ機能の一部
- ファイルの出所を追跡
- 一般的なユーザーの使用には影響しない

対応方法：
1. この属性が残っていても、アプリケーションの機能には影響しません
2. エンドユーザーの環境では、システムが適切に処理します
3. 開発・テスト時にこの属性が表示されるのは正常な動作です


### シンボリックリンクの保持に関する問題

問題：
- zip化の過程でFrameworksディレクトリ内のシンボリックリンクが実ファイルに変換される
- これによりQtの依存関係の解決に問題が発生し、アプリケーションがクラッシュする

解決策：
1. tar.gzを使用してシンボリックリンクを保持：
   ```bash
   # アプリケーションを圧縮
   tar -czf コードのQちゃん.tar.gz dist/
   ```

確認方法：
1. 解凍後、以下のシンボリックリンクが正しく保持されているか確認：
   ```bash
   # Qtフレームワークのリンク
   ls -la dist/コードのQちゃん.app/Contents/Frameworks/Qt*
   
   # PyQt6のQtライブラリ構造
   ls -la dist/コードのQちゃん.app/Contents/Frameworks/PyQt6/Qt6/lib/Qt*.framework/Versions/Current
   
   # その他の重要なリンク（cv2, PIL）
   ls -la dist/コードのQちゃん.app/Contents/Frameworks/cv2/.dylibs
   ls -la dist/コードのQちゃん.app/Contents/Frameworks/PIL/.dylibs
   ```

2. 以下のリンクが存在することを確認：
   - QtCore, QtGui, QtWidgets等が`PyQt6/Qt6/lib/...`を指している
   - フレームワークのVersions/Currentが`A`を指している
   - cv2とPILの`.dylibs`が`__dot__dylibs`を指している
   - Pythonフレームワークの`Current`が正しいバージョンを指している

## 参考情報

- [macOS Gatekeeper について](https://support.apple.com/ja-jp/HT202491)
- [アプリケーションの公証について](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [GitHub Actions について](https://docs.github.com/ja/actions) 