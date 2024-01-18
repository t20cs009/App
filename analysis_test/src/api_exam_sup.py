from fer import FER
import os
import matplotlib.pyplot as plt

def analyze_emotions_in_folder(folder_path):
    # フォルダ内の全てのファイルを取得
    file_list = os.listdir(folder_path)

    # Emotion Detection結果を格納する変数
    total_analyzed = 0
    angry_count = 0

    # フォルダ内の各画像に対して検出を行う
    for file_name in file_list:
        # ファイルの絶対パス
        file_path = os.path.join(folder_path, file_name)

        # 画像を読み込む
        image = plt.imread(file_path)

        # Emotion Detectionを実行
        emotion_detector = FER(mtcnn=True)
        dominant_emotion, emotion_score = emotion_detector.top_emotion(image)

        # カウントを更新
        print(dominant_emotion)
        if dominant_emotion:
            total_analyzed += 1
        if dominant_emotion == 'surprise':
            angry_count += 1

    return total_analyzed, angry_count

# 例: フォルダ内の画像すべてに対してEmotion Detectionを実行
folder_path = 'C:/Users/GOLAB/Desktop/t20cs009/logi/App/analysis_test/img/sup_1'
total_analyzed, angry_count = analyze_emotions_in_folder(folder_path)

print(f"Total images analyzed: {total_analyzed}")
print(f"Total 'angry' emotions detected: {angry_count}")
