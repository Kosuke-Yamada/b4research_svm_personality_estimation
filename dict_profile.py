#-*-coding:utf-8-*-

import os, sys
import MeCab
from collections import Counter
import json

#書き込みディレクトリ, ファイル
WRITE_DIR = "../DATA/08.DICT_ALL/"############
if os.path.exists(WRITE_DIR) == False:
    os.mkdir(WRITE_DIR)
WRITE_FILE = WRITE_DIR + "dict_profile.json"

if __name__ == '__main__':

    index = 0 
    index_dict = {}

    for i in range(0,130,20):
        key = "count_des_char_"+str(i).zfill(3)+"-"+str(i+19).zfill(3)
        index_dict[key] = index
        index += 1
    index_dict["count_des_char_140-"] = index
    index += 1
    
    index_dict["log_count_followee_-04"] = index
    index += 1
    for i in range(5,10,2):
        key = "log_count_followee_"+str(i).zfill(2)+"-"+str(i+1).zfill(2)
        index_dict[key] = index
        index += 1
    index_dict["log_count_followee_11-"] = index
    index += 1

    index_dict["log_count_follower_-04"] = index
    index += 1
    for i in range(5,10,2):
        key = "log_count_follower_"+str(i).zfill(2)+"-"+str(i+1).zfill(2)
        index_dict[key] = index
        index += 1
    index_dict["log_count_follower_11-"] = index
    index += 1

    index_dict["log_friends_followers_ratio_--1.0"] = index
    index += 1
    for i in range(-2,4,1):
        key = "log_friends_followers_ratio_"+str(i/2).zfill(2)+"-"+str(i/2+0.5).zfill(2)
        index_dict[key] = index
        index += 1
    index_dict["log_friends_followers_ratio_2.0-"] = index
    index += 1

    index_dict["log_count_statises_-06"] = index
    index += 1
    for i in range(7,16,2):
        key = "log_count_statuses_"+str(i).zfill(2)+"-"+str(i+1).zfill(2)
        index_dict[key] = index
        index += 1
    index_dict["log_count_statuses_17-"] = index
    index += 1  

    index_dict["log_count_favourites_-06"] = index
    index += 1
    for i in range(7,16,2):
        key = "log_count_favourites_"+str(i).zfill(2)+"-"+str(i+1).zfill(2)
        index_dict[key] = index
        index += 1
    index_dict["log_count_favourites_17-"] = index
    index += 1

    index_dict["log_favourites_statuses_ratio_--3.0"] = index
    index += 1
    for i in range(-6,2,1):
        key = "log_favourites_statuses_ratio_"+str(i/2)+"-"+str(i/2+0.5)
        index_dict[key] = index
        index += 1
    index_dict["log_favourites_statuses_ratio_1.0-"] = index
    index += 1                                            

    index_dict["log_statuses_day_ratio_-00"] = index
    index += 1
    for i in range(0,6,1):
        key = "log_statuses_day_ratio_"+str(i).zfill(2)+"-"+str(i+1).zfill(2)
        index_dict[key] = index
        index += 1
    index_dict["log_statuses_day_ratio_06-"] = index
    index += 1
        
    index_dict["log_favorurites_day_ratio_--2"] = index
    index += 1
    for i in range(-2,6,1):
        key = "log_favorurites_day_ratio_"+str(i)+"-"+str(i+1)
        index_dict[key] = index
        index += 1
    index_dict["log_favorurites_day_ratio_6-"] = index
    index += 1

    index_dict["log_day_since_created_at_-5"] = index
    index += 1
    for i in range(6,12,1):
        key = "log_day_since_created_at_"+str(i)+"-"+str(i+1)
        index_dict[key] = index
        index += 1
    index_dict["log_day_since_created_at_12-"] = index
    index += 1

    print(index_dict)
    with open(WRITE_FILE,"w") as fwrite:
        json.dump(index_dict, fwrite, indent = 4, ensure_ascii = False)
    
