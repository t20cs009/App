import os
import random
import shutil

def copy_random_files(source_folder, destination_folder, num_files=100):
    # ソースディレクトリ内のファイルリストを取得
    file_list = os.listdir(source_folder)

    # ランダムにnum_files個のファイルを選択
    selected_files = random.sample(file_list, min(num_files, len(file_list)))

    # ディレクトリが存在しない場合は作成
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 選択されたファイルをコピー
    for file_name in selected_files:
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)
        shutil.copyfile(source_path, destination_path)

# 例: ランダムに100個のファイルを選択し別のフォルダに保存
source_directory = 'C:/Users/GOLAB/test/test/fear'
destination_directory = 'C:/Users/GOLAB/Desktop/t20cs009/logi/App/analysis_test/img/fear'

copy_random_files(source_directory, destination_directory, num_files=100)
