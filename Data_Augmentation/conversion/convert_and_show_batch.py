import os
import cv2
import numpy as np
from PIL import Image

# 淘汰了，不用这个

def convert_coordinates_sj2yolo(box, image_width, image_height):
    points = np.array([(int(box[i] * image_width), int(box[i + 1] * image_height)) for i in range(0, 8, 2)], dtype=np.int32)
    x, y, w, h = cv2.boundingRect(points)
    center_x = x + w / 2
    center_y = y + h / 2
    width = w
    height = h * 2

    # 归一化
    center_x /= image_width
    center_y /= image_height
    width /= image_width
    height /= image_height

    return center_x, center_y, width, height


def read_sj_annotation(annotation_path, image_width, image_height):
    annotations = []
    with open(annotation_path, "r") as f:
        for line in f:
            class_idx, *box = map(float, line.strip().split())
            center_x, center_y, width, height = convert_coordinates_sj2yolo(box, image_width, image_height)
            annotations.append((int(class_idx), center_x, center_y, width, height))
    return annotations


def draw_bbox(image, annotations):
    for annotation in annotations:
        class_idx, center_x, center_y, width, height = annotation
        img_height, img_width = image.shape[:2]
        x = int((center_x - width / 2) * img_width)
        y = int((center_y - height / 2) * img_height)
        w = int(width * img_width)
        h = int(height * img_height)

        color = (0, 255, 0)  # bbox颜色为绿色
        thickness = 2
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
        text = f"Class {class_idx}"
        font_scale = 0.8
        font_thickness = 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        cv2.rectangle(image, (x, y - text_size[1]), (x + text_size[0], y), color, -1)
        cv2.putText(image, text, (x, y), font, font_scale, (0, 0, 0), font_thickness, lineType=cv2.LINE_AA)


def main(image_folder, annotation_folder):
    image_files = sorted(os.listdir(image_folder))
    annotation_files = sorted(os.listdir(annotation_folder))

    for image_file, annotation_file in zip(image_files, annotation_files):
        image_path = os.path.join(image_folder, image_file)
        annotation_path = os.path.join(annotation_folder, annotation_file)

        image = Image.open(image_path)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        img_height, img_width = image.shape[:2]
        annotations = read_sj_annotation(annotation_path, img_width, img_height)

        draw_bbox(image, annotations)

        cv2.imshow("YOLO Annotation Visualization", image)

        key = cv2.waitKey(0)
        if key == ord("q"):  # 按下 "q" 键退出
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    image_folder = r"G:\Radar_datasets\by_sentinel\images\train"  # 图像文件夹路径
    annotation_folder = r"G:\Radar_datasets\by_sentinel\labels\train"  # 上交格式标注文件夹路径
    main(image_folder, annotation_folder)
