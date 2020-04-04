# -*- coding: utf-8 -*-
# @Time    : 2020/4/2 18:41
# @Author  : zhoujun
import lmdb
import six
import sys
import numpy as np
from PIL import Image
from torch.utils.data import Dataset, DataLoader,ConcatDataset


class lmdbDataset(Dataset):
    def __init__(self, lmdb_path=None, transform=None, target_transform=None):
        self.env = lmdb.open(lmdb_path, max_readers=12, readonly=True, lock=False, readahead=False, meminit=False)

        if not self.env:
            print('cannot creat lmdb from %s' % (lmdb_path))
            sys.exit(0)

        with self.env.begin(write=False) as txn:
            nSamples = int(txn.get('num-samples'.encode('utf-8')))
            self.nSamples = nSamples

        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        assert index <= len(self), 'index range error'
        index += 1
        item = {}
        with self.env.begin(write=False) as txn:
            img_key = 'image-%09d' % index
            imgbuf = txn.get(img_key.encode('utf-8'))

            buf = six.BytesIO()
            buf.write(imgbuf)
            buf.seek(0)
            try:
                img = Image.open(buf).convert('RGB')
            except IOError:
                print('Corrupted image for %d' % index)
                return self[index + 1]

            if self.transform is not None:
                img = self.transform(img)
            item['img'] = img
            polygonsKey = 'polygons-%09d' % index
            textsKey = 'texts-%09d' % index
            illegibilityKey = 'illegibility-%09d' % index
            languageKey = 'language-%09d' % index
            polygons = txn.get(polygonsKey.encode('utf-8'))
            item['polygons'] = np.frombuffer(polygons).reshape(-1, 4, 2)

            item['texts'] = txn.get(textsKey.encode('utf-8')).decode().split('\t')
            illegibility = txn.get(illegibilityKey.encode('utf-8')).decode().split('\t')
            item['illegibility'] = [x.lower()=='true' for x in illegibility]
            item['language'] = txn.get(languageKey.encode('utf-8')).decode().split('\t')

            if self.target_transform is not None:
                item['texts'] = self.target_transform(item['texts'])

        return item


if __name__ == '__main__':
    import time
    from tqdm import tqdm
    from torchvision import transforms
    from matplotlib import pyplot as plt

    # 支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    lmdb_path = r'E:\zj\dataset\icdar2015 (2)\train'

    dataset = lmdbDataset(lmdb_path, transform=transforms.ToTensor())
    train_loader = DataLoader(dataset=dataset, batch_size=1, shuffle=True, num_workers=0)
    pbar = tqdm(total=len(train_loader))
    tic = time.time()
    for i, data in enumerate(train_loader):
        pass
        # img = data['img'][0].numpy().transpose(1, 2, 0) * 255
        # label = [x[0] for x in data['texts']]
        #
        # img = show_bbox_on_image(Image.fromarray(img.astype(np.uint8)), data['polygons'][0], label)
        # plt.imshow(img)
        # plt.show()
        # pbar.update(1)
    # pbar.close()
    print(len(train_loader) / (time.time() - tic))