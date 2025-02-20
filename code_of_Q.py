import sys
import cv2
import atexit
import io
from PIL import Image
import qrcode
from qrcode.image.svg import SvgImage
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QTextEdit, QFileDialog, QColorDialog, QMessageBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap


class QRCodeScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('すごいぞコードのQちゃん！')
        self.setGeometry(100, 100, 700, 600)

        # カメラリソース初期化
        self.cap = None
        self.initialize_camera()
        
        # 終了時のクリーンアップを登録
        atexit.register(self.cleanup_resources)
        
        # 状態変数の初期化
        self.show_qr_code = False
        self.qr_image = None
        self.svg_image = None
        self.qr_fill_color = 'black'
        self.qr_back_color = 'white'
        
        # UIの設定
        self.setup_ui()
        
        # カメラが利用可能な場合のみフレーム更新を開始
        if self.cap is not None and self.cap.isOpened():
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)
        else:
            self.show_camera_error()

    def setup_ui(self):
        # メインウィジェットとレイアウト
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # ボタンレイアウト
        button_layout = QHBoxLayout()
        
        # ボタンの作成
        self.generate_button = QPushButton('QRコードの作成')
        self.load_button = QPushButton('画像からQRコードを読み取る')
        self.camera_button = QPushButton('カメラに戻る')
        self.save_button = QPushButton('QRコードをSVGで保存')
        self.color_button = QPushButton('QRコードの色を選択')
        self.clear_button = QPushButton('クリア')
        
        # ボタンの初期状態設定
        self.camera_button.hide()
        self.save_button.hide()
        
        # ボタンのイベント接続
        self.generate_button.clicked.connect(self.generate_qr_code)
        self.load_button.clicked.connect(self.read_qr_from_image)
        self.camera_button.clicked.connect(self.return_to_camera)
        self.save_button.clicked.connect(self.save_qr_code)
        self.color_button.clicked.connect(self.choose_color)
        self.clear_button.clicked.connect(self.clear_text)
        
        # ボタンをレイアウトに追加
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.camera_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.color_button)
        
        # テキストエリアの設定
        text_label = QLabel('スキャンまたは生成するテキスト:')
        self.text_edit = QTextEdit()
        self.text_edit.setFixedHeight(100)
        
        # 画像表示用ラベル
        self.image_label = QLabel()
        self.image_label.setFixedSize(480, 360)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # レイアウトに要素を追加
        layout.addLayout(button_layout)
        layout.addWidget(text_label)
        
        text_layout = QHBoxLayout()
        text_layout.addWidget(self.text_edit)
        text_layout.addWidget(self.clear_button)
        layout.addLayout(text_layout)
        
        layout.addWidget(self.image_label)
        
        main_widget.setLayout(layout)

    def initialize_camera(self):
        try:
            QMessageBox.information(
                self,
                'カメラアクセス',
                'カメラへのアクセス許可が求められた場合は「許可」を選択してください。'
            )
            
            # macOSでのカメラ初期化を最適化
            if sys.platform == 'darwin':
                self.cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
            else:
                self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                raise ValueError("Failed to open camera")
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.detector = cv2.QRCodeDetector()
            
        except Exception as e:
            self.cap = None
            QMessageBox.warning(
                self,
                'カメラエラー',
                'カメラの初期化に失敗しました。\nシステム設定でカメラへのアクセスを許可してください。'
            )
            print(f"Camera initialization error: {str(e)}", file=sys.stderr)

    def show_camera_error(self):
        self.image_label.setText(
            "カメラを利用できません\n画像からQRコードを読み取るか\nQRコードを生成してください"
        )

    def update_frame(self):
        if not self.show_qr_code and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                data, vertices, _ = self.detector.detectAndDecode(frame)
                
                if data:
                    self.text_edit.setText(data)
                
                # フレームを表示用に変換
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def generate_qr_code(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, '入力エラー', 'テキストフィールドに文字を入力してください')
            return

        max_characters = 4000
        if len(text) > max_characters:
            QMessageBox.warning(
                self,
                '文字数エラー',
                f'テキストが長すぎます。{max_characters}文字以内にしてください。'
            )
            return

        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            border=1,
        )
        qr.add_data(text)
        qr.make(fit=True)

        self.svg_image = qr.make_image(image_factory=SvgImage)
        self.qr_image = qr.make_image(
            fill=self.qr_fill_color,
            back_color=self.qr_back_color
        ).resize((320, 320), Image.LANCZOS)

        # QRコードを表示
        img_byte_arr = io.BytesIO()
        self.qr_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        qt_image = QImage.fromData(img_byte_arr)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))
        
        # ボタンの表示状態を更新
        self.show_qr_code = True
        self.camera_button.show()
        self.save_button.show()

    def choose_color(self):
        fill_color = QColorDialog.getColor()
        if fill_color.isValid():
            back_color = QColorDialog.getColor()
            if back_color.isValid():
                self.qr_fill_color = fill_color.name()
                self.qr_back_color = back_color.name()

    def read_qr_from_image(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            'QRコード画像を選択',
            '',
            'Images (*.png *.jpg *.jpeg *.bmp)'
        )
        if filename:
            image = cv2.imread(filename)
            if image is None:
                QMessageBox.critical(
                    self,
                    '読み込みエラー',
                    '画像ファイルの読み込みに失敗しました。形式を確認してください。'
                )
                return

            data, vertices, _ = self.detector.detectAndDecode(image)
            if data:
                self.text_edit.setText(data)
                QMessageBox.information(
                    self,
                    'QRコード読み取り',
                    'QRコードが正常に読み取られました'
                )
            else:
                QMessageBox.warning(
                    self,
                    'エラー',
                    'QRコードが画像内に見つかりませんでした。'
                )

    def save_qr_code(self):
        if self.svg_image is not None:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                'SVGファイルとして保存',
                '',
                'SVG files (*.svg)'
            )
            if filename:
                self.svg_image.save(filename)
                QMessageBox.information(
                    self,
                    '保存完了',
                    'QRコードがSVG形式で保存されました'
                )

    def return_to_camera(self):
        self.show_qr_code = False
        self.camera_button.hide()
        self.save_button.hide()

    def clear_text(self):
        self.text_edit.clear()

    def cleanup_resources(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()

    def closeEvent(self, event):
        self.cleanup_resources()
        event.accept()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = QRCodeScannerApp()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Application error: {str(e)}", file=sys.stderr)
        sys.exit(1)
