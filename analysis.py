import cv2
import tkinter as tk
from PIL import Image, ImageTk
from fer import FER
import time

class FERApp:
    def __init__(self, root, window_id):
        self.root = root
        self.root.title(f"FER Analysis - Window {window_id}")
        self.root.geometry("400x300")  # Set a uniform size

        self.video_source = 0  # Change this if needed for a different webcam

        self.fer = FER(mtcnn=True)

        self.vid = cv2.VideoCapture(self.video_source, cv2.CAP_DSHOW)

        self.label_emotion = tk.Label(root, text="", font=("Arial", 18))
        self.label_emotion.pack()

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.emotion_history = []
        self.frames_since_last_update = 0  # 最後の更新からのフレーム数
        self.last_update_time = time.time()

        # Dictionary to map emotions to image paths
        self.emotion_images = {
            'happy': 'img/happy.png',  # Replace with your image path
            'sad': 'img/sad.png',  # Replace with your image path
            'angry': 'img/angry.png',  # Replace with your image path
            'neutral': 'img/neutral.png',  # Replace with your image path
            'surprise': 'img/surprise.png',  # Replace with your image path
            'fear': 'img/fear.png',  # Replace with your image path
            # Add other emotions and their respective image paths
        }
        
        # Exit Button
        self.btn_exit = tk.Button(root, text="Exit", command=self.exit_app)
        self.btn_exit.pack()

        self.update()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.fer.detect_emotions(frame)

            for face in result:
                emotion = face['emotions']

                self.emotion_history.append(emotion)
                self.frames_since_last_update += 1

            current_time = time.time()
            elapsed_time = current_time - self.last_update_time

            if elapsed_time >= 1:  # 1秒ごとに処理
                # 平均感情の計算
                if self.emotion_history:  # リストが空でない場合に処理を行う
                    average_emotion = {emotion: sum(data[emotion] for data in self.emotion_history) / len(self.emotion_history) for emotion in result[0]['emotions']}
                     # 一番大きな平均値を持つ感情を取得
                    dominant_emotion = max(average_emotion, key=average_emotion.get)
                else:
                     # 一番大きな平均値を持つ感情を取得
                    dominant_emotion = 'neutral'

               

                # Update the label with the dominant emotion
                self.label_emotion.config(text=f"Dominant emotion: {dominant_emotion.capitalize()}")

                # Display an image based on the detected emotion
                if dominant_emotion in self.emotion_images:
                    img_path = self.emotion_images[dominant_emotion]
                    img = Image.open(img_path)
                    img = ImageTk.PhotoImage(img)
                    self.image_label.config(image=img)
                    self.image_label.image = img  # Keep a reference to avoid garbage collection

                # リストをクリアして次のデータ収集の準備
                self.emotion_history.clear()
                self.frames_since_last_update = 0
                self.last_update_time = time.time()

        self.root.after(100, self.update)
        
    def exit_app(self):
        self.root.destroy()


def main():
    root = tk.Tk()
    root.geometry("400x100")

    def create_new_window(window_id):
        new_window = tk.Toplevel(root)
        app = FERApp(new_window, window_id)

    btn_window1 = tk.Button(root, text="Open Window 1", command=lambda: create_new_window(1))
    btn_window1.pack(side="left")

    btn_window2 = tk.Button(root, text="Open Window 2", command=lambda: create_new_window(2))
    btn_window2.pack(side="right")
    
    def exit_app():
        root.destroy()
    
    btn_exit = tk.Button(root, text="Exit", command=exit_app)
    btn_exit.pack(side="bottom" )

    root.mainloop()


if __name__ == "__main__":
    main()