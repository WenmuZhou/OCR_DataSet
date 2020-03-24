# -*- coding: utf-8 -*-
# @Time    : 2020/3/24 11:36
# @Author  : zhoujun
import os
import numpy as np
from PIL import Image
from torch.utils.data import Dataset, DataLoader

from convert.utils import load


class DetDataSet(Dataset):
    def __init__(self, txt_path, transform=None, target_transform=None):
        self.data_list = load(txt_path)
        self.transform = transform
        self.target_transform = target_transform

    def __getitem__(self, item):
        try:
            line = self.data_list[item].split('\t')
            img = Image.open(line[0]).convert('RGB')
            img = self.pre_processing(img)
            label = self.make_label(line[1])
            # 进行标签制作
            if self.transform:
                img = self.transform(img)
            if self.target_transform:
                label = self.target_transform(label)
            return img, label
        except:
            return self.__getitem__(np.random.randint(self.__len__()))

    def __len__(self):
        return len(self.data_list)

    def make_label(self, label):
        return label

    def pre_processing(self, img):
        return img


if __name__ == '__main__':
    from tqdm import tqdm
    from torchvision import transforms
    from matplotlib import pyplot as plt

    # 支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    json_path = r'D:\dataset\icdar2017rctw\recognition\train.txt'

    dataset = DetDataSet(json_path, transform=transforms.ToTensor())
    train_loader = DataLoader(dataset=dataset, batch_size=1, shuffle=True, num_workers=0)
    pbar = tqdm(total=len(train_loader))
    for i, (img, label) in enumerate(train_loader):
        img = img[0].numpy().transpose(1, 2, 0)
        plt.title(label[0])
        plt.imshow(img)
        plt.show()
        pbar.update(1)
    pbar.close()
