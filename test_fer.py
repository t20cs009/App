from fer import FER
import matplotlib.pyplot as plt

image = plt.imread('img/kattu2.jpg')

emo_detector = FER(mtcnn=True)
dominant_emotion, emotion_score = emo_detector.top_emotion(image)
plt.imshow(image)
print(dominant_emotion, emotion_score)