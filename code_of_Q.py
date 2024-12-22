import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
import cv2
from PIL import Image, ImageTk
import qrcode
from qrcode.image.svg import SvgImage
import sys
import atexit


class QRCodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("すごいぞコードのQちゃん！")
        self.root.geometry("700x600")

        # カメラリソース初期化
        self.cap = None
        self.initialize_camera()

        # 終了時のクリーンアップを登録
        atexit.register(self.cleanup_resources)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 以下は既存のUI初期化コード
        self.setup_ui()

        # カメラが利用可能な場合のみフレーム更新を開始
        if self.cap is not None and self.cap.isOpened():
            self.update_frame()
        else:
            self.show_camera_error()

    def initialize_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise ValueError("Failed to open camera")

            # カメラの設定を最適化
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.detector = cv2.QRCodeDetector()

        except Exception as e:
            self.cap = None
            print(f"Camera initialization error: {str(e)}", file=sys.stderr)

    def setup_ui(self):
        # Button frame setup
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Generate QR code button
        self.generate_button = tk.Button(
            button_frame, text="QRコードの作成", command=self.generate_qr_code
        )
        self.generate_button.grid(row=0, column=0, padx=10)

        # Read QR code from image button
        self.load_image_button = tk.Button(
            button_frame,
            text="画像からQRコードを読み取る",
            command=self.read_qr_from_image,
        )
        self.load_image_button.grid(row=0, column=1, padx=10)

        # Return to camera button
        self.return_to_camera_button = tk.Button(
            button_frame, text="カメラに戻る", command=self.return_to_camera
        )
        self.return_to_camera_button.grid(row=0, column=2, padx=10)
        self.return_to_camera_button.grid_remove()

        # Save SVG button
        self.save_button = tk.Button(
            button_frame, text="QRコードをSVGで保存", command=self.save_qr_code
        )
        self.save_button.grid(row=0, column=3, padx=10)
        self.save_button.grid_remove()

        # Color selection button
        self.color_button = tk.Button(
            button_frame, text="QRコードの色を選択", command=self.choose_color
        )
        self.color_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Result text area setup
        self.setup_text_area()

        # Canvas setup
        self.canvas = tk.Canvas(self.root, width=480, height=360)
        self.canvas.pack(pady=10)

        # Initialize state variables
        self.show_qr_code = False
        self.qr_image = None
        self.svg_image = None
        self.qr_fill_color = "black"
        self.qr_back_color = "white"

    def setup_text_area(self):
        self.result_label = tk.Label(self.root, text="スキャンまたは生成するテキスト:")
        self.result_label.pack()

        text_frame = tk.Frame(self.root)
        text_frame.pack(pady=10)

        self.clear_button = tk.Button(
            text_frame, text="クリア", command=self.clear_text
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.result_text = tk.Text(text_frame, height=4, width=50, wrap="word")
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_bar = tk.Scrollbar(text_frame, command=self.result_text.yview)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scroll_bar.set)

    def show_camera_error(self):
        self.canvas.create_text(
            240,
            180,
            text="カメラを利用できません\n画像からQRコードを読み取るか\nQRコードを生成してください",
            fill="red",
            anchor="center",
            justify="center",
        )

    def cleanup_resources(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()

    def on_closing(self):
        self.cleanup_resources()
        self.root.destroy()

    def update_frame(self):
        if not self.show_qr_code:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, anchor="nw", image=imgtk)
                self.canvas.imgtk = imgtk

                data, vertices, _ = self.detector.detectAndDecode(frame)
                if data:
                    self.result_text.delete("1.0", tk.END)
                    self.result_text.insert(tk.END, data)
        self.root.after(30, self.update_frame)

    def generate_qr_code(self):
        text = self.result_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning(
                "入力エラー", "テキストフィールドに文字を入力してください"
            )
            return

        max_characters = 4000
        if len(text) > max_characters:
            messagebox.showwarning(
                "文字数エラー",
                f"テキストが長すぎます。{max_characters}文字以内にしてください。",
            )
            return

        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            border=1,  # 余白を1に設定（デフォルトは4）
        )
        qr.add_data(text)
        qr.make(fit=True)

        self.svg_image = qr.make_image(image_factory=SvgImage)

        # 生成したQRコードの表示サイズを320x320に設定
        self.qr_image = qr.make_image(
            fill=self.qr_fill_color, back_color=self.qr_back_color
        ).resize((320, 320), Image.LANCZOS)

        self.show_qr_code = True
        qr_imgtk = ImageTk.PhotoImage(self.qr_image)
        self.canvas.create_image(0, 0, anchor="nw", image=qr_imgtk)
        self.canvas.imgtk = qr_imgtk

        self.return_to_camera_button.grid()
        self.save_button.grid()

    def choose_color(self):
        fill_color = colorchooser.askcolor(title="QRコードの色を選択")[1]
        back_color = colorchooser.askcolor(title="QRコードの背景色を選択")[1]
        if fill_color and back_color:
            self.qr_fill_color = fill_color
            self.qr_back_color = back_color

    def read_qr_from_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("画像ファイル", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            image = cv2.imread(file_path)
            if image is None:
                messagebox.showerror(
                    "読み込みエラー",
                    "画像ファイルの読み込みに失敗しました。形式を確認してください。",
                )
                return

            data, vertices, _ = self.detector.detectAndDecode(image)
            if data:
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, data)
                messagebox.showinfo(
                    "QRコード読み取り", "QRコードが正常に読み取られました"
                )
            else:
                messagebox.showwarning(
                    "エラー", "QRコードが画像内に見つかりませんでした。"
                )

    def save_qr_code(self):
        if self.svg_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".svg", filetypes=[("SVGファイル", "*.svg")]
            )
            if file_path:
                self.svg_image.save(file_path)
                messagebox.showinfo("保存完了", "QRコードがSVG形式で保存されました")

    def clear_text(self):
        self.result_text.delete("1.0", tk.END)

    def return_to_camera(self):
        self.show_qr_code = False
        self.return_to_camera_button.grid_remove()
        self.save_button.grid_remove()

    def __del__(self):
        if hasattr(self, "cap") and self.cap.isOpened():
            self.cap.release()


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = QRCodeScannerApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Application error: {str(e)}", file=sys.stderr)
        sys.exit(1)
