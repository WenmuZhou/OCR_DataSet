# -*- coding: utf-8 -*-
# @Time    : 2020/3/24 11:26
# @Author  : zhoujun

import os
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
from convert.utils import load, save

def cvt(gt_path, save_path, img_folder):
    content = load(gt_path)
    file_list = []
    for i,line in tqdm(enumerate(content)):
        try:
            line = line.split('.jpg ')
            img_path = os.path.join(img_folder, line[-2])
            file_list.append(img_path + '.jpg' + '\t' + line[-1] + '\t' + 'Chinese')
            # img = Image.open(img_path)
            # plt.title(line[-1])
            # plt.imshow(img)
            # plt.show()
        except:
            a = 1
    save(file_list, save_path)


if __name__ == '__main__':
    img_folder = r'D:\dataset\360w\train_images'
    gt_path = r'D:\BaiduNetdiskDownload\360_train.txt'
    save_path = r'D:\BaiduNetdiskDownload\train.txt'
    cvt(gt_path, save_path, img_folder)