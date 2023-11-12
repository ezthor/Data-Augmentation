import os
import cv2
import numpy as np

# 将上交格式（四点标注）文件夹下图片可视化,n下一张，p上一张，d删除图片和标注

# 函数：读取类YOLO格式的标注文件并解析bbox信息
def read_yolo_annotation(annotation_path, img_width, img_height):
    annotations = []
    with open(annotation_path, "r") as f:
        for line in f:
            class_idx, x1, y1, x2, y2, x3, y3, x4, y4 = map(float, line.strip().split())
            x1 = int(x1 * img_width)
            y1 = int(y1 * img_height)
            x2 = int(x2 * img_width)
            y2 = int(y2 * img_height)
            x3 = int(x3 * img_width)
            y3 = int(y3 * img_height)
            x4 = int(x4 * img_width)
            y4 = int(y4 * img_height)

            annotations.append((int(class_idx), [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]))
    return annotations


# 函数：在图像上绘制bbox和类别标签
def draw_bbox(image, annotations):
    for annotation in annotations:
        fontFace = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (0, 255, 0)  # bbox颜色为绿色
        thickness = 2
        class_idx, points = annotation
        print(points)
        cv2.putText(image, "1", points[0], fontFace, fontScale, color, thickness)
        cv2.putText(image, "2", points[1], fontFace, fontScale, color, thickness)
        cv2.putText(image, "3", points[2], fontFace, fontScale, color, thickness)
        cv2.putText(image, "4", points[3], fontFace, fontScale, color, thickness)
        points = np.array(points, np.int32)
        points = points.reshape((-1, 1, 2))

        image = cv2.polylines(image, [points], isClosed=True, color=color, thickness=thickness)




# 主函数
def main(image_folder, annotation_folder):
    image_files = sorted(os.listdir(image_folder))

    current_index = 0

    while current_index < len(image_files):
        image_filename = image_files[current_index]
        image_name, image_ext = os.path.splitext(image_filename)
        annotation_filename = image_name + ".txt"

        image_path = os.path.join(image_folder, image_filename)
        annotation_path = os.path.join(annotation_folder, annotation_filename)

        if not os.path.isfile(annotation_path):
            print(f"Annotation not found for {image_filename}. Skipping...")
            current_index += 1
            continue

        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to read image: {image_path}")
                current_index += 1
                continue

            img_height, img_width, _ = image.shape
            annotations = read_yolo_annotation(annotation_path, img_width, img_height)
            draw_bbox(image, annotations)

            cv2.imshow("Annotated Image", image)
            print(annotation_path)
            key = cv2.waitKey(0)
            if key == ord("n"):  # 按下 "n" 键查看下一张图像
                current_index += 1
            elif key == ord("p") and current_index > 0:  # 按下 "p" 键查看上一张图像
                current_index -= 1
            elif key == ord("d"):  # 按下 "d" 键删除图像和标注文件
                os.remove(image_path)
                os.remove(annotation_path)
                print("Deleted:", image_path, annotation_path)
                del image_files[current_index]
            elif key == 27:  # 按下ESC键退出
                break
        except Exception as e:
            print("Error occurred while processing image:", image_path)
            print("Error message:", str(e))
            current_index += 1
            continue

    cv2.destroyAllWindows()


if __name__ == "__main__":
    image_folder = r"G:\Radar_datasets\by_sentinel\images\train"  # 图像文件夹路径
    annotation_folder = r"G:\Radar_datasets\by_sentinel\labels\train"  # 标注文件夹路径
    main(image_folder, annotation_folder)
