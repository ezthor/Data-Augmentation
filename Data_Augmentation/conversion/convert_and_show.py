import os
import cv2
import numpy as np
from PIL import Image

# 不用这个

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


def main(image_path, annotation_path):
    image = Image.open(image_path)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    img_height, img_width = image.shape[:2]
    annotations = read_sj_annotation(annotation_path, img_width, img_height)

    draw_bbox(image, annotations)

    cv2.imshow("YOLO Annotation Visualization", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    image_path = r"G:\Radar_datasets\by_sentinel\images\train\Image_20230330203219587.jpg"  # 图像路径
    annotation_path = r"G:\Radar_datasets\by_sentinel\labels\train\Image_20230330203219587.txt"  # 上交格式标注文件路径
    main(image_path, annotation_path)
