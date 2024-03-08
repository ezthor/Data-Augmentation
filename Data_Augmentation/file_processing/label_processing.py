import os
import shutil

# 文件夹路径
path = r'G:\LangYa\Radar\Radar_datasets\华农数据集\华农数据集_已整理\labels000001-053796\labels'



# 起始编号和结束编号
start_num = 52083
end_num = 53796
# 文件夹名称 保证6位数
new_folder = f'labels{start_num:06d}'+f'-{end_num:06d}'

# 检查新文件夹是否存在
if not os.path.isdir(os.path.join(path, new_folder)):
    os.mkdir(os.path.join(path, new_folder))

# 遍历文件夹内所有文件
for file in os.listdir(path):
    # 检查文件是否是txt文件和是否在编号内
    if file.endswith('.txt') and start_num <= int(file.strip('.txt')) <= end_num:
        # 移动文件
        shutil.move(os.path.join(path, file), os.path.join(path, new_folder, file))