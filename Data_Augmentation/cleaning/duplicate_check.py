import os
import glob

# 检查目标文件夹下是否有重复的图片

def find_duplicate_images(folder_path):
    image_dict = {}
    for image_file in glob.glob(os.path.join(folder_path, '*.jpg')):  # 假设图片格式为jpg，你可以根据需要修改
        image_name = os.path.basename(image_file)
        if image_name in image_dict:
            image_dict[image_name].append(image_file)
        else:
            image_dict[image_name] = [image_file]

    duplicates_found = False
    for image_name, image_files in image_dict.items():
        if len(image_files) > 1:
            print(f"图片名'{image_name}'有以下重复文件:")
            for image_file in image_files:
                print(image_file)
            duplicates_found = True

    if not duplicates_found:
        print("未找到重复的图片文件.")

# 用法示例
folder_path = r"G:\Radar_datasets\yolo\second_period\radar_second_period\images\train"  # 将此处替换为你的文件夹路径
find_duplicate_images(folder_path)
