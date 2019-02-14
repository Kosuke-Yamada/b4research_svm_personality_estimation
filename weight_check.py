#-*-coding:utf-8-*-

import numpy as np
import json
import os, sys
from sklearn.externals import joblib

NUM = 8
MBTI = "JP"
NUM_TEST = 2

MAX_WORDS = 10000
MIN_TWEET = 1600
NUM_TWEET = 1600

GET_NUM = 500

READ_DICT_DIR = "../DATA/08.DICT_ALL/"
READ_DICT_FILE_01 = READ_DICT_DIR+"dict_tweet_"+str(NUM_TWEET).zfill(4)+"_"+str(MIN_TWEET).zfill(4)+"_"+str(MAX_WORDS)+".json"
READ_DICT_FILE_02 = READ_DICT_DIR+"dict_des_"+str(MIN_TWEET).zfill(4)+"_"+str(MAX_WORDS)+".json"
READ_DICT_FILE_03 = READ_DICT_DIR+"dict_profile.json"
READ_DICT_FILE_04 = READ_DICT_DIR+"dict_rt_mbti_ratio.json"
READ_DICT_FILE_05 = READ_DICT_DIR+"dict_fav_mbti_ratio.json"
READ_DICT_LIST = [READ_DICT_FILE_01, READ_DICT_FILE_02, READ_DICT_FILE_03]#, READ_DICT_FILE_03]

READ_MODEL_FILE = "../DATA/10.SVM_AUC_ALL/best_model/"+str(MBTI)+"_"+str(NUM).zfill(2)+"/"+str(NUM_TEST).zfill(2)+".sav"

#辞書情報
def info_dict(dict_list):
    index_dict = {}
    max_features = 0
    for i, read_file in enumerate(dict_list):###
        with open(read_file, "r") as fread:
            read_dict = json.load(fread)
        for key in list(read_dict):
            index_dict[key+"_"+str(i)] = int(read_dict[key]) + max_features
        max_features = max(index_dict.values()) + 1
    return max_features, index_dict
    
#メインプログラム
if __name__ == '__main__':
    
    #辞書データ
    max_features, word2index = info_dict(READ_DICT_LIST)

    index2word = {v:k for k, v in word2index.items()}   
    model = joblib.load(READ_MODEL_FILE)
    
    coef_list = model.coef_[0].tolist()
    coef_dict = {}
    for index, coef in enumerate(coef_list):
        coef_dict[index] = coef
    coef_dict = sorted(coef_dict.items(), key = lambda x:-x[1])
    
    flag_stop = 0
    for i, (index, value) in enumerate(coef_dict):
        if i < GET_NUM:
            print(str(i)+"\t{0:.4f}\t".format(value)+str(index)+"\t"+index2word[index])
        
        if max_features-GET_NUM-1 < i:
           print(str(i)+"\t{0:.4f}\t".format(value)+str(index)+"\t"+index2word[index])
         
        #if index >= 20073:
        #    print(str(i)+"\t{0:.4f}\t".format(value)+str(index)+"\t"+index2word[index])

        #if value < 0 and flag_stop == 0:
        #    print()
        #    flag_stop = 1
