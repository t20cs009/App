import os
import shutil

def copy_files_with_name(source_dir, destination_dir, keyword):
    # ソースディレクトリ内のファイルを取得
    files = os.listdir(source_dir)

    # キーワードを含むファイルを抽出してコピー
    for file in files:
        if keyword in file:
            source_path = os.path.join(source_dir, file)
            destination_path = os.path.join(destination_dir, file)
            shutil.copy2(source_path, destination_path)
            print(f"コピー完了: {file}")

# 使用例
source_directory = 'C:/Users/GOLAB/Downloads/val_set/annotations'
destination_directory = 'C:/Users/GOLAB/Desktop/t20cs009/logi/App/analysis_test/annotations'
keyword_to_match = 'exp'

copy_files_with_name(source_directory, destination_directory, keyword_to_match)
