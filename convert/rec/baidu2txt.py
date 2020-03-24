# -*- coding: utf-8 -*-
# @Time    : 2020/3/24 11:10
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
    for line in tqdm(content):
        line = line.split('\t')
        img_path = os.path.join(img_folder, line[-2])
        if not os.path.exists(img_path):
            print(img_path)
        file_list.append(img_path + '\t' + line[-1] + '\t' + 'Chinese')
        # img = Image.open(img_path)
        # plt.title(line[-1])
        # plt.imshow(img)
        # plt.show()
    save(file_list, save_path)


if __name__ == '__main__':
    img_folder = r'D:\dataset\百度中文场景文字识别\train_images'
    gt_path = r'D:\dataset\百度中文场景文字识别\train.list'
    save_path = r'D:\dataset\百度中文场景文字识别\train.txt'
    cvt(gt_path, save_path, img_folder)
