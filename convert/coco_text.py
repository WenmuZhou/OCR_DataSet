from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = 'andreasveit'
__version__ = '2.0'
# Interface for accessing the COCO-Text dataset.

# COCO-Text is a large dataset designed for text detection and recognition.
# This is a Python API that assists in loading, parsing and visualizing the 
# annotations. The format of the COCO-Text annotations is also described on 
# the project website http://vision.cornell.edu/se3/coco-text/. In addition to this API, please download both
# the COCO images and annotations.
# This dataset is based on Microsoft COCO. Please visit http://mscoco.org/
# for more information on COCO, including for the image data, object annotatins
# and caption annotations. 

# An alternative to using the API is to load the annotations directly
# into Python dictionary:
# with open(annotation_filename) as json_file:
#     coco_text = json.load(json_file)
# Using the API provides additional utility functions.

# The following API functions are defined:
#  COCO_Text  - COCO-Text api class that loads COCO annotations and prepare data structures.
#  getAnnIds  - Get ann ids that satisfy given filter conditions.
#  getImgIds  - Get img ids that satisfy given filter conditions.
#  loadAnns   - Load anns with the specified ids.
#  loadImgs   - Load imgs with the specified ids.
#  loadRes    - Load algorithm results and create API for accessing them.
# Throughout the API "ann"=annotation, "cat"=category, and "img"=image.

# COCO-Text Toolbox.        Version 1.1
# Data and  paper available at:  http://vision.cornell.edu/se3/coco-text/
# Code based on Microsoft COCO Toolbox Version 1.0 by Piotr Dollar and Tsung-Yi Lin
# extended and adapted by Andreas Veit, 2016.
# Licensed under the Simplified BSD License [see bsd.txt]

import json
import datetime
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.path import Path
import numpy as np
import copy
import os

