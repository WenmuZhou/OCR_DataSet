# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 19:54
# @Author  : zhoujun
import cv2
import json
import os
import glob
import pathlib
from natsort import natsorted

__all__ = ['load']


def get_file_list(folder_path: str, p_postfix: list = None) -> list:
    """
    获取所给文件目录里的指定后缀的文件,读取文件列表目前使用的是 os.walk 和 os.listdir ，这两个目前比 pathlib 快很多
    :param filder_path: 文件夹名称
    :param p_postfix: 文件后缀,如果为 [.*]将返回全部文件
    :return: 获取到的指定类型的文件列表
    """
    assert os.path.exists(folder_path) and os.path.isdir(folder_path)
    if p_postfix is None:
        p_postfix = ['.jpg']
    if isinstance(p_postfix, str):
        p_postfix = [p_postfix]
    file_list = [x for x in glob.glob(folder_path + '/**/*.*', recursive=True) if
                 os.path.splitext(x)[-1] in p_postfix or '.*' in p_postfix]
    return natsorted(file_list)


def load(file_path: str):
    file_path = pathlib.Path(file_path)
    func_dict = {'.txt': load_txt, '.json': load_json, '.list': load_txt}
    assert file_path.suffix in func_dict
    return func_dict[file_path.suffix](file_path)


def load_txt(file_path: str):
    with open(file_path, 'r', encoding='utf8') as f:
        content = [x.strip().strip('\ufeff').strip('\xef\xbb\xbf') for x in f.readlines()]
    return content


def load_json(file_path: str):
    with open(file_path, 'r', encoding='utf8') as f:
        content = json.load(f)
    return content


def save(data, file_path):
    file_path = pathlib.Path(file_path)
    func_dict = {'.txt': save_txt, '.json': save_json}
    assert file_path.suffix in func_dict
    return func_dict[file_path.suffix](data, file_path)


def save_txt(data, file_path):
    """
    将一个list的数组写入txt文件里
    :param data:
    :param file_path:
    :return:
    """
    if not isinstance(data, list):
        data = [data]
    with open(file_path, mode='w', encoding='utf8') as f:
        f.write('\n'.join(data))


def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def show_bbox_on_image(image, polygons=None, txt=None, color=None, font_path='convert/simsun.ttc'):
    """
    在图片上绘制 文本框和文本
    :param image:
    :param polygons: 文本框
    :param txt: 文本
    :param color: 绘制的颜色
    :param font_path: 字体
    :return:
    """
    from PIL import ImageDraw, ImageFont
    image = image.convert('RGB')
    draw = ImageDraw.Draw(image)
    if color is None:
        color = (255, 0, 0)
    if txt is not None:
        font = ImageFont.truetype(font_path, 20)
    for i, box in enumerate(polygons):
        if txt is not None:
            draw.text((int(box[0][0]) + 20, int(box[0][1]) - 20), str(txt[i]), fill='red', font=font)
        for j in range(len(box) - 1):
            draw.line((box[j][0], box[j][1], box[j + 1][0], box[j + 1][1]), fill=color, width=5)
        draw.line((box[-1][0], box[-1][1], box[0][0], box[0][1]), fill=color, width=5)
    return image


def load_gt(json_path):
    """
    从json文件中读取出 文本行的坐标和gt，字符的坐标和gt
    :param json_path:
    :return:
    """
    content = load(json_path)
    d = {}
    for gt in content['data_list']:
        img_path = os.path.join(content['data_root'], gt['img_name'])
        polygons = []
        texts = []
        illegibility_list = []
        language_list = []
        for annotation in gt['annotations']:
            if len(annotation['polygon']) == 0 or len(annotation['text']) == 0:
                continue
            polygons.append(annotation['polygon'])
            texts.append(annotation['text'])
            illegibility_list.append(annotation['illegibility'])
            language_list.append(annotation['language'])
            for char_annotation in annotation['chars']:
                if len(char_annotation['polygon']) == 0 or len(char_annotation['char']) == 0:
                    continue
                polygons.append(char_annotation['polygon'])
                texts.append(char_annotation['char'])
                illegibility_list.append(char_annotation['illegibility'])
                language_list.append(char_annotation['language'])
        d[img_path] = {'polygons': polygons, 'texts': texts, 'illegibility_list': illegibility_list,
                       'language_list': language_list}
    return d
