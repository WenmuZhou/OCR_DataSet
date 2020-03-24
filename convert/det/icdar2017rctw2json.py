# -*- coding: utf-8 -*-
# @Time    : 2020/3/18 14:12
# @Author  : zhoujun
"""
将icdar2015数据集转换为统一格式
"""
import pathlib
from tqdm import tqdm
from convert.utils import load, save, get_file_list


def cvt(save_path, img_folder):
    """
    将icdar2015格式的gt转换为json格式
    :param gt_path:
    :param save_path:
    :return:
    """
    gt_dict = {'data_root': img_folder}
    data_list = []
    for img_path in tqdm(get_file_list(img_folder, p_postfix=['.jpg'])):
        img_path = pathlib.Path(img_path)
        gt_path = pathlib.Path(img_folder) / img_path.name.replace('.jpg', '.txt')
        content = load(gt_path)
        cur_gt = {'img_name': img_path.name, 'annotations': []}
        for line in content:
            cur_line_gt = {'polygon': [], 'text': '', 'illegibility': False, 'language': 'Latin'}
            chars_gt = [{'polygon': [], 'char': '', 'illegibility': False, 'language': 'Latin'}]
            cur_line_gt['chars'] = chars_gt
            line = line.split(',')
            # 字符串级别的信息
            x1, y1, x2, y2, x3, y3, x4, y4 = list(map(float, line[:8]))
            cur_line_gt['polygon'] = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            cur_line_gt['text'] = line[-1][1:-1]
            cur_line_gt['illegibility'] = True if line[8] == '1' else False
            cur_gt['annotations'].append(cur_line_gt)
        data_list.append(cur_gt)
    gt_dict['data_list'] = data_list
    save(gt_dict, save_path)


if __name__ == '__main__':
    img_folder = r'D:\dataset\icdar2017rctw\detection\imgs'
    save_path = r'D:\dataset\icdar2017rctw\detection\train.json'
    cvt(save_path, img_folder)
