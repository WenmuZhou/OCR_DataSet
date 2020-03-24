# -*- coding: utf-8 -*-
# @Time    : 2020/3/24 11:36
# @Author  : zhoujun
import os
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
            d.append({'img_path': img_path, 'polygons': polygons, 'texts': texts,
                      'illegibility_list': illegibility_list,
                      'language_list': language_list})
        return d

    def __getitem__(self, item):
        try:
            item_dict = self.data_list[item]
            item_dict['img'] = Image.open(item_dict['img_path']).convert('RGB')
            item_dict['img'] = self.pre_processing(item_dict)
            item_dict['label'] = self.make_label(item_dict)
            # 进行标签制作
            if self.transform:
                item_dict['img'] = self.transform(item_dict['img'])
            if self.target_transform:
                item_dict['label'] = self.target_transform(item_dict['label'])
            return item_dict
        except:
            return self.__getitem__(np.random.randint(self.__len__()))

    def __len__(self):
        return len(self.data_list)

    def make_label(self, item_dict):
        return item_dict['texts']

    def pre_processing(self, item_dict):
        return item_dict['img']


if __name__ == '__main__':
    from tqdm import tqdm
    from torchvision import transforms
    from matplotlib import pyplot as plt

    # 支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    json_path = r'D:\dataset\icdar2017rctw\detection\train.json'

    dataset = DetDataSet(json_path, transform=transforms.ToTensor())
    train_loader = DataLoader(dataset=dataset, batch_size=1, shuffle=True, num_workers=0)
    pbar = tqdm(total=len(train_loader))
    for i, data in enumerate(train_loader):
        img = data['img'][0].numpy().transpose(1, 2, 0) * 255
        label = [x[0] for x in data['label']]

        img = show_bbox_on_image(Image.fromarray(img.astype(np.uint8)), data['polygons'], label)
        plt.imshow(img)
        plt.show()
        pbar.update(1)
    pbar.close()
