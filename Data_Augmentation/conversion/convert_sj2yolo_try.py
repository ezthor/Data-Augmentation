import os
import cv2
import numpy as np

# 将上交格式转为yolo，不记得能不能跑了，不能用convert4points那个

def convert_coordinates(box, image_width, image_height):
    points = np.array([(int(box[i] * image_width), int(box[i + 1] * image_height)) for i in range(0, 8, 2)], dtype=np.int32)


    # 计算最小外接矩形的外接矩形
    x, y, w, h = cv2.boundingRect(points)
    center_x = x + w / 2
    center_y = y + h / 2

    # 将宽度和高度归一化
    width = w
    height = h * 2

    return center_x, center_y, width, height


def normalize_coordinates(box, image_width, image_height):
    # 归一化最小外接矩形数据并转换为YOLO格式
    center_x = box[0] / image_width
    center_y = box[1] / image_height
    width = box[2] / image_width
    height = box[3] / image_height

    return center_x, center_y, width, height


def convert_annotation(image_folder, annotation_folder, output_folder, class_id):
    os.makedirs(output_folder, exist_ok=True)
    image_files = os.listdir(image_folder)

    for image_file in image_files:
        # 读取图片
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)
        image_height, image_width, _ = image.shape

        # 将图片文件后缀改为txt
        image_name = os.path.splitext(image_file)[0]
        annotation_file = image_name + ".txt"
        annotation_path = os.path.join(annotation_folder, annotation_file)

        if not os.path.exists(annotation_path):
            continue

        # 读取上交格式标注数据
        with open(annotation_path, 'r') as f:
            lines = f.readlines()

        # 遍历标注数据并进行转换
        yolo_annotations = []
        for line in lines:
            data = line.strip().split()
            class_num = int(data[0])
            if class_num == class_id:
                box = list(map(float, data[1:]))
                center_x, center_y, width, height = convert_coordinates(box, image_width, image_height)
                normalized_data = normalize_coordinates((center_x, center_y, width, height), image_width, image_height)
                yolo_annotation = f"{class_id} {' '.join(map(str, normalized_data))}\n"
                yolo_annotations.append(yolo_annotation)

        # 将转换后的标注写入新的标注文件
        if yolo_annotations:
            output_path = os.path.join(output_folder, annotation_file)
            with open(output_path, 'w') as f:
                f.writelines(yolo_annotations)


if __name__ == "__main__":
    image_folder_path = r"G:\Radar_datasets\by_sentinel\images\train"
    annotation_folder_path = r"G:\Radar_datasets\by_sentinel\labels\train"
    output_folder_path = r"G:\Radar_datasets\by_sentinel\labels_new\train"
    class_id_to_convert = 0

    convert_annotation(image_folder_path, annotation_folder_path, output_folder_path, class_id_to_convert)
