import cv2
import tkinter as tk
from PIL import Image, ImageTk
from fer import FER
import time
import os
import random

class YourApp:
    def __init__(self, root, window_id):
        self.root = root
        self.root.title("FER Analysis")

        self.video_source = 0  # Change this if needed for a different webcam
        self.windw_id = window_id

        self.fer = FER(mtcnn=True)

        self.vid = cv2.VideoCapture(self.video_source)
        self.width='800'  # Set a uniform size
        self.height='450'

        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()

        self.btn_quit = tk.Button(root, text="Quit", command=self.quit)
        self.btn_quit.pack()
        
        self.label_emotion = tk.Label(root, text="", font=("Arial", 18))
        self.label_emotion.pack()

        self.image_label = tk.Label(root)
        self.image_label.pack()
        
        self.alter_image_label = tk.Label(root)
        self.alter_image_label.pack()

        self.emotion_history = []
        self.frames_since_last_update = 0  # 最後の更新からのフレーム数
        self.last_update_time = time.time()
        
        self.threshold_angry = 0.3  # この値を適切な閾値に設定
        self.threshold_sad = 0.3
        self.threshold_fear = 0.3
        self.second_window = None
        self.second_window_label = None
        self.is_second_window = False
        
        self.emotion_images = {
            'happy': 'img/happy.png',  # Replace with your image path
            'sad': 'img/sad.png',  # Replace with your image path
            'angry': 'img/angry.png',  # Replace with your image path
            'neutral': 'img/neutral.png',  # Replace with your image path
            'surprise': 'img/surprise.png',  # Replace with your image path
            'fear': 'img/fear.png',  # Replace with your image path
            # Add other emotions and their respective image paths
        }
        
        if self.windw_id == 1:
            self.update1()
        if self.windw_id == 2:
            self.update2()

    def update1(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.fer.detect_emotions(frame)
            
            for face in result:
                (x, y, w, h) = face['box']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                emotion = face['emotions']
                cv2.putText(frame, max(emotion, key=emotion.get), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)            
            
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
                        print(average_emotion)
                        # 閾値を超えていて，ウィンドウがないなら生成
                        if average_emotion.get('angry', 0) > self.threshold_angry:
                            print('angry')
                            self.show_img(win_id = 1)
                        elif average_emotion.get('sad', 0) > self.threshold_sad or average_emotion.get('disgust', 0) > self.threshold_sad:
                            print('sad')
                            self.show_img(win_id = 2)
                        # 超えていないかつ存在するなら消す
                        elif self.is_second_window:
                            self.close_img()
                            print("hello")
                    else:
                         #Set neutral as default
                        dominant_emotion = 'neutral'
                
                    # Update the label with the dominant emotion
                    self.label_emotion.config(text=f"Dominant emotion: {dominant_emotion.capitalize()}")

                    # リストをクリアして次のデータ収集の準備
                    self.emotion_history.clear()
                    self.frames_since_last_update = 0
                    self.last_update_time = time.time()

        self.root.update_idletasks()
        self.root.after(100, self.update1)
        
    def update2(self):
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
        self.root.update_idletasks()
        self.root.after(100, self.update2)
        
    def show_img(self, win_id):
        if not self.is_second_window:
            win_id = win_id
            alter_img_path = self.show_random_file(win_id)
            original_img = Image.open(alter_img_path)

            # リサイズしたいサイズを指定
            target_size = (400, 300)
            resized_img = original_img.resize(target_size)

            alter_img = ImageTk.PhotoImage(resized_img)

            # angryの閾値を超えているかどうかを確認
            if win_id == 1:
                self.alter_image_label = tk.Label(self.root)
                self.alter_image_label.configure(image=alter_img)
                self.alter_image_label.place(x=300, y=80)
                self.alter_image_label.image = alter_img
                self.is_second_window = True
            elif win_id == 2:
                self.alter_image_label = tk.Label(self.root)
                self.alter_image_label.configure(image=alter_img)
                self.alter_image_label.place(x=300, y=80)
                self.alter_image_label.image = alter_img
                self.is_second_window = True
                
    def close_img(self):
        if self.alter_image_label:
            self.alter_image_label.destroy()
        self.alter_image_label = None
        self.is_second_window = False
    
    def show_random_file(self, win_id):
        if win_id == 1:
            directory = 'img/relax'
        if win_id == 2:
            directory = 'img/happiness'
        file_list = os.listdir(directory)
        selected_file = random.choice(file_list)
        return os.path.join(directory, selected_file)

    def quit(self):
        self.vid.release()
        self.root.destroy()

def main():
    root = tk.Tk()
    root.geometry("400x100")

    def create_new_window(window_id):
        new_window = tk.Toplevel(root)
        app = YourApp(new_window, window_id)
            
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
