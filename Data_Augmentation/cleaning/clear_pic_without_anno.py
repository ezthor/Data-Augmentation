import os

# 如果目标文件夹下图片没有标注，把图片删掉

def check_and_delete_unmatched_images(image_folder, annotation_folder):
    image_files = os.listdir(image_folder)
    annotation_files = os.listdir(annotation_folder)

    for image_file in image_files:
        image_name = os.path.splitext(image_file)[0]
        annotation_file = image_name + ".txt"

        if annotation_file not in annotation_files:
            image_path = os.path.join(image_folder, image_file)
            annotation_path = os.path.join(annotation_folder, annotation_file)

            # Delete image and annotation file
            os.remove(image_path)
            if os.path.exists(annotation_path):
                os.remove(annotation_path)

            print("Deleted:", image_file, annotation_file)

if __name__ == "__main__":
    image_folder = r"G:\Radar_datasets\yolo\paste_red5turn1\images"  # 图像文件夹路径
    annotation_folder = r"G:\Radar_datasets\yolo\paste_red5turn1\labels"  # 标注文件夹路径

    check_and_delete_unmatched_images(image_folder, annotation_folder)
