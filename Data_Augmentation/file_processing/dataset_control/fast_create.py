import os
import shutil
from sklearn.model_selection import train_test_split

def gather_datasets(parent_folder, output_folder, dataset_names, test_size):
    # 收集所有的图片和标签文件
    all_images = []
    all_labels = []
    for dataset_name in dataset_names:
        images_folder = os.path.join(parent_folder, dataset_name, 'images')
        labels_folder = os.path.join(parent_folder, dataset_name, 'labels')
        for image_file in os.listdir(images_folder):
            all_images.append(os.path.join(images_folder, image_file))
            all_labels.append(os.path.join(labels_folder, image_file.replace('.jpg', '.txt')))
    # 划分训练集和验证集
    train_images, val_images, train_labels, val_labels = train_test_split(all_images, all_labels, test_size=test_size, random_state=42)
    # 复制文件
    for dataset_type, image_files, label_files in [('train', train_images, train_labels), ('val', val_images, val_labels)]:
        for image_file, label_file in zip(image_files, label_files):
            if not os.path.exists(os.path.join(output_folder, 'images', dataset_type)):
                os.makedirs(os.path.join(output_folder, 'images', dataset_type))
            if not os.path.exists(os.path.join(output_folder, 'labels', dataset_type)):
                os.makedirs(os.path.join(output_folder, 'labels', dataset_type))
            shutil.copy(image_file, os.path.join(output_folder, 'images', dataset_type, os.path.basename(image_file)))
            shutil.copy(label_file, os.path.join(output_folder, 'labels', dataset_type, os.path.basename(label_file)))

dataset_names = ['dataset1', 'dataset2']  # 你想要整合的数据块的名称列表
parent_folder = '/path/to/your/datasets'  # 改为你的父文件夹路径
output_folder = '/path/to/your/output'  # 改为你想要输出的文件夹路径
test_size = 0.2  # 这边是划分训练和验证集的比例，你可以自己调整
gather_datasets(parent_folder, output_folder, dataset_names, test_size)