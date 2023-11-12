import os
import random
from PIL import Image


# 将roi图粘贴到原图上
# TODO: 详细文档


def check_overlap(rect1, rect2):
    # 检查两个矩形是否有重叠
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)


def overlay_images(bg_img, fg_img, x, y):
    # 在背景图上覆盖前景图
    bg_img.paste(fg_img, (int(x), int(y)), None)  # 将None作为mask传入


def convert_bbox_to_yolo(bbox, img_width, img_height):
    # 将标注框的坐标转换为Yolo格式
    class_id, x, y, w, h = bbox
    x_center = x + w / 2
    y_center = y + h / 2
    yolo_x = x_center / img_width
    yolo_y = y_center / img_height
    yolo_w = w / img_width
    yolo_h = h / img_height
    return f"{class_id} {yolo_x} {yolo_y} {yolo_w} {yolo_h}"


def main(original_folder, original_annotation_folder, roi_folder, roi_annotation_folder, output_folder, overlap_shift):
    original_images = os.listdir(original_folder)
    roi_images = os.listdir(roi_folder)
    random.shuffle(roi_images)  # 随机洗牌截图列表，确保每张原图只粘贴一张截图

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for original_image_file in original_images:
        # 处理每张原图
        original_image_path = os.path.join(original_folder, original_image_file)
        original_annotation_path = os.path.join(original_annotation_folder, original_image_file.replace(".jpg", ".txt"))
        output_image_path = os.path.join(output_folder, original_image_file)
        output_annotation_path = os.path.join(output_folder, original_image_file.replace(".jpg", ".txt"))

        # original_image = Image.open(original_image_path)
        # original_image = original_image.convert("RGB")  # 确保图像模式为RGB

        # debug
        try:
            original_image = Image.open(original_image_path)
            original_image = original_image.convert("RGB")
        except Exception as e:
            print(f"Error loading image: {original_image_file}, Error: {e}")
            continue
        # debug

        with open(original_annotation_path, 'r') as f:
            original_annotations = f.readlines()

        # 只选择截图列表中的第一张截图进行处理
        roi_image_file = roi_images.pop(0)
        roi_images.append(roi_image_file)  # 将已使用的截图放回截图列表末尾，确保所有截图都能使用
        roi_image_path = os.path.join(roi_folder, roi_image_file)
        roi_annotation_path = os.path.join(roi_annotation_folder, roi_image_file.replace(".jpg", ".txt"))

        roi_image = Image.open(roi_image_path)
        roi_image = roi_image.convert("RGB")  # 确保图像模式为RGB

        with open(roi_annotation_path, 'r') as f:
            roi_annotations = f.readlines()

        success = False
        for _ in range(len(original_annotations)):
            # 处理每次贴图
            while True:
                x = random.randint(0, original_image.width - roi_image.width)
                y = random.randint(0, original_image.height - roi_image.height)
                # 取即将贴的位置的左上角，左上角范围x留了截图的宽，y留了截图的长，用roi_rect存，存的都是原始像素值，在新图片的坐标系下
                roi_rect = [x, y, roi_image.width, roi_image.height]
                # 默认是没有覆盖的
                overlap = False
                # 对所有原始标注的边框进行检查
                for annotation in original_annotations:
                    # 原始标注是yolo格式，要转换为真实像素值
                    class_id, x, y, w, h = map(float, annotation.split())
                    x *= original_image.width
                    y *= original_image.height
                    w *= original_image.width
                    h *= original_image.height
                    # 用rect存遍历的所有原始bbox
                    rect = [x, y, w, h]
                    # 如果检测到重叠，flag变true，退出检验循环
                    if check_overlap(rect, roi_rect):
                        overlap = True
                        break
                # 如果没有重叠，就退出随机取点过程，进入覆盖过程，否则回到随机取点过程
                if not overlap:
                    break

            overlay_images(original_image, roi_image, roi_rect[0], roi_rect[1])

            with open(output_annotation_path, 'w') as f_out:
                for annotation in original_annotations:
                    f_out.write(annotation)
                for annotation in roi_annotations:
                    # 截图的x，y是中心点的x，y
                    class_id, x, y, w, h = map(float, annotation.split())
                    # roi_rect[0]是粘贴位置的左上角新图坐标系下的x真实像素值，应该是这个加上在截图中相对的x值才是新的边框位置
                    x = (x + roi_rect[0]) / original_image.width
                    y = (y + roi_rect[1]) / original_image.height
                    w = w / original_image.width
                    h = h / original_image.height
                    new_annotation = f"{class_id} {x} {y} {w} {h}\n"
                    f_out.write(new_annotation)

            success = True
            print(f"Processed image: {original_image_file}, ROI image: {roi_image_file}")
            break

        if not success:
            print(f"Failed to process ROI image: {roi_image_file}")

        original_image.save(output_image_path)


if __name__ == "__main__":
    original_folder = r"G:\Radar_datasets\yolo\paste_red5turn1\images"
    original_annotation_folder = r"G:\Radar_datasets\yolo\paste_red5turn1\labels"
    roi_folder = r"G:\Radar_datasets\yolo\extract_try_roi_blue5\images\train"
    roi_annotation_folder = r"G:\Radar_datasets\yolo\extract_try_roi_blue5\labels\train"
    output_folder = r"G:\Radar_datasets\yolo\paste_red5turn1_blue5turn1"
    overlap_shift = 5  # 根据需要调整重叠时的平移值

    main(original_folder, original_annotation_folder, roi_folder, roi_annotation_folder, output_folder, overlap_shift)
