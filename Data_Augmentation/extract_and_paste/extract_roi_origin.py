import os
import shutil
from PIL import Image

# 提取出来的标注信息用原始像素值存储

# 每次提取id号
def extract_armor5_cars(images_folder, labels_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取images文件夹中所有的图片文件
    image_files = [file for file in os.listdir(images_folder) if file.endswith('.jpg')]

    # 处理每个图片文件
    for image_file in image_files:
        image_name = image_file.replace('.jpg', '')
        label_file = image_name + '.txt'
        label_file_path = os.path.join(labels_folder, label_file)

        # 读取标签文件内容
        with open(label_file_path, 'r') as file:
            lines = file.readlines()

        # 记录每辆车的装甲板标注信息
        cars_with_armor5 = []
        img_width = 0
        img_height = 0
        # 处理标签文件，检查是否有装甲板与车辆有重叠
        for line in lines:
            class_id, center_x, center_y, width, height = map(float, line.strip().split())

            # 如果是车辆
            if class_id == 0:
                img = Image.open(os.path.join(images_folder, image_file))
                img_width, img_height = img.size
                # 记录了car的左上角和右下角的真实像素值坐标
                car_x_min = int((center_x - width / 2) * img_width)
                car_y_min = int((center_y - height / 2) * img_height)
                car_x_max = int((center_x + width / 2) * img_width)
                car_y_max = int((center_y + height / 2) * img_height)

                # 检查是否有与车辆有重叠的五号装甲板
                for other_line in lines:
                    other_class_id, other_center_x, other_center_y, other_width, other_height = map(float,
                                                                                                    other_line.strip().split())
                    if other_class_id == id and other_line != line:
                        armor_center_x = int(other_center_x * img_width)
                        armor_center_y = int(other_center_y * img_height)

                        # 检查装甲板是否与车辆有重叠，并将装甲板信息添加到车辆的装甲板列表中
                        if (car_x_min <= armor_center_x <= car_x_max) and (car_y_min <= armor_center_y <= car_y_max):
                            cars_with_armor5.append((other_class_id, car_x_min, car_y_min, car_x_max, car_y_max,
                                                     armor_center_x, armor_center_y,
                                                     other_width * img_width, other_height * img_height))

        # 处理每辆车的装甲板信息
        # 获取图片的绝对路径
        image_path = os.path.join(images_folder, image_file)

        # 打开图片
        img = Image.open(image_path)

        # 处理每辆车的截图信息
        roi_x_min = 0
        roi_y_min = 0
        output_image_folder = os.path.join(output_folder, 'images', 'train')
        os.makedirs(output_image_folder, exist_ok=True)

        for idx, car_info in enumerate(cars_with_armor5):
            class_id, car_x_min, car_y_min, car_x_max, car_y_max, armor_center_x, armor_center_y, armor_width, armor_height = car_info

            # 打开图片并裁剪出截取的区域
            if idx == 0 and car_x_min != 0:  # 只处理第一行车辆信息
                # 计算中心点不变两倍长宽的ROI区域
                center_x = (car_x_min + car_x_max) // 2
                center_y = (car_y_min + car_y_max) // 2
                roi_width = (car_x_max - car_x_min) * 2
                roi_height = (car_y_max - car_y_min) * 2

                # 考虑图像边界情况
                roi_x_min = max(center_x - roi_width // 2, 0)
                roi_y_min = max(center_y - roi_height // 2, 0)
                roi_x_max = min(center_x + roi_width // 2, img_width)
                roi_y_max = min(center_y + roi_height // 2, img_height)

                # 打开图片并裁剪出截取的区域
                cropped_img = img.crop((roi_x_min, roi_y_min, roi_x_max, roi_y_max))

                # 保存截取的图片到输出文件夹
                output_image_name = f"{image_name}_{color}{id - flag * 5}.jpg"  # 修改图片名为"_red1.jpg"
                output_image_path = os.path.join(output_image_folder, output_image_name)
                cropped_img.save(output_image_path)
                # 创建装甲板标注文件并写入装甲板信息
        # 如果有五号车
        if cars_with_armor5:
            output_label_folder = os.path.join(output_folder, 'labels', 'train')
            os.makedirs(output_label_folder, exist_ok=True)
            output_label_file_name = f"{image_name}_{color}{id - flag * 5}.txt"
            output_label_file_path = os.path.join(output_label_folder, output_label_file_name)
            with open(output_label_file_path, 'w') as output_file:
                for armor_info in cars_with_armor5:
                    class_id, car_x_min, car_y_min, car_x_max, car_y_max, armor_center_x, armor_center_y, armor_width, armor_height = armor_info
                    # 只保存装甲板
                    output_file.write(
                        f"{class_id} {int(armor_center_x - roi_x_min)} {int(armor_center_y - roi_y_min)} {int(armor_width)} {int(armor_height)}\n")

    print("截取和标签转换完成！")


# args:
images_folder = r'G:\Radar_datasets\yolo\after_filter\train\images'  # 替换为实际的images/train文件夹路径
labels_folder = r'G:\Radar_datasets\yolo\after_filter\train\labels'  # 替换为实际的labels/train文件夹路径

color = "red"
flag = 0
# 单次使用

# 提取哪一号车
id = 10
output_folder = r'G:\Radar_datasets\yolo\second_period\datasets\red3'  # 替换为所需的输出文件夹路径
extract_armor5_cars(images_folder, labels_folder, output_folder)
'''
# 全部提取
output_base_folder = r'G:\Radar_datasets\yolo\second_period\datasets'  # 替换为所需的输出文件夹路径,最后不用加/
for id in range(6, 11):
    if id <= 5:
        color = "red"
        flag = 0
    else:
        color = "blue"
        flag = 1
    output_folder = os.path.join(output_base_folder, f'{color}{id - flag * 5}')
    os.makedirs(output_folder, exist_ok=True)
    extract_armor5_cars(images_folder, labels_folder, output_folder)
'''