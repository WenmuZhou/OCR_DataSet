# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 16:17
# @Author  : zhoujun
"""
根据json，将图片移动到指定文件夹，以便删除不需要的图片
"""
import os
import shutil
from tqdm import tqdm
from convert.utils import load_gt

if __name__ == '__main__':
    json_path = r'D:\dataset\COCO_Text\detection\val.json'
    save_path = r'D:\dataset\COCO_Text\detection\val'
    os.makedirs(save_path,exist_ok=True)
    data = load_gt(json_path)
    for img_path, gt in tqdm(data.items()):
        dst_path = os.path.join(save_path,os.path.basename(img_path))
        shutil.move(img_path,dst_path)
