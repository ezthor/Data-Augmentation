import os
import cv2
import numpy as np
from PIL import Image

# 将目标文件夹下yolo格式图片的标注信息可视化,n下一张，p上一张，d删除图片和标注

# 函数：读取类YOLO格式的标注文件并解析bbox信息
def read_yolo_annotation(annotation_path, img_width, img_height):
    annotations = []
    with open(annotation_path, "r") as f:
        for line in f:
            class_idx, center_x, center_y, width, height = map(float, line.strip().split())
            x = int((center_x - width / 2) * img_width)
            y = int((center_y - height / 2) * img_height)
            w = int(width * img_width)
            h = int(height * img_height)

            # 确保bbox不超过图像边界
            x1 = max(0, x)
            y1 = max(0, y)
            x2 = min(img_width, x + w)
            y2 = min(img_height, y + h)

            annotations.append((int(class_idx), x1, y1, x2 - x1, y2 - y1))
    return annotations


# 函数：在图像上绘制bbox和类别标签
def draw_bbox(image, annotations):
    for annotation in annotations:
        class_idx, x, y, w, h = annotation
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


# 主函数
# 主函数
def main(image_folder, annotation_folder):
    image_files = sorted(os.listdir(image_folder))
    annotation_files = sorted(os.listdir(annotation_folder))
    idx = 0

    while idx < len(image_files):
        image_file = image_files[idx]
        annotation_file = annotation_files[idx]

        image_path = os.path.join(image_folder, image_file)
        annotation_path = os.path.join(annotation_folder, annotation_file)

        print("Image Path:", image_path)  # 添加这行进行调试

        try:
            image = Image.open(image_path)
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            if image is None:
                print("Failed to read image:", image_path)
                idx += 1
                continue

            img_height, img_width = image.shape[:2]

            annotations = read_yolo_annotation(annotation_path, img_width, img_height)
            draw_bbox(image, annotations)

            cv2.imshow("YOLO Annotation Visualization", image)

            key = cv2.waitKey(0)
            if key == ord("q"):  # 按下 "q" 键退出
                break
            elif key == ord("n"):  # 按下 "n" 键查看下一张图像
                idx += 1
            elif key == ord("p") and idx > 0:  # 按下 "p" 键查看上一张图像
                idx -= 1
            elif key == ord("d"):  # 按下 "d" 键删除图像和标注文件
                os.remove(image_path)
                os.remove(annotation_path)
                print("Deleted:", image_path, annotation_path)
                del image_files[idx]
                del annotation_files[idx]
        except Exception as e:
            print("Error occurred while processing image:", image_path)
            print("Error message:", str(e))
            idx += 1
            continue

    cv2.destroyAllWindows()


if __name__ == "__main__":
    image_folder = r"G:\道路危害大赛\数据集\train1112_mix_single_cls\class0\train\images"  # 图像文件夹路径
    annotation_folder = r"G:\道路危害大赛\数据集\train1112_mix_single_cls\class0\train\labels"  # 标注文件夹路径
    main(image_folder, annotation_folder)