class COCO_Text:
    def __init__(self, annotation_file=None):
        """
        Constructor of COCO-Text helper class for reading and visualizing annotations.
        :param annotation_file (str): location of annotation file
        :return:
        """
        # load dataset
        self.dataset = {}
        self.anns = {}
        self.imgToAnns = {}
        self.catToImgs = {}
        self.imgs = {}
        self.cats = {}
        self.val = []
        self.test = []
        self.train = []
        if not annotation_file == None:
            assert os.path.isfile(annotation_file), "file does not exist"
            print('loading annotations into memory...')
            time_t = datetime.datetime.utcnow()
            dataset = json.load(open(annotation_file, 'r'))
            print(datetime.datetime.utcnow() - time_t)
            self.dataset = dataset
            self.createIndex()

    def createIndex(self):
        # create index
        print('creating index...')
        self.imgToAnns = {int(cocoid): self.dataset['imgToAnns'][cocoid] for cocoid in self.dataset['imgToAnns']}
        self.imgs      = {int(cocoid): self.dataset['imgs'][cocoid] for cocoid in self.dataset['imgs']}
        self.anns      = {int(annid): self.dataset['anns'][annid] for annid in self.dataset['anns']}
        self.cats      = self.dataset['cats']
        self.val       = [int(cocoid) for cocoid in self.dataset['imgs'] if self.dataset['imgs'][cocoid]['set'] == 'val']
        self.test      = [int(cocoid) for cocoid in self.dataset['imgs'] if self.dataset['imgs'][cocoid]['set'] == 'test']
        self.train     = [int(cocoid) for cocoid in self.dataset['imgs'] if self.dataset['imgs'][cocoid]['set'] == 'train']
        print('index created!')

    def info(self):
        """
        Print information about the annotation file.
        :return:
        """
        for key, value in self.dataset['info'].items():
            print('%s: %s'%(key, value))

    def filtering(self, filterDict, criteria):
        return [key for key in filterDict if all(criterion(filterDict[key]) for criterion in criteria)]

    def getAnnByCat(self, properties):
        """
        Get ann ids that satisfy given properties
        :param properties (list of tuples of the form [(category type, category)] e.g., [('readability','readable')] 
            : get anns for given categories - anns have to satisfy all given property tuples
        :return: ids (int array)       : integer array of ann ids
        """
        return self.filtering(self.anns, [lambda d, x=a, y=b:d[x] == y for (a,b) in properties])

    def getAnnIds(self, imgIds=[], catIds=[], areaRng=[]):
        """
        Get ann ids that satisfy given filter conditions. default skips that filter
        :param imgIds  (int array)     : get anns for given imgs
               catIds  (list of tuples of the form [(category type, category)] e.g., [('readability','readable')] 
                : get anns for given cats
               areaRng (float array)   : get anns for given area range (e.g. [0 inf])
        :return: ids (int array)       : integer array of ann ids
        """
        imgIds = imgIds if type(imgIds) == list else [imgIds]
        catIds = catIds if type(catIds) == list else [catIds]

        if len(imgIds) == len(catIds) == len(areaRng) == 0:
            anns = list(self.anns.keys())
        else:
            if not len(imgIds) == 0:
                anns = sum([self.imgToAnns[imgId] for imgId in imgIds if imgId in self.imgToAnns],[])
            else:
                anns = list(self.anns.keys())
            anns = anns if len(catIds)  == 0 else list(set(anns).intersection(set(self.getAnnByCat(catIds))))
            anns = anns if len(areaRng) == 0 else [ann for ann in anns if self.anns[ann]['area'] > areaRng[0] and self.anns[ann]['area'] < areaRng[1]]
        return anns

    def getImgIds(self, imgIds=[], catIds=[]):
        '''
        Get img ids that satisfy given filter conditions.
        :param imgIds (int array) : get imgs for given ids
        :param catIds (int array) : get imgs with all given cats
        :return: ids (int array)  : integer array of img ids
        '''
        imgIds = imgIds if type(imgIds) == list else [imgIds]
        catIds = catIds if type(catIds) == list else [catIds]

        if len(imgIds) == len(catIds) == 0:
            ids = list(self.imgs.keys())
        else:
            ids = set(imgIds)
            if not len(catIds) == 0:
                ids  = ids.intersection(set([self.anns[annid]['image_id'] for annid in self.getAnnByCat(catIds)]))
        return list(ids)

    def loadAnns(self, ids=[]):
        """
        Load anns with the specified ids.
        :param ids (int array)       : integer ids specifying anns
        :return: anns (object array) : loaded ann objects
        """
        if type(ids) == list:
            return [self.anns[id] for id in ids]
        elif type(ids) == int:
            return [self.anns[ids]]

    def loadImgs(self, ids=[]):
        """
        Load anns with the specified ids.
        :param ids (int array)       : integer ids specifying img
        :return: imgs (object array) : loaded img objects
        """
        if type(ids) == list:
            return [self.imgs[id] for id in ids]
        elif type(ids) == int:
            return [self.imgs[ids]]

    def showAnns(self, anns, show_mask=False):
        """
        Display the specified annotations.
        :param anns (array of object): annotations to display
        :return: None
        """
        if len(anns) == 0:
            return 0
        ax = plt.gca()
        boxes = []
        color = []
        for ann in anns:
            c = np.random.random((1, 3)).tolist()[0]
            if show_mask:
                verts = list(zip(*[iter(ann['mask'])] * 2)) + [(0, 0)]
                codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 2) + [Path.CLOSEPOLY]
                path = Path(verts, codes)
                patch = PathPatch(path, facecolor='none')
                boxes.append(patch)
                text_x, text_y = verts[0]
            else:
                left, top, width, height = ann['bbox']
                boxes.append(Rectangle([left,top],width,height,alpha=0.4))
                text_x, text_y = left, top
            color.append(c)
            if 'utf8_string' in list(ann.keys()):
                ax.annotate(ann['utf8_string'],(text_x, text_y-4),color=c)
        p = PatchCollection(boxes, facecolors=color, edgecolors=(0,0,0,1), linewidths=3, alpha=0.4)
        ax.add_collection(p)

    def loadRes(self, resFile):
        """
        Load result file and return a result api object.
        :param   resFile (str)     : file name of result file
        :return: res (obj)         : result api object
        """
        res = COCO_Text()
        res.dataset['imgs'] = [img for img in self.dataset['imgs']]

        print('Loading and preparing results...     ')
        time_t = datetime.datetime.utcnow()
        if type(resFile) == str:
            anns = json.load(open(resFile))
        else:
            anns = resFile
        assert type(anns) == list, 'results in not an array of objects'
        annsImgIds = [int(ann['image_id']) for ann in anns]

        if set(annsImgIds) != (set(annsImgIds) & set(self.getImgIds())):
            print('Results do not correspond to current coco set')
            print('skipping ', str(len(set(annsImgIds)) - len(set(annsImgIds) & set(self.getImgIds()))), ' images')
        annsImgIds = list(set(annsImgIds) & set(self.getImgIds()))

        res.imgToAnns = {cocoid : [] for cocoid in annsImgIds}
        res.imgs = {cocoid: self.imgs[cocoid] for cocoid in annsImgIds}

        assert anns[0]['bbox'] != [], 'results have incorrect format'
        for id, ann in enumerate(anns):
            if ann['image_id'] not in annsImgIds:
                continue
            bb = ann['bbox']
            ann['area'] = bb[2]*bb[3]
            ann['id'] = id
            res.anns[id] = ann
            res.imgToAnns[ann['image_id']].append(id)
        print('DONE (t=%0.2fs)'%((datetime.datetime.utcnow() - time_t).total_seconds()))

        return res