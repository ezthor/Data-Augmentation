# 将视频抽帧
import cv2
from tqdm import tqdm
import os

path = "/home/nvidia/RDDWorkspace/data/IMG_1050.mov"
video_name = path.split('/')[-1].split('.')[0]
video = cv2.VideoCapture(path)
target_folder_path = "/home/nvidia/RDDWorkspace/data/auto_label/"
target_folder_path += video_name
target_folder_path += "/images"
if not os.path.exists(target_folder_path):
    os.makedirs(target_folder_path)
frame_num = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
for i in tqdm(range(frame_num), desc="Extracting frames"):
    ret, frame = video.read()
    if not ret:
        print("empty")
        break
    cv2.imwrite(f"{target_folder_path}/{video_name}_{int(video.get(1)):06d}.jpg", frame)
    # print(f"Extracting frame {video.get(1)}")