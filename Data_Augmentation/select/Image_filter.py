import os
import shutil

# 初筛图片，只保留有目标装甲板的图片
# TODO:详细文档

def extract_armor5_images_and_labels(dataset_folder, output_folder):
    images_train_folder = os.path.join(dataset_folder, 'images', 'train')
    images_val_folder = os.path.join(dataset_folder, 'images', 'val')
    labels_train_folder = os.path.join(dataset_folder, 'labels', 'train')
    labels_val_folder = os.path.join(dataset_folder, 'labels', 'val')

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 处理train集中的数据
    extract_images_and_labels(images_train_folder, labels_train_folder, os.path.join(output_folder, 'train'))

    # 处理val集中的数据
    extract_images_and_labels(images_val_folder, labels_val_folder, os.path.join(output_folder, 'val'))

    print("提取完成！")


def extract_images_and_labels(images_folder, labels_folder, output_folder):
    # 获取文件夹中所有的图片文件
    image_files = [file for file in os.listdir(images_folder) if file.endswith('.jpg')]

    # 处理每个图片文件
    for image_file in image_files:
        image_name = image_file.replace('.jpg', '')
        label_file = image_name + '.txt'
        label_file_path = os.path.join(labels_folder, label_file)

        # 读取标签文件内容
        with open(label_file_path, 'r') as file:
            lines = file.readlines()

        # 检查标签文件是否包含五号装甲板类别
        has_armor5 = any(line.startswith('7 ') or line.startswith('10 ') for line in lines)

        if has_armor5:
            # 提取对应的图片文件
            image_path = os.path.join(images_folder, image_file)

            # 将图像复制到输出文件夹
            output_image_folder = os.path.join(output_folder, 'images')
            os.makedirs(output_image_folder, exist_ok=True)
            shutil.copy(image_path, output_image_folder)

            # 将标签文件复制到输出文件夹
            output_label_folder = os.path.join(output_folder, 'labels')
            os.makedirs(output_label_folder, exist_ok=True)
            shutil.copy(label_file_path, output_label_folder)


# 示例用法:
dataset_folder = r'G:\道路危害大赛\数据集\train1112_mix'  # 替换为实际的数据集文件夹路径
output_folder = r'G:\道路危害大赛\数据集\train1112_mix_single_cls\class7'  # 替换为所需的输出文件夹路径
extract_armor5_images_and_labels(dataset_folder, output_folder)
