# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 20:55
# @Author  : zhoujun
import os
import shutil
import pathlib
import numpy as np
from tqdm import tqdm
from PIL import Image
from matplotlib import pyplot as plt

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

from convert.utils import load_gt, save

if __name__ == '__main__':
    json_path = r'D:\dataset\icdar2015\detection\train.json'
    save_path = r'D:\dataset\icdar2015\recognition\train'
    gt_path = pathlib.Path(save_path).parent / 'train.txt'
    if os.path.exists(save_path):
        shutil.rmtree(save_path, ignore_errors=True)
    os.makedirs(save_path, exist_ok=True)
    data = load_gt(json_path)
    file_list = []
    for img_path, gt in tqdm(data.items()):
        img = Image.open(img_path)
        img_name = pathlib.Path(img_path).stem
        for i, (polygon, text, illegibility) in enumerate(zip(gt['polygons'], gt['texts'], gt['illegibility_list'])):
            if illegibility:
                continue
            polygon = np.array(polygon)
            x_min = polygon[:, 0].min()
            x_max = polygon[:, 0].max()
            y_min = polygon[:, 1].min()
            y_max = polygon[:, 1].max()
            roi_img = img.crop((x_min, y_min, x_max, y_max))
            roi_img_save_path = os.path.join(save_path, '{}_{}.jpg'.format(img_name, i))
            roi_img.save(roi_img_save_path)
            file_list.append(roi_img_save_path + '\t' + text)
            # plt.title(text)
            # plt.imshow(roi_img)
            # plt.show()
    save(file_list, gt_path)
