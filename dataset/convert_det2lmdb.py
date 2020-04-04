# -*- coding: utf-8 -*-
# @Time    : 2020/4/2 14:19
# @Author  : zhoujun

import os
import lmdb
import cv2
import numpy as np
import argparse
import shutil
import sys
from convert.utils import load_gt

def checkImageIsValid(imageBin):
    if imageBin is None:
        return False

    try:
        imageBuf = np.fromstring(imageBin, dtype=np.uint8)
        img = cv2.imdecode(imageBuf, cv2.IMREAD_GRAYSCALE)
        imgH, imgW = img.shape[0], img.shape[1]
    except:
        return False
    else:
        if imgH * imgW == 0:
            return False

    return True


def writeCache(env, cache):
    with env.begin(write=True) as txn:
        for k, v in cache.items():
            if type(k) == str:
                k = k.encode()
            if type(v) == str:
                v = v.encode()
            txn.put(k, v)


def createDataset(outputPath, data_dict, map_size=79951162, checkValid=True):
    """
    Create LMDB dataset for CRNN training.

    ARGS:
        outputPath    : LMDB output path
        data_dict : a dict contains img_path,texts,text_polys
        checkValid    : if true, check the validity of every image
    """
    # If lmdb file already exists, remove it. Or the new data will add to it.
    if os.path.exists(outputPath):
        shutil.rmtree(outputPath)
        os.makedirs(outputPath)
    else:
        os.makedirs(outputPath)

    nSamples = len(data_dict)
    env = lmdb.open(outputPath, map_size=map_size)
    cache = {}
    cnt = 1
    for img_path in data_dict:
        data = data_dict[img_path]
        if not os.path.exists(img_path):
            print('%s does not exist' % img_path)
            continue
        with open(img_path, 'rb') as f:
            imageBin = f.read()
        if checkValid:
            if not checkImageIsValid(imageBin):
                print('%s is not a valid image' % img_path)
                continue

        imageKey = 'image-%09d' % cnt
        polygonsKey = 'polygons-%09d' % cnt
        textsKey = 'texts-%09d' % cnt
        illegibilityKey = 'illegibility-%09d' % cnt
        languageKey = 'language-%09d' % cnt
        cache[imageKey] = imageBin
        cache[polygonsKey] = np.array(data['polygons']).tostring()
        cache[textsKey] = '\t'.join(data['texts'])
        cache[illegibilityKey] = '\t'.join([str(x) for x in data['illegibility_list']])
        cache[languageKey] = '\t'.join(data['language_list'])
        if cnt % 1000 == 0:
            writeCache(env, cache)
            cache = {}
            print('Written %d / %d' % (cnt, nSamples))
        cnt += 1
    nSamples = cnt - 1
    cache['num-samples'] = str(nSamples)
    writeCache(env, cache)
    env.close()
    print('Created dataset with %d samples' % nSamples)


def show_demo(demo_number, image_path_list, label_list):
    print('\nShow some demo to prevent creating wrong lmdb data')
    print('The first line is the path to image and the second line is the image label')
    for i in range(demo_number):
        print('image: %s\nlabel: %s\n' % (image_path_list[i], label_list[i]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('--out', type = str, required = True, help = 'lmdb data output path')
    parser.add_argument('--json_path', type=str, default='E:\\zj\\dataset\\icdar2015 (2)\\detection\\test.json',help='path to gt json')
    parser.add_argument('--save_floder', type=str,default=r'E:\zj\dataset\icdar2015 (2)', help='path to save lmdb')
    args = parser.parse_args()

    data_dict = load_gt(args.json_path)
    out_lmdb = os.path.join(args.save_floder,'train')
    createDataset(out_lmdb, data_dict, map_size=79951162)
