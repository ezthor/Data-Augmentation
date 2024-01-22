from ultralytics import YOLO
from pathlib import Path

# 加载模型
model = YOLO(r'G:\LangYa\Radar\模型\一阶段标car\best.pt')

# 图片文件夹路径
image_path = Path(r'G:\LangYa\Radar\Radar_datasets\not_label\3\images')

# 标签文件夹路径
label_path = Path(r'G:\LangYa\Radar\Radar_datasets\not_label\3\labels')
if not label_path.exists():
    label_path.mkdir()
print("start")
# 对每张图片进行推理

for img_file in image_path.glob('*.jpg'):
    # 进行推理
    results = model(img_file)

    # 遍历所有预测结果,如果置信度大于0.5,则把xywhn保存到txt文件中
    # 每个results是一个图片的预测结果，result是总的，有一个总的boxes，每一个box是一个目标，一个目标有一个conf，有一个xywhn，xywhn感觉是tensor，要[0][index]才能把四个存入
    # box.cls是tensor([0.], device='cuda:0'),要[0]才能把0存入
    for result in results:

        with open(label_path / f'{img_file.stem}.txt', 'w') as f:
            for box in result.boxes:
                if box.conf > 0.5:
                    f.write(
                        f'{box.cls[0]} {box.xywhn[0][0]} {box.xywhn[0][1]} {box.xywhn[0][2]} {box.xywhn[0][3]}\n')
    '''
    boxes	Tensor | ndarray	tensor 或包含检测框的 numpy 数组、 形状为 (num_boxes, 6) 或 (num_boxes, 7)。最后两列包含置信度和类别值。 如果存在，倒数第三列包含轨迹 ID。	所需
    '''
    '''
        for result in results:

        with open(label_path / f'{img_file.stem}.txt', 'w') as f:
            for line in result.boxes.xywhn:
                f.write(f'0 {line[0]} {line[1]} {line[2]} {line[3]}\n')
    for result in results:

        with open(label_path / f'{img_file.stem}.txt', 'w') as f:
            index = 0
            for line in result.boxes:
                if line.conf > 0.5:
                    f.write(
                        f'0 {line.xywhn[index][0]} {line.xywhn[index][1]} {line.xywhn[index][2]} {line.xywhn[index][3]}\n')
                    index += 1
    '''

