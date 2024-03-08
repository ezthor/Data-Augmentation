import os
import json
from PIL import Image

# YOLO格式的标签转换为COCO格式的标签
def yolo_to_coco(yolo_bbox, image_width, image_height):
    x_center, y_center, bbox_width, bbox_height = yolo_bbox
    x_center *= image_width
    y_center *= image_height
    bbox_width *= image_width
    bbox_height *= image_height

    x_min = max(0, int(x_center - bbox_width / 2))
    y_min = max(0, int(y_center - bbox_height / 2))
    x_max = min(image_width, int(x_center + bbox_width / 2))
    y_max = min(image_height, int(y_center + bbox_height / 2))

    return [x_min, y_min, x_max - x_min, y_max - y_min]

# 创建COCO格式的annotation
def create_coco_annotation(image_id, yolo_annotations, image_width, image_height):
    annotations = []
    for yolo_annotation in yolo_annotations:
        category_id, *bbox = yolo_annotation
        coco_bbox = yolo_to_coco(bbox, image_width, image_height)
        annotation = {
            "id": len(annotations) + 1,
            "image_id": image_id,
            "category_id": category_id,
            "bbox": coco_bbox,
            "area": coco_bbox[2] * coco_bbox[3],
            "iscrowd": 0
        }
        annotations.append(annotation)
    return annotations

# 转换Yolo数据集到COCO格式
def convert_yolo_to_coco(yolo_dir, coco_dir):
    categories = [{"id": 0, "name": "category_name"}]  # 修改为你的类别信息

    for split in ["train", "val"]:
        images_path = os.path.join(yolo_dir, "images", split)
        labels_path = os.path.join(yolo_dir, "labels", split)
        coco_images_path = os.path.join(coco_dir, f"{split}2017")
        if not os.path.exists(coco_images_path):
            os.makedirs(coco_images_path)

        images = []
        annotations = []
        image_id = 1

        for filename in os.listdir(images_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(images_path, filename)
                image = Image.open(image_path)
                image_width, image_height = image.size

                # Create COCO image entry
                coco_image = {
                    "id": image_id,
                    "file_name": filename,
                    "width": image_width,
                    "height": image_height
                }
                images.append(coco_image)

                # Read YOLO annotations
                label_file_path = os.path.join(labels_path, filename.replace(".jpg", ".txt"))
                with open(label_file_path, 'r') as label_file:
                    lines = label_file.readlines()
                    yolo_annotations = [list(map(float, line.strip().split())) for line in lines]

                # Create COCO annotations
                coco_annotations = create_coco_annotation(image_id, yolo_annotations, image_width, image_height)
                annotations.extend(coco_annotations)

                # Copy image to COCO directory
                destination_path = os.path.join(coco_images_path, filename)
                image.save(destination_path)

                image_id += 1

        instances_data = {
            "info": {},
            "licenses": {},
            "images": images,
            "annotations": annotations,
            "categories": categories
        }

        annotations_path = os.path.join(coco_dir, "annotations")
        if not os.path.exists(annotations_path):
            os.makedirs(annotations_path)

        if split == "train":
            instances_train_path = os.path.join(annotations_path, "instances_train2017.json")
            with open(instances_train_path, 'w') as train_file:
                json.dump(instances_data, train_file)
        elif split == "val":
            instances_val_path = os.path.join(annotations_path, "instances_val2017.json")
            with open(instances_val_path, 'w') as val_file:
                json.dump(instances_data, val_file)

# 使用示例
yolo_dataset_directory = r'G:\道路危害大赛\数据集\train1117'
coco_dataset_directory = r'G:\道路危害大赛\数据集\train1117_coco_new'

convert_yolo_to_coco(yolo_dataset_directory, coco_dataset_directory)
