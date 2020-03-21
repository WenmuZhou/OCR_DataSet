# -*- coding: utf-8 -*-
# @Time    : 2020/3/21 12:54
# @Author  : zhoujun
"""
将coco_text数据集转换为统一格式
"""
import os
import numpy as np
from tqdm import tqdm
from convert.utils import load, save
from convert.coco_text import COCO_Text

def cvt(gt_path, save_path, imgs_folder):
    gt_dict = {'data_root': imgs_folder}
    data_list = []
    ct = COCO_Text(gt_path)

    train_img_ids = ct.getImgIds(imgIds=ct.val)
    for img_id in tqdm(train_img_ids):
        img = ct.loadImgs(img_id)[0]
        # img_path = os.path.join(imgs_folder, img['file_name'])
        # if not os.path.exists(img_path):
        #     continue
        cur_gt = {'img_name': img['file_name'], 'annotations': []}
        annIds = ct.getAnnIds(imgIds=img['id'])
        anns = ct.loadAnns(annIds)
        for ann in anns:
            if len(ann['utf8_string']) == 0:
                continue
            cur_line_gt = {'polygon': [], 'text': '', 'illegibility': False, 'language': 'Latin'}
            chars_gt = [{'polygon': [], 'char': '', 'illegibility': False, 'language': 'Latin'}]
            cur_line_gt['chars'] = chars_gt

            cur_line_gt['language'] = ann['language']
            chars_gt[0]['language'] = ann['language']

            cur_line_gt['polygon'] = np.array(ann['mask']).reshape(-1,2).tolist()
            cur_line_gt['text'] = ann['utf8_string']
            cur_line_gt['illegibility'] = True if ann['legibility'] == "illegible" else False
            cur_gt['annotations'].append(cur_line_gt)
        if len(cur_gt['annotations']) > 0:
            data_list.append(cur_gt)
    gt_dict['data_list'] = data_list
    save(gt_dict, save_path)
    print(len(gt_dict), len(data_list))


def show_coco(gt_path, imgs_folder):
    import numpy as np
    import skimage.io as io
    import matplotlib.pyplot as plt

    data = COCO_Text(gt_path)
    # get all images containing at least one instance of legible text
    imgIds = data.getImgIds(imgIds=data.train)
    # pick one at random
    img = data.loadImgs(imgIds[np.random.randint(0, len(imgIds))])[0]
    I = io.imread(os.path.join(imgs_folder, img['file_name']))
    plt.figure()
    plt.imshow(I)
    annIds = data.getAnnIds(imgIds=img['id'])
    anns = data.loadAnns(annIds)
    data.showAnns(anns)
    plt.show()


if __name__ == '__main__':
    gt_path = r'D:\dataset\COCO_Text\detection\cocotext.v2.json'
    imgs_folder = r'D:\dataset\COCO_Text\detection\val'
    save_path = r'D:\dataset\COCO_Text\detection\val.json'
    cvt(gt_path, save_path, imgs_folder)
    # show_coco(gt_path, imgs_folder)
