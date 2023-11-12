import os
import random
import shutil

# 按比例划分train和val

def split_train_val(source_images_folder, source_labels_folder, val_ratio):
    # 创建val文件夹，如果不存在
    val_images_folder = os.path.join(source_images_folder, 'val')
    val_labels_folder = os.path.join(source_labels_folder, 'val')
    os.makedirs(val_images_folder, exist_ok=True)
    os.makedirs(val_labels_folder, exist_ok=True)

    # 获取源文件夹中的所有图片文件名
    image_files = [file for file in os.listdir(source_images_folder) if file.endswith('.jpg')]

    # 获取所有图片的序号列表
    num_samples = len(image_files)
    all_indices = list(range(num_samples))

    # 计算验证集样本数
    num_val_samples = int(num_samples * val_ratio)

    # 随机抽取验证集样本的序号
    val_indices = random.sample(all_indices, num_val_samples)

    # 将图片和标注分配到train或val文件夹中
    for i, image_file in enumerate(image_files):
        label_file = image_file.replace('.jpg', '.txt')
        image_source_path = os.path.join(source_images_folder, image_file)
        label_source_path = os.path.join(source_labels_folder, label_file)

        if i in val_indices:
            image_destination_path = os.path.join(val_images_folder, image_file)
            label_destination_path = os.path.join(val_labels_folder, label_file)
        else:
            image_destination_path = os.path.join(source_images_folder, image_file)
            label_destination_path = os.path.join(source_labels_folder, label_file)

        # 移动文件
        shutil.move(image_source_path, image_destination_path)
        shutil.move(label_source_path, label_destination_path)

if __name__ == "__main__":
    images_folder = r"G:\Radar_datasets\by_sentinel\images\train"  # 替换为images/train文件夹的路径
    labels_folder = r"G:\Radar_datasets\by_sentinel\labels\train"  # 替换为labels/train文件夹的路径
    val_ratio = 0.1  # 验证集所占的比例，这里设为0.1表示10%

    split_train_val(images_folder, labels_folder, val_ratio)
    print("分割完成！")
