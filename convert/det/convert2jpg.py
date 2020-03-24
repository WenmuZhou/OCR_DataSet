# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 10:37
# @Author  : zhoujun
"""
用于将图片统一转换为jpg
"""
import os
import pathlib
from tqdm import tqdm
from convert.utils import get_file_list

if __name__ == '__main__':
    img_folder = r'D:\dataset\mlt2019\detection\imgs'
    for img_path in tqdm(get_file_list(img_folder, p_postfix=['.*'])):
        img_path = pathlib.Path(img_path)
        save_path = img_path.parent / (img_path.stem + '.jpg')
        if img_path != save_path:
            os.rename(img_path, save_path)
