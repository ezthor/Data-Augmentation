# RM数据集清洗与整理脚本

>ezthor 2024.3.8

一些文件、图像和标注处理的小脚本，拥有板块如下

- 可视化
- 统计
- 筛选
- 文件移动
- 裁切roi图像
- 标注格式转换
- 标注清洗
- 自动标注

其中很多代码都是一次性的处理小工具，没有很好的封装，有一些是尝试写了没成功的半成品代码，慎用，如果遇到出错可能是代码问题，可以私信我

## 可视化（visualize）

功能有coco、yolo、真实像素值和上交格式（四点的xy比例坐标）的标注的可视化

## 统计（statistic）

统计每个类别的bbox数量

## 筛选（select）

image_filter是初筛，只保留有某个类别标注的标注文件和图片，没有封装，不建议用

single_cls_filter是把某个区间的类别同时筛出的，有一定的封装，例如可以选择筛出有类别从4-7的所有图片

## 文件移动（file_processing)

分别为文件按比例分割为train和val

把编号a-b的标注文件移动到另外一个文件夹

将存放在各个文件夹下的images和labels归总到一个总文件夹下

## 裁切roi图像（extract_and_paste)

把某个图像的标注区域周围的roi区域裁剪下来，并保存新标注信息（以yolo，真实像素值等格式）

## 标注类别转换（conversion）

有4点格式转为yolo格式、真实像素值转为yolo格式、上交格式转为yolo格式、yolo格式转到coco格式、将某个文件夹内的标注编号由a改为b等功能

## 清洗（cleaning）

把没有标注的图片删除

把没标注为空的图片和标注文件删除

把某个类别的标注删除

检查某个文件夹下是否有重复的文件

## 自动标注（auto_label)

用训练好的模型对文件夹下的图片进行预标注







