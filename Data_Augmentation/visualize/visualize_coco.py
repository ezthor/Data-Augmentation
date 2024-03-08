from pathlib import Path
import cv2
from pycocotools.coco import COCO
import matplotlib.pyplot as plt

# COCO annotations file path
annotations_file = r'G:\道路危害大赛\数据集\train1117_coco_new\annotations\instances_train2017.json'
images_directory = Path(r'G:\道路危害大赛\数据集\train1117_coco_new\train2017')

# Initialize COCO API for instance annotations
coco = COCO(annotations_file)

# Load all image ids
image_ids = coco.getImgIds()

# Visualize images with annotations
for img_id in image_ids:
    # Load image info
    image_info = coco.loadImgs(img_id)[0]
    image_path = images_directory / image_info['file_name']

    # Read image using OpenCV
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Failed to read image: {image_path}")
        continue

    # Load annotations for the image
    annotation_ids = coco.getAnnIds(imgIds=img_id)
    annotations = coco.loadAnns(annotation_ids)

    # Display image with annotations
    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    # Plot annotations
    for annotation in annotations:
        bbox = annotation['bbox']
        category_id = annotation['category_id']
        category = coco.loadCats(category_id)[0]['name']
        x, y, w, h = bbox
        plt.gca().add_patch(plt.Rectangle((x, y), w, h, fill=False, edgecolor='red', linewidth=2))
        plt.text(x, y - 5, category, color='red', fontsize=10, weight='bold')

    plt.show()
