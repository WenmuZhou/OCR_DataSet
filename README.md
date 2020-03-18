# Todo

- [ ] 提供数据集百度云链接
- [ ] 数据集转换为统一格式
- [ ] 提供读取脚本




# 数据集

| 数据集                            | 主页                                                         | 适用情况  | 数据情况                                                     | 标注形式                                                     | 说明                                                         |
| --------------------------------- | ------------------------------------------------------------ | --------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ICDAR2015                         | https://rrc.cvc.uab.es/?ch=4                                 | 检测&识别 | 语言: 英文     train:1,000     test:500                      | x1, y1, x2, y2, x3, y3, x4, y4, transcription                | 坐标: x1, y1, x2, y2, x3, y3, x4,  y4     transcription : 框内的文字信息 |
| MLT2019                           | https://rrc.cvc.uab.es/?ch=15                | 检测&识别 | 语言: 混合     train:10,000     test:10,000                  | x1,y1,x2,y2,x3,y3,x4,y4,script,transcription                 | 坐标: x1, y1, x2, y2, x3, y3, x4,  y4     script: 文字所属语言     transcription : 框内的文字信息 |
| COCO-Text                         | https://rrc.cvc.uab.es/?ch=5                                 | 检测&识别 | 语言: 混合     train:43,686     validation:10,000     test:10,000 | json                                                         |                                                              |
| ReCTS                             | https://rrc.cvc.uab.es/?ch=12&com=introduction               | 检测&识别 | 语言: 混合     train:20,000     test:5,000                   | {       “chars”: [         {“points”:  [x1,y1,x2,y2,x3,y3,x4,y4], “transcription” : “trans1”, "ignore":0  },         {“points”:  [x1,y1,x2,y2,x3,y3,x4,y4], “transcription” : “trans2”, " ignore ":0  }],       “lines”: [         {“points”:  [x1,y1,x2,y2,x3,y3,x4,y4] , “transcription” : “trans3”, "ignore ":0  }],     } | points: x1,y1,x2,y2,x3,y3,x4,y4       chars: 字符级别的标注     lines: 行级别的标注.      transcription : 框内的文字信息     ignore: 0:不忽略，1:忽略 |
| SROIE                             | https://rrc.cvc.uab.es/?ch=13                                | 检测&识别 | 语言: 英文     train:699     test:400                        | x1, y1, x2, y2, x3, y3, x4, y4, transcription                | 坐标: x1, y1, x2, y2, x3, y3, x4,  y4     transcription : 框内的文字信息 |
| ArT                               | https://rrc.cvc.uab.es/?ch=14                                | 检测&识别 | 语言: 混合     train: 5,603     test: 4,563                  | {     “gt_1”: [  {“points”: [[x1, y1], [x2, y2], …, [xn,  yn]], “transcription” : “trans1”, “language” : “Latin”,  "illegibility": false },             {“points”: [[x1, y1],  [x2, y2], …, [xn, yn]], “transcription” : “trans2”, “language” : “Chinese”,  "illegibility": false }],     } | points:  x1,y1,x2,y2,x3,y3,x4,y4…xn,yn      transcription : 框内的文字信息     language: 语言信息     illegibility: 是否模糊 |
| LSVT                              | https://rrc.cvc.uab.es/?ch=16                                | 检测&识别 | 语言: 混合     全标注     train: 30,000     test: 20,000     只标注文本     400,000 | {     “gt_1”: [  {“points”: [[x1, y1], [x2, y2], …, [xn,  yn]], “transcription” : “trans1”, "illegibility": false },             {“points”: [[x1, y1],  [x2, y2], …, [xn, yn]], “transcription” : “trans2”, "illegibility":  false }],     } | points:  x1,y1,x2,y2,x3,y3,x4,y4…xn,yn      transcription : 框内的文字信息     illegibility: 是否模糊 |
| Synth800k                         | http://www.robots.ox.ac.uk/~vgg/data/scenetext/              | 检测&识别 | 语言: 英文     800,000                                       | imnames:      wordBB:      charBB:      txt:                 | imnames: 文件名称     wordBB: 2*4*n,每张图像内的文本框     charBB: 2*4*n,每张图像内的字符框     txt: 每张图形内的字符串 |
| mjsynth                           | http://www.robots.ox.ac.uk/~vgg/data/text/                   | 识别      | 语言: 英文     9,000,000                                     | -                                                            | -                                                            |
| Synthetic Chinese String  Dataset | 链接：https://pan.baidu.com/s/1Js-lK6j2DBXPMLLjaDbchg <br/>提取码：2ect | 识别      | 语言: 混合     300k                                          |                                                              |                                                              |

# 数据生成工具

 https://github.com/TianzhongSong/awesome-SynthText 