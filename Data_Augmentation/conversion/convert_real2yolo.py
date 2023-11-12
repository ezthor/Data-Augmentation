import os
from PIL import Image


# 将labelme的json转为yolo

def convert_to_yolo_format(images_folder, labels_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [file for file in os.listdir(images_folder) if file.endswith('.jpg')]

    for image_file in image_files:
        image_name = image_file.replace('.jpg', '')
        label_file = image_name + '.txt'
        label_file_path = os.path.join(labels_folder, label_file)

        with open(label_file_path, 'r') as file:
            lines = file.readlines()

        yolo_annotations = []
        image_path = os.path.join(images_folder, image_file)
        img = Image.open(image_path)
        img_width, img_height = img.size

        for line in lines:
            class_id, center_x, center_y, width, height = map(float, line.strip().split())


            yolo_class_id = int(class_id)
            yolo_center_x = center_x / img_width
            yolo_center_y = center_y / img_height
            yolo_width = width / img_width
            yolo_height = height / img_height

            yolo_annotations.append(
                f"{yolo_class_id} {yolo_center_x:.6f} {yolo_center_y:.6f} {yolo_width:.6f} {yolo_height:.6f}\n")

        output_label_folder = os.path.join(output_folder, 'labels')
        os.makedirs(output_label_folder, exist_ok=True)
        output_label_file_path = os.path.join(output_label_folder, label_file)
        with open(output_label_file_path, 'w') as output_file:
            output_file.writelines(yolo_annotations)

    print("Conversion to YOLO format completed!")


# 使用例子:
base_folder = r'G:\Radar_datasets\yolo\second_period\datasets'
color = "red"
start_id = 1
end_id = 5
'''
# 单个文件夹进行操作
images_folder = r'G:\Radar_datasets\yolo\second_period\datasets\blue1\images\train'  # Replace with the path to your "images" folder
labels_folder = r'G:\Radar_datasets\yolo\second_period\datasets\blue1\labels\train'  # Replace with the path to your "labels" folder
output_folder = r'G:\Radar_datasets\yolo\second_period\datasets\blue1\labels_yolo\train'  # Replace with the path to your desired output folder
'''
for id in range(start_id, end_id+1):
    images_folder = os.path.join(base_folder, f'{color}{id}', "images", "train")
    labels_folder = os.path.join(base_folder, f'{color}{id}', "labels", "train")
    output_folder = os.path.join(base_folder, f'{color}{id}', "labels_yolo", "train")
    convert_to_yolo_format(images_folder, labels_folder, output_folder)
