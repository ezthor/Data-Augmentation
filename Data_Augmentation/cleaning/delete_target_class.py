import os

# 将目标号的标注删除,一般不用，我是特定作业需要才写了这个

def remove_target_class_annotations(annotation_folder):
    annotation_files = sorted(os.listdir(annotation_folder))

    for annotation_file in annotation_files:
        annotation_path = os.path.join(annotation_folder, annotation_file)

        with open(annotation_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            class_idx = int(line.split()[0])
            if class_idx != target:
                new_lines.append(line)

        # Write the updated lines back to the file
        with open(annotation_path, 'w') as f:
            f.writelines(new_lines)

        if not new_lines:
            print(f"File '{annotation_file}' has no remaining annotations.")


if __name__ == "__main__":
    annotation_folder = r"G:\Radar_datasets\sd_sentinel\New_Sentry_datasets(1-500)\labels"  # YOLO格式标注文件夹路径
    target = 3
    remove_target_class_annotations(annotation_folder)
