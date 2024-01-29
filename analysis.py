import cv2
import tkinter as tk
from PIL import Image, ImageTk
from fer import FER
import time
import os
import random

class FERApp:
    def __init__(self, root, window_id):
        self.root = root
        if window_id == 1:
            self.root.title(f"FER Analysis - Window for you")
        if window_id == 2:
            self.root.title(f'FER Analysis - Window for companion')
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
        
        self.threshold_angry = 0.2  # この値を適切な閾値に設定
        self.threshold_sad = 0.2
        self.threshold_fear = 0.2
        self.second_window = None
        self.second_window_label = None
        self.is_second_window = False
        
        self.window_id = window_id

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
            
            if result:
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
                        
                        # angry converter
                        print(average_emotion['angry'])
                        # 閾値を超えていて，ウィンドウがないなら生成
                        if average_emotion.get('angry', 0) > self.threshold_angry or average_emotion.get('sad', 0) > self.threshold_sad or average_emotion.get('fear', 0) > self.threshold_fear:
                            print('show')
                            self.show_second_window()
                        # 超えていないかつ存在するなら消す
                        elif self.is_second_window:
                            self.close_second_window()
                            
                    else:
                         #Set neutral as default
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
        
    def show_second_window(self):
        if not self.is_second_window:
             # 別のウィンドウを作成
            self.second_window = tk.Toplevel(self.root)
            self.second_window.title("Don't be nervous!")
            self.label = tk.Label(self.root, text=f'Do not be so nervous!')
            self.label.pack(pady=20)

            # 別のウィンドウに画像を表示
            img_path = self.show_random_file()  # ここに別の画像のパスを設定
            img = Image.open(img_path)
            img = ImageTk.PhotoImage(img)
            self.second_window_label = tk.Label(self.second_window, image=img)
            self.second_window_label.image = img
            self.second_window_label.pack()

            # 別のウィンドウを閉じるためのボタン
            close_button = tk.Button(self.second_window, text="Close", command=self.close_second_window)
            close_button.pack()

            # ウィンドウが表示されたことをフラグに設定
            self.is_second_window = True

    def close_second_window(self):
        self.second_window.destroy()
        # ウィンドウが閉じられたことをフラグに設定
        self.is_second_window = False
    
    def show_random_file(self):
        directory = 'img/posi'
        file_list = os.listdir(directory)
        selected_file = random.choice(file_list)
        return os.path.join(directory, selected_file)
        
        
    def exit_app(self):
        self.root.destroy()


def main():
    root = tk.Tk()
    root.geometry("400x100")

    def create_new_window(window_id):
        new_window = tk.Toplevel(root)
        app = FERApp(new_window, window_id)

    btn_window1 = tk.Button(root, text="Open Window for you", command=lambda: create_new_window(1))
    btn_window1.pack(side="left")

    btn_window2 = tk.Button(root, text="Open Window for companion", command=lambda: create_new_window(2))
    btn_window2.pack(side="right")
    
    def exit_app():
        root.destroy()
    
    btn_exit = tk.Button(root, text="Exit", command=exit_app)
    btn_exit.pack(side="bottom" )

    root.mainloop()


if __name__ == "__main__":
    main()
