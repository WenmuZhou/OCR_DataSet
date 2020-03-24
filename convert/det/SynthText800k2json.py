# -*- coding: utf-8 -*-
# @Time    : 2020/3/23 9:29
# @Author  : zhoujun
import os
import pathlib
import numpy as np
from tqdm import tqdm
import scipy.io as sio
from convert.utils import save


class SynthTextDataset():
    def __init__(self, img_folder: str, gt_path: str):
        self.img_folder = img_folder
        if not os.path.exists(self.img_folder):
            raise FileNotFoundError('Dataset folder is not exist.')

        self.targetFilePath = gt_path
        if not os.path.exists(self.targetFilePath):
            raise FileExistsError('Target file is not exist.')
        targets = {}
        sio.loadmat(self.targetFilePath, targets, squeeze_me=True, struct_as_record=False,
                    variable_names=['imnames', 'wordBB', 'txt'])

        self.imageNames = targets['imnames']
        self.wordBBoxes = targets['wordBB']
        self.transcripts = targets['txt']

    def cvt(self):
        gt_dict = {'data_root': self.img_folder}
        data_list = []
        pbar = tqdm(total=len(self.imageNames))
        for imageName, wordBBoxes, texts in zip(self.imageNames, self.wordBBoxes, self.transcripts):
            wordBBoxes = np.expand_dims(wordBBoxes, axis=2) if (wordBBoxes.ndim == 2) else wordBBoxes
            _, _, numOfWords = wordBBoxes.shape
            text_polys = wordBBoxes.reshape([8, numOfWords], order='F').T  # num_words * 8
            text_polys = text_polys.reshape(numOfWords, 4, 2)  # num_of_words * 4 * 2
            transcripts = [word for line in texts for word in line.split()]
            if numOfWords != len(transcripts):
                continue
            cur_gt = {'img_name': imageName, 'annotations': []}
            for polygon, text in zip(text_polys, transcripts):
                cur_line_gt = {'polygon': [], 'text': '', 'illegibility': False, 'language': 'Latin'}
                chars_gt = [{'polygon': [], 'char': '', 'illegibility': False, 'language': 'Latin'}]
                cur_line_gt['chars'] = chars_gt
                cur_line_gt['text'] = text
                cur_line_gt['polygon'] = polygon.tolist()
                cur_line_gt['illegibility'] = text in ['###', '*']
                cur_gt['annotations'].append(cur_line_gt)
            data_list.append(cur_gt)
            pbar.update(1)
        pbar.close()
        gt_dict['data_list'] = data_list
        save(gt_dict, save_path)


if __name__ == '__main__':
    img_folder = r'D:\dataset\SynthText800k\detection\imgs'
    gt_path = r'D:\dataset\SynthText800k\detection\gt.mat'
    save_path = r'D:\dataset\SynthText800k\detection\train1.json'
    synth_dataset = SynthTextDataset(img_folder, gt_path)
    synth_dataset.cvt()
