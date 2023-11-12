import os

# 将目标标注文件夹下的某个类别id转为另一个id，用于整合别人的数据集符合自己的规范


def convert_class_id(annotation_folder, id1, id2):
    annotation_files = sorted(os.listdir(annotation_folder))

    for annotation_file in annotation_files:
        annotation_path = os.path.join(annotation_folder, annotation_file)

        with open(annotation_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            class_idx = int(parts[0])
            if class_idx == id1:
                parts[0] = str(id2)
            new_line = ' '.join(parts) + '\n'
            new_lines.append(new_line)

        # Write the updated lines back to the file
        with open(annotation_path, 'w') as f:
            f.writelines(new_lines)

if __name__ == "__main__":
    annotation_folder = r"G:\Radar_datasets\sd_sentinel\New_Sentry_datasets(1-500)\labels"  # YOLO格式标注文件夹路径
    id1 = 9  # 要转换的类别id
    id2 = 13  # 转换后的类别id
    convert_class_id(annotation_folder, id1, id2)
