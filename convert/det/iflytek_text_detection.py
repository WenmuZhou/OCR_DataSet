# -*- coding: utf-8 -*-
# @Time    : 2020/7/7 10:08
# @Author  : zhoujun
import numpy as np
from tqdm import tqdm
from convert.utils import load, save


def cvt(gt_path, save_path, imgs_folder):
    gt_dict = {'data_root': imgs_folder}
    data_list = []
    ct = load(gt_path)

    for img_id, anns in tqdm(ct.items()):
        img_name = img_id.replace('gt', 'img') + '.jpg'
        cur_gt = {'img_name': img_name, 'annotations': []}
        for ann in anns:
            cur_line_gt = {'polygon': [], 'text': '', 'illegibility': False, 'language': 'Latin'}
            chars_gt = [{'polygon': [], 'char': '', 'illegibility': False, 'language': 'Latin'}]
            cur_line_gt['chars'] = chars_gt

            cur_line_gt['polygon'] = ann['points']
            cur_line_gt['illegibility'] = ann['illegibility']
            cur_gt['annotations'].append(cur_line_gt)
        if len(cur_gt['annotations']) > 0:
            data_list.append(cur_gt)
    gt_dict['data_list'] = data_list
    save(gt_dict, save_path)
    print(len(gt_dict), len(data_list))


if __name__ == '__main__':
    gt_path = r'D:\dataset\自然场景文字检测挑战赛初赛数据\验证集\validation.json'
    imgs_folder = r'D:\dataset\自然场景文字检测挑战赛初赛数据\验证集\new_image'
    save_path = r'D:\dataset\自然场景文字检测挑战赛初赛数据\验证集\validation_new.json'
    cvt(gt_path, save_path, imgs_folder)
    # show_coco(gt_path, imgs_folder)
