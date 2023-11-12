import os
from PIL import Image

# 用于处理某个图片文件夹和文本文件夹下的同名图片和标注
# 原始图片用yolo格式存储 车为0号 红1-5为类1-5，蓝1-5为6-10，如有其它id也行
#  extract_armor5_cars函数将range范围内的符合id的车作为初始轮廓，将宽高扩大两倍，并根据边界情况进行新轮廓限制，获得新roi截图四点坐标
# 用新截图roi四点坐标截图，将装甲板原始图的标注信息根据新截图左上角点进行转换后写入新标注信息
# 新图片和标注命名为原图名_红/蓝id
# 使用时确保原图是yolo格式，将图片文件夹路径和标注文件夹路径修改为自己路径，将range中参数改为自己要提取的id

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
                car_x_min = (center_x - width / 2) * img_width
                car_y_min = (center_y - height / 2) * img_height
                car_x_max = (center_x + width / 2) * img_width
                car_y_max = (center_y + height / 2) * img_height

                # 检查是否有与车辆有重叠的五号装甲板
                for other_line in lines:
                    other_class_id, other_center_x, other_center_y, other_width, other_height = map(float,
                                                                                                    other_line.strip().split())
                    if other_class_id == id and other_line != line:
                        armor_center_x = other_center_x * img_width
                        armor_center_y = other_center_y * img_height

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
        print("处理图片:" + image_path)
        # 处理每辆车的截图信息
        roi_x_min = 0
        roi_y_min = 0
        roi_width = 0
        roi_height = 0
        output_image_folder = os.path.join(output_folder, 'images', 'train')
        os.makedirs(output_image_folder, exist_ok=True)

        for idx, car_info in enumerate(cars_with_armor5):
            class_id, car_x_min, car_y_min, car_x_max, car_y_max, armor_center_x, armor_center_y, armor_width, armor_height = car_info

            # 打开图片并裁剪出截取的区域
            if idx == 0 and car_x_min != 0:  # 只处理第一行车辆信息
                # 计算中心点不变两倍长宽的ROI区域
                center_x = (car_x_min + car_x_max) / 2
                center_y = (car_y_min + car_y_max) / 2
                roi_width = (car_x_max - car_x_min) * 2
                roi_height = (car_y_max - car_y_min) * 2

                if roi_width == 0 or roi_height == 0:
                    continue

                # 考虑图像边界情况
                roi_x_min = max(center_x - roi_width // 2, 0)
                roi_y_min = max(center_y - roi_height // 2, 0)
                roi_x_max = min(center_x + roi_width // 2, img_width)
                roi_y_max = min(center_y + roi_height // 2, img_height)
                # 应该使用修正过的roi图像的参数，可能宽高改变了
                roi_width=roi_x_max-roi_x_min
                roi_height=roi_y_max-roi_y_min

                # 打开图片并裁剪出截取的区域
                cropped_img = img.crop((roi_x_min, roi_y_min, roi_x_max, roi_y_max))

                # 保存截取的图片到输出文件夹
                output_image_name = f"{image_name}_{color}{id-flag*5}.jpg"  # 修改图片名为"_red1.jpg"
                output_image_path = os.path.join(output_image_folder, output_image_name)
                cropped_img.save(output_image_path)
                # 创建装甲板标注文件并写入装甲板信息
        # 如果有五号车
        if cars_with_armor5:
            if roi_width == 0 or roi_height == 0:
                continue
            output_label_folder = os.path.join(output_folder, 'labels', 'train')
            os.makedirs(output_label_folder, exist_ok=True)
            output_label_file_name = f"{image_name}_{color}{id-flag*5}.txt"
            output_label_file_path = os.path.join(output_label_folder, output_label_file_name)
            with open(output_label_file_path, 'w') as output_file:
                for armor_info in cars_with_armor5:
                    class_id, car_x_min, car_y_min, car_x_max, car_y_max, armor_center_x, armor_center_y, armor_width, armor_height = armor_info
                    # 只保存装甲板
                    output_file.write(
                        f"{class_id} {(armor_center_x - roi_x_min) / roi_width} {(armor_center_y - roi_y_min) / roi_height} {armor_width / roi_width} {armor_height / roi_height}\n")

    print("截取和标签转换完成！")


# 主函数:
# 待修改params:
# 文件夹路径
images_folder = r'G:\Radar_datasets\extend_3\images\train'  # 替换为实际的images/train文件夹路径
labels_folder = r'G:\Radar_datasets\extend_3\labels\train'  # 替换为实际的labels/train文件夹路径
# 目标车辆颜色
color = "blue" #红车还是蓝车，约定红车编号为1-5，蓝车为6-10
# 如果要提取1到10的id，start为1.end为10
start_id=1
end_id=10
# 单次使用
'''
id = 3

output_folder = r'G:\Radar_datasets\yolo\second_period\datasets\red3'  # 替换为所需的输出文件夹路径
extract_armor5_cars(images_folder, labels_folder, output_folder)
'''
# 全部提取

flag=-1

output_base_folder = r'G:\Radar_datasets\extend_3'  # 替换为所需的输出文件夹路径,最后不用加/
for id in range(start_id, end_id+1):
    # 颜色自适应
    if id<=5:
        color="red"
    elif 5 < id <= 10:
        color="blue"
    # flag修改
    if color == "blue":
        flag = 1
    elif color == "red":
        flag = 0
    else:
        exit(-1)
    output_folder = os.path.join(output_base_folder, f'{color}{id}')
    os.makedirs(output_folder, exist_ok=True)
    extract_armor5_cars(images_folder, labels_folder, output_folder)
