# -*- coding: utf-8 -*-
# @Time    : 2020/3/24 11:10
# @Author  : zhoujun
import os
import pathlib
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt
from convert.utils import load, save


def cvt(gt_path, save_path, img_folder):
    content = load(gt_path)
    file_list = []
    for line in tqdm(content):
        img_relative_path = line.split(' ')[0]
        img_path = os.path.join(img_folder, img_relative_path)
        img_path = pathlib.Path(img_path)
        label = img_path.stem.split('_')[1]
        if not img_path.exists():
            print(img_path)
        file_list.append(str(img_path) + '\t' + label + '\t' + 'English')
        # img = Image.open(img_path)
        # plt.title(label)
        # plt.imshow(img)
        # plt.show()
    save(file_list, save_path)


if __name__ == '__main__':
    img_folder = r'D:\dataset\mjsynth\imgs'
    gt_path = r'D:\dataset\mjsynth\annotation_test.txt'
    save_path = r'D:\dataset\mjsynth\test.txt'
    cvt(gt_path, save_path, img_folder)
