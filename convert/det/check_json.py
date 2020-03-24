# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 20:33
# @Author  : zhoujun
"""
用于检查生成的json文件有没有问题
"""
from PIL import Image
from  tqdm import tqdm
from matplotlib import pyplot as plt

from convert.utils import show_bbox_on_image, load_gt

if __name__ == '__main__':
    json_path = r'D:\dataset\icdar2017rctw\detection\train.json'
    data = load_gt(json_path)
    for img_path, gt in tqdm(data.items()):
        # print(gt['illegibility_list'])
        # print(gt['texts'])
        img = Image.open(img_path)
        img = show_bbox_on_image(img, gt['polygons'], gt['texts'])
        plt.imshow(img)
        plt.show()
