# -*- coding: utf-8 -*-
# @Time    : 2020/3/24 11:36
# @Author  : zhoujun
import os
import sys

project = 'OCR_DataSet'  # 工作项目根目录
sys.path.append(os.getcwd().split(project)[0] + project)
import numpy as np
from PIL import Image
from torch.utils.data import Dataset, DataLoader

from convert.utils import load, show_bbox_on_image

class DetDataSet(Dataset):
    def __init__(self, json_path, transform=None, target_transform=None):
        self.data_list = self.load_data(json_path)
        self.transform = transform
        self.target_transform = target_transform

    def load_data(self, json_path):
        """
        从json文件中读取出 文本行的坐标和gt，字符的坐标和gt
        :param json_path:
        :return:
        """
        content = load(json_path)
        d = []
        for gt in content['data_list']:
            img_path = os.path.join(content['data_root'], gt['img_name'])
            polygons = []
            texts = []
            illegibility_list = []
            language_list = []
            for annotation in gt['annotations']:
                if len(annotation['polygon']) == 0:
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
            d.append({'img_path': img_path, 'polygons': np.array(polygons), 'texts': texts,
                      'illegibility': illegibility_list,
                      'language': language_list})
        return d

    def __getitem__(self, item):
        item_dict = self.data_list[item]
        item_dict['img'] = Image.open(item_dict['img_path']).convert('RGB')
        item_dict['img'] = self.pre_processing(item_dict)
        item_dict['texts'] = self.make_label(item_dict)
        # 进行标签制作
        if self.transform:
            item_dict['img'] = self.transform(item_dict['img'])
        if self.target_transform:
            item_dict['texts'] = self.target_transform(item_dict['texts'])
        return item_dict

    def __len__(self):
        return len(self.data_list)

    def make_label(self, item_dict):
        return item_dict['texts']

    def pre_processing(self, item_dict):
        return item_dict['img']


if __name__ == '__main__':
    import time
    from tqdm import tqdm
    from torchvision import transforms
    from matplotlib import pyplot as plt

    # 支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    json_path = r'D:\dataset\自然场景文字检测挑战赛初赛数据\训练集\\train.json'

    dataset = DetDataSet(json_path, transform=transforms.ToTensor())
    train_loader = DataLoader(dataset=dataset, batch_size=1, shuffle=True, num_workers=0)
    pbar = tqdm(total=len(train_loader))
    tic = time.time()
    for i, data in enumerate(train_loader):
        pass
        img = data['img'][0].numpy().transpose(1, 2, 0) * 255
        texts = [x[0] for x in data['texts']]

        img = show_bbox_on_image(Image.fromarray(img.astype(np.uint8)), data['polygons'][0],texts)
        plt.imshow(img)
        plt.show()
        pbar.update(1)
    pbar.close()
    print(len(train_loader)/(time.time()-tic))