import os
import json

def labelme_to_yolo(labelme_json_file, output_file, class_mapping):
    with open(labelme_json_file, 'r') as f:
        labelme_data = json.load(f)

    image_width = labelme_data["imageWidth"]
    image_height = labelme_data["imageHeight"]

    with open(output_file, 'w') as f:
        for shape in labelme_data["shapes"]:
            class_label = shape["label"]
            class_id = class_mapping.get(class_label)
            if class_id is not None:
                points = shape["points"]

                # 计算边界框的中心坐标和宽高
                x_min = min(points, key=lambda x: x[0])[0]
                y_min = min(points, key=lambda x: x[1])[1]
                x_max = max(points, key=lambda x: x[0])[0]
                y_max = max(points, key=lambda x: x[1])[1]
                center_x = (x_min + x_max) / 2
                center_y = (y_min + y_max) / 2
                width = x_max - x_min
                height = y_max - y_min

                # 归一化坐标
                center_x /= image_width
                center_y /= image_height
                width /= image_width
                height /= image_height

                # 将结果写入YOLO格式文件
                f.write(f"{class_id} {center_x} {center_y} {width} {height}\n")


def process_folder(folder_path, output_folder, class_mapping):
    os.makedirs(output_folder, exist_ok=True)
    image_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        json_file = image_file.replace(".jpg", ".json")
        json_path = os.path.join(folder_path, json_file)

        if os.path.exists(json_path):
            output_file = os.path.join(output_folder, image_file.replace(".jpg", ".txt"))
            labelme_to_yolo(json_path, output_file, class_mapping)


if __name__ == "__main__":
    folder_path = r"G:\Radar_datasets\extend_3\3"  # 包含图片和JSON文件的文件夹路径
    output_folder = "G:\Radar_datasets\extend_3\labels"  # 输出的YOLO格式文件保存的文件夹路径
    class_mapping = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
                     "10": 10}  # 类别映射，根据您的实际类别进行修改

    process_folder(folder_path, output_folder, class_mapping)

