import cv2
import tkinter as tk
from PIL import Image, ImageTk
from fer import FER
import time
import os
import random

class Mirror:
    def __init__(self, app, image_path):
        self.app = app
        self.root = tk.Toplevel(app.root)
        self.root.title("Mirror Window")
        
        self.root.geometry("400x400+900+100")  # ウィンドウのサイズと位置を指定
        
        self.image_label = tk.Label(self.root)
        self.image_label.pack()
        
        self.label_emotion = tk.Label(self.root, text="", font=("Arial", 18))
        self.label_emotion.pack()

        self.new_image_path = None 
        
        self.update()

    def update(self):
        # FERAppから感情を取得
        emotion = self.app.get_emotion()

        # 画像のパスを取得
        new_image_path = self.app.get_image_path_for_emotion(emotion)

        # 新しい画像のパスがセットされていれば画像を更新
        img = Image.open(new_image_path)
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img  # Keep a reference to avoid garbage collection
        
        self.label_emotion.config(text=f"Dominant emotion: {emotion.capitalize()}")

        # 一定時間ごとに再度updateメソッドを呼び出す
        self.root.after(1000, self.update)

    def close_window(self):
        self.root.destroy()
        self.app.second_window_closed()  # FERAppにセカンドウィンドウが閉じられたことを通知


class FERApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FER Analysis")

        self.video_source = 0  # Change this if needed for a different webcam

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
        
        self.mirror = None
        self.dominant_emotion = 'neutral'
        
        self.emotion_images = {
            'happy': 'img/happy.png',  # Replace with your image path
            'sad': 'img/sad.png',  # Replace with your image path
            'angry': 'img/angry.png',  # Replace with your image path
            'neutral': 'img/neutral.png',  # Replace with your image path
            'surprise': 'img/surprise.png',  # Replace with your image path
            'fear': 'img/fear.png',  # Replace with your image path
        }
        
        # 先にミラー画面を設定
        self.mirror = Mirror(self, self.get_image_path_for_emotion(self.dominant_emotion))

        self.update()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            top, bottom, left, right = 0, 450, 220, 580
            frame = frame[top:bottom, left:right]

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
                        
                        # 閾値を超えていて，ウィンドウがないなら生成
                        if average_emotion.get('angry', 0) > self.threshold_angry:
                            self.show_img(win_id = 1)
                        elif average_emotion.get('sad', 0) > self.threshold_sad or average_emotion.get('disgust', 0) > self.threshold_sad:
                            self.show_img(win_id = 2)
                        # 超えていないかつ存在するなら消す
                        elif self.is_second_window:
                            self.close_img()
                    else:
                         #Set neutral as default
                        dominant_emotion = 'neutral'
                        
                    self.dominant_emotion = dominant_emotion
                    if not self.mirror:
                        self.mirror = Mirror(self, self.get_image_path_for_emotion(self.dominant_emotion))
                
                    # Update the label with the dominant emotion
                    self.label_emotion.config(text=f"Dominant emotion: {dominant_emotion.capitalize()}")

                    # Display an image based on the detected emotion
                    # if dominant_emotion in self.emotion_images:
                    #     img_path = self.emotion_images[dominant_emotion]
                    #     img = Image.open(img_path)
                    #     img = ImageTk.PhotoImage(img)
                    #     self.image_label.config(image=img)
                    #     self.image_label.place(x=50,y=100)
                    #     self.image_label.image = img  # Keep a reference to avoid garbage collection

                    # リストをクリアして次のデータ収集の準備
                    self.emotion_history.clear()
                    self.frames_since_last_update = 0
                    self.last_update_time = time.time()
        if self.mirror:
            self.mirror.update()

        self.root.after(100, self.update)
        
    def get_emotion(self):
        return self.dominant_emotion

    def get_image_path_for_emotion(self, emotion):
        # 感情に対応する画像のパスを取得するメソッド
        return self.emotion_images.get(emotion, 'img/neutral.png')  # デフォルトの画像へのパスを設定

    def second_window_closed(self):
        self.second_window = None  # セカンドウィンドウの変数をリセット
        
    def show_img(self, win_id):
        if not self.is_second_window:
            win_id = win_id
            alter_img_path = self.show_random_file(win_id)
            original_img = Image.open(alter_img_path)

            # リサイズしたいサイズを指定
            target_size = (400, 300)
            resized_img = original_img.resize(target_size)

            alter_img = ImageTk.PhotoImage(resized_img)
            self.alter_image_label.config(text=f"Do not be so nervous!")

            # angryの閾値を超えているかどうかを確認
            if win_id == 1:
                self.alter_image_label = tk.Label(self.root)
                self.alter_image_label.configure(image=alter_img)
                self.alter_image_label.place(x=380, y=80)
                self.alter_image_label.image = alter_img
                self.is_second_window = True
            elif win_id == 2:
                self.alter_image_label = tk.Label(self.root)
                self.alter_image_label.configure(image=alter_img)
                self.alter_image_label.place(x=380, y=80)
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
    app1 = FERApp(root)
    
    def exit_app():
        root.destroy()
        
    root.mainloop()

if __name__ == "__main__":
    main()