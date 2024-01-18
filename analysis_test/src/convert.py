import os
from PIL import Image
import numpy as np

def grayscale_to_rgb(image_path):
    # グレースケール画像を開く
    grayscale_image = Image.open(image_path).convert("L")

    # グレースケール画像をRGB形式に変換
    rgb_image = Image.merge("RGB", (grayscale_image, grayscale_image, grayscale_image))

    # 画像をNumPy配列に変換
    image_array = np.array(rgb_image)

    return image_array

def process_and_save_images(input_dir, output_dir):
    # 入力ディレクトリ内の全てのファイルを取得
    file_list = os.listdir(input_dir)

    # ファイルの順序を取得
    sorted_file_list = sorted(file_list)

    for idx, file_name in enumerate(sorted_file_list):
        # ファイルの絶対パス
        file_path = os.path.join(input_dir, file_name)

        # グレースケール画像をRGB形式に変換
        colorized_image_array = grayscale_to_rgb(file_path)

        # NumPy配列をImageオブジェクトに変換
        colorized_image = Image.fromarray(colorized_image_array)

        # 出力先のファイルパス
        output_path = os.path.join(output_dir, f"{idx + 1}.jpg")

        # 画像を保存
        colorized_image.save(output_path)

# 例: グレースケール画像をRGB形式に変換して保存（入力ディレクトリと出力ディレクトリのパスを指定）
input_directory = 'C:/Users/GOLAB/Desktop/t20cs009/logi/App/analysis_test/img/fear'
output_directory = 'C:/Users/GOLAB/Desktop/t20cs009/logi/App/analysis_test/img/fea_1'

process_and_save_images(input_directory, output_directory)
