# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 20:33
# @Author  : zhoujun
from PIL import Image
from matplotlib import pyplot as plt

from convert.utils import show_bbox_on_image, load_gt

if __name__ == '__main__':
    json_path = r'D:\dataset\icdar2015\detection\test\test.json'
    data = load_gt(json_path)
    for img_path, gt in data.items():
        img = Image.open(img_path)
        img = show_bbox_on_image(img, gt['polygons'], gt['texts'])
        plt.imshow(img)
        plt.show()
