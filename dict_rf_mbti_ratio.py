#-*-coding:utf-8-*-

import os, sys
import MeCab
from collections import Counter
import json

#書き込みディレクトリ, ファイル
WRITE_DIR = "../DATA/08.DICT_ALL/"############
if os.path.exists(WRITE_DIR) == False:
    os.mkdir(WRITE_DIR)
WRITE_FILE = WRITE_DIR + "dict_rt_mbti_ratio.json"

if __name__ == '__main__':

    index = 0 
    index_dict = {}

    for mbti in ["EI","NS","TF","JP"]:
        for i in range(10):
            key = "rt_"+mbti+"_"+str(round(i/10,1))+"-"+str(round(i/10+0.1,1))
            index_dict[key] = index
            index += 1

    with open(WRITE_FILE,"w") as fwrite:
        json.dump(index_dict, fwrite, indent = 4, ensure_ascii = False)
    
