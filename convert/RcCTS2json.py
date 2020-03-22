# -*- coding: utf-8 -*-
# @Time    : 2020/3/18 14:12
# @Author  : zhoujun
"""
将icdar2015数据集转换为统一格式
"""
import pathlib
import numpy as np
from tqdm import tqdm
from convert.utils import load, save, get_file_list


def decode_chars(char_list):
    polygon_list = []
    illegibility_list = []
    text_list = []
    for char_dict in char_list:
        polygon_list.append(np.array(char_dict['points']).reshape(-1, 2).tolist())
        illegibility_list.append(char_dict['ignore'])
        text_list.append(char_dict['transcription'])
    return polygon_list, illegibility_list, text_list


def cvt(gt_path, save_path, img_folder):
    """
    将icdar2015格式的gt转换为json格式
    :param gt_path:
    :param save_path:
    :return:
    """
    gt_dict = {'data_root': img_folder}
    data_list = []
    for file_path in tqdm(get_file_list(gt_path, p_postfix=['.json'])):
        content = load(file_path)
        file_path = pathlib.Path(file_path)
        img_name = file_path.stem + '.jpg'
        cur_gt = {'img_name': img_name, 'annotations': []}
        char_polygon_list, char_illegibility_list, char_text_list = decode_chars(content['chars'])
        for line in content['lines']:
            cur_line_gt = {'polygon': [], 'text': '', 'illegibility': False, 'language': 'Latin'}
            chars_gt = [{'polygon': [], 'char': '', 'illegibility': False, 'language': 'Latin'}]
            cur_line_gt['chars'] = chars_gt
            # 字符串级别的信息
            cur_line_gt['polygon'] = np.array(line['points']).reshape(-1, 2).tolist()
            cur_line_gt['text'] = line['transcription']
            cur_line_gt['illegibility'] = True if line['ignore'] == 1 else False
            str_len = len(line['transcription'])
            # 字符信息
            flag = False
            for char_idx in range(len(char_polygon_list)):
                for str_idx in range(1, str_len + 1):
                    if ''.join(char_text_list[char_idx:char_idx + str_idx]) == line['transcription']:
                        chars_gt = []
                        for j in range(char_idx, char_idx + str_idx):
                            chars_gt.append({'polygon': char_polygon_list[j], 'char': char_text_list[j],
                                             'illegibility': char_illegibility_list[j], 'language': 'Latin'})
                        cur_line_gt['chars'] = chars_gt
                        char_polygon_list = char_polygon_list[char_idx + str_len:]
                        char_text_list = char_text_list[char_idx + str_len:]
                        char_illegibility_list = char_illegibility_list[char_idx + str_len:]
                        flag = True
                        break
                if flag:
                    break
            cur_gt['annotations'].append(cur_line_gt)
        data_list.append(cur_gt)
    gt_dict['data_list'] = data_list
    save(gt_dict, save_path)


if __name__ == '__main__':
    gt_path = r'D:\dataset\ReCTS\detection\gt'
    img_folder = r'D:\dataset\ReCTS\detection\img'
    save_path = r'D:\dataset\ReCTS\detection\train.json'
    cvt(gt_path, save_path, img_folder)
