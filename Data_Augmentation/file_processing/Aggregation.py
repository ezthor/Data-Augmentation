import os
import shutil

# 将目标文件夹下的所有文件夹里的图片和标注复制到一个all文件夹下的images文件夹和labels文件夹，注意目标文件夹下的所有文件夹都需要用yolo格式的文件结构

def move_files(source_folder, destination_folder):
    # 获取源文件夹中的所有子文件夹名（red1到red5，blue1到blue5）
    subfolders = [folder for folder in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, folder))]

    # 遍历每个子文件夹
    for subfolder in subfolders:
        subfolder_path = os.path.join(source_folder, subfolder)
        images_folder = os.path.join(subfolder_path, 'images', train)
        labels_folder = os.path.join(subfolder_path, 'labels', train)

        # 移动图片文件
        for image_file in os.listdir(images_folder):
            image_source = os.path.join(images_folder, image_file)
            image_destination = os.path.join(destination_folder, 'images', train, image_file)
            shutil.move(image_source, image_destination)

        # 移动标注文件
        for label_file in os.listdir(labels_folder):
            label_source = os.path.join(labels_folder, label_file)
            label_destination = os.path.join(destination_folder, 'labels', train, label_file)
            shutil.move(label_source, label_destination)

if __name__ == "__main__":
    datasets_folder = r"G:\计算机视觉课\实验\实验2\data\split_folder"  # 替换为datasets文件夹的路径
    all_folder = r"G:\计算机视觉课\实验\实验2\data\test"  # 替换为all文件夹的路径

    # 创建all文件夹及其子文件夹（images/train和labels/train）
    os.makedirs(os.path.join(all_folder, 'images', 'train'), exist_ok=True)
    os.makedirs(os.path.join(all_folder, 'labels', 'train'), exist_ok=True)
    flag = 0 # 如果images下有train文件夹，flag置1
    if flag:
        train = 'train'
    else:
        train = ''

    move_files(datasets_folder, all_folder)
    print("移动完成！")
