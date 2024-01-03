import cv2
import tkinter as tk
from PIL import Image, ImageTk
from fer import FER

class FERApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FER Analysis")

        self.video_source = 0  # Change this if needed for a different webcam

        self.fer = FER(mtcnn=True)

        self.vid = cv2.VideoCapture(self.video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()

        self.btn_quit = tk.Button(root, text="Quit", command=self.quit)
        self.btn_quit.pack()

        self.update()

    def update(self):
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

        self.root.after(15, self.update)

    def quit(self):
        self.vid.release()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = FERApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
