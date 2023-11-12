import os

# 将标注信息和图片一起删除，如果标注为空

def delete_empty_annotations(image_folder, annotation_folder):
    image_files = sorted(os.listdir(image_folder))
    annotation_files = sorted(os.listdir(annotation_folder))

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        annotation_file = image_file.replace(".jpg", ".txt")  # 假设标注文件扩展名是 '.txt'
        annotation_path = os.path.join(annotation_folder, annotation_file)

        if not os.path.exists(annotation_path) or os.path.getsize(annotation_path) == 0:
            os.remove(image_path)
            if os.path.exists(annotation_path):
                os.remove(annotation_path)

if __name__ == "__main__":
    image_folder = r"G:\Radar_datasets\sd_sentinel\New_Sentry_datasets(1-500)\images"  # 图片文件夹路径
    annotation_folder = r"G:\Radar_datasets\sd_sentinel\New_Sentry_datasets(1-500)\labels"  # 标注文件夹路径
    delete_empty_annotations(image_folder, annotation_folder)
