# -*- coding: utf-8 -*-
# @Time    : 2020/3/18 14:12
# @Author  : zhoujun
"""
将icdar2015数据集转换为统一格式
"""
import os
from tqdm import tqdm
from convert.utils import load, save


def cvt(gt_path, save_path, img_folder):
    """
    将icdar2015格式的gt转换为json格式
    :param gt_path:
    :param save_path:
    :return:
    """
    gt_dict = {'data_root': img_folder}
    data_list = []
    origin_gt = load(gt_path)
    for img_name, gt in tqdm(origin_gt.items()):
        cur_gt = {'img_name': img_name + '.jpg', 'annotations': []}
        for line in gt:
            cur_line_gt = {'polygon': [], 'text': '', 'illegibility': False, 'language': 'Latin'}
            chars_gt = [{'polygon': [], 'char': '', 'illegibility': False, 'language': 'Latin'}]
            cur_line_gt['chars'] = chars_gt
            # 字符串级别的信息
            cur_line_gt['polygon'] = line['points']
            cur_line_gt['text'] = line['transcription']
            cur_line_gt['illegibility'] = line['illegibility']
            cur_gt['annotations'].append(cur_line_gt)
        data_list.append(cur_gt)
    gt_dict['data_list'] = data_list
    save(gt_dict, save_path)


if __name__ == '__main__':
    gt_path = r'D:\dataset\LSVT\detection\train_full_labels.json'
    img_folder = r'D:\dataset\LSVT\detection\imgs'
    save_path = r'D:\dataset\LSVT\detection\train.json'
    cvt(gt_path, save_path, img_folder)
