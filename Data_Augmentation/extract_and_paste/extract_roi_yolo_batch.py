import os
import shutil
from PIL import Image

# 批量提取roi图，把每一号的车的roi图都提取出来（单次的只提取一种车的，例如只提取红2，现在把所有循环一遍)
# 不对这玩意好像写错了用不了，用文件名没有batch的，也可以批量提取

def extract_armor5_cars(images_folder, labels_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [file for file in os.listdir(images_folder) if file.endswith('.jpg')]

    for image_file in image_files:
        image_name = image_file.replace('.jpg', '')
        label_file = image_name + '.txt'
        label_file_path = os.path.join(labels_folder, label_file)

        with open(label_file_path, 'r') as file:
            lines = file.readlines()

        cars_with_armor5 = []
        img_width, img_height = 0, 0

        for line in lines:
            class_id, center_x, center_y, width, height = map(float, line.strip().split())

            if class_id == 0:
                img = Image.open(os.path.join(images_folder, image_file))
                img_width, img_height = img.size
                car_x_min = int(center_x - width / 2)
                car_y_min = int(center_y - height / 2)
                car_x_max = int(center_x + width / 2)
                car_y_max = int(center_y + height / 2)

                for other_line in lines:
                    other_class_id, other_center_x, other_center_y, other_width, other_height = map(float,
                                                                                                    other_line.strip().split())
                    if other_class_id == 5 and other_line != line:
                        armor_center_x = int(other_center_x)
                        armor_center_y = int(other_center_y)

                        if (car_x_min <= armor_center_x <= car_x_max) and (car_y_min <= armor_center_y <= car_y_max):
                            cars_with_armor5.append((other_class_id, car_x_min, car_y_min, car_x_max, car_y_max,
                                                     armor_center_x, armor_center_y,
                                                     other_width, other_height))

        image_path = os.path.join(images_folder, image_file)
        img = Image.open(image_path)

        roi_x_min, roi_y_min = 0, 0
        roi_x_max, roi_y_max = 0, 0  # 初始化默认值
        output_image_folder = os.path.join(output_folder, 'images', 'train')
        os.makedirs(output_image_folder, exist_ok=True)

        for idx, car_info in enumerate(cars_with_armor5):
            class_id, car_x_min, car_y_min, car_x_max, car_y_max, armor_center_x, armor_center_y, armor_width, armor_height = car_info

            if idx == 0 and car_x_min != 0:
                center_x = (car_x_min + car_x_max) // 2
                center_y = (car_y_min + car_y_max) // 2
                roi_width = (car_x_max - car_x_min) * 2
                roi_height = (car_y_max - car_y_min) * 2

                roi_x_min = max(center_x - roi_width // 2, 0)
                roi_y_min = max(center_y - roi_height // 2, 0)
                roi_x_max = min(center_x + roi_width // 2, img_width)
                roi_y_max = min(center_y + roi_height // 2, img_height)

                if roi_x_min == roi_x_max or roi_y_min == roi_y_max or roi_x_max - roi_x_min == 0 or roi_y_max - roi_y_min == 0:
                    continue  # 跳过当前车辆信息的处理

                cropped_img = img.crop((roi_x_min, roi_y_min, roi_x_max, roi_y_max))

                output_image_name = f"{image_name}_red.jpg"
                output_image_path = os.path.join(output_image_folder, output_image_name)
                cropped_img.save(output_image_path)

        if cars_with_armor5:
            output_label_folder = os.path.join(output_folder, 'labels', 'train')
            os.makedirs(output_label_folder, exist_ok=True)
            output_label_file_name = f"{image_name}_red.txt"
            output_label_file_path = os.path.join(output_label_folder, output_label_file_name)
            with open(output_label_file_path, 'w') as output_file:
                for armor_info in cars_with_armor5:
                    class_id, car_x_min, car_y_min, car_x_max, car_y_max, armor_center_x, armor_center_y, armor_width, armor_height = armor_info
                    print(armor_center_x, roi_x_min, roi_x_max, roi_x_min, armor_center_y, roi_y_min, roi_y_max,
                          roi_y_min)
                    output_file.write(

                        f"{class_id} {((armor_center_x - roi_x_min) / (roi_x_max - roi_x_min)):.6f} {((armor_center_y - roi_y_min) / (roi_y_max - roi_y_min)):.6f} {((armor_width) / (roi_x_max - roi_x_min)):.6f} {((armor_height) / (roi_y_max - roi_y_min)):.6f}\n")

    print("截取和标签转换完成！")


# 用法:
images_folder = r'G:\Radar_datasets\extend_3\images\train'
labels_folder = r'G:\Radar_datasets\extend_3\labels\train'
output_base_folder = r'G:\Radar_datasets\extend_3'

for id in range(1, 11):
    output_folder = os.path.join(output_base_folder, f'try{id}')
    os.makedirs(output_folder, exist_ok=True)
    extract_armor5_cars(images_folder, labels_folder, output_folder)
