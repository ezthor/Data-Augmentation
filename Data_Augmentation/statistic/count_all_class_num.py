import os

# 统计bbox数

def count_bbox_by_class(folder_path):
    class_bbox_count = {}

    # 遍历文件夹下所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # 仅处理Yolo标注文件（.txt文件）
            with open(os.path.join(folder_path, filename), "r") as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split()
                    if len(data) == 5:
                        class_index = int(float(data[0]))  # 解析为整数

                        # 统计每个类别的bbox数量
                        class_bbox_count[class_index] = class_bbox_count.get(class_index, 0) + 1

    return class_bbox_count

def main():
    folder_path = r"G:\Radar_datasets\yolo\paste_red5turn1_blue5turn1\labels"  # 替换为你的文件夹路径
    class_bbox_count = count_bbox_by_class(folder_path)

    # 输出结果
    for class_index, bbox_count in class_bbox_count.items():
        print(f"类别 {class_index}: {bbox_count} 个 bbox")

if __name__ == "__main__":
    main()
