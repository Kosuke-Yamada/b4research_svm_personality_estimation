#-*-coding:utf-8-*-

import os, sys
import json

MIN_TWEET = 400

#読み込みディレクトリ，ファイル
READ_TEXT_DIR = "../DATA/04.16P_TWEETTEXT_TEXT_FILTER/"
READ_MBTI_DIR = "../DATA/03.16P_MBTI/"

#書き込みディレクトリ, ファイル
WRITE_DIR = "../DATA/09.DATASET_ALL/"###
if os.path.exists(WRITE_DIR) == False:
    os.mkdir(WRITE_DIR)
WRITE_FILE = WRITE_DIR+"mbti_"+str(MIN_TWEET).zfill(4)+".json"

if __name__ == '__main__':

    count = 0
    write_dict = {}
    for year in range(2017, 2019):
        for month in range(1, 13):
            ym = str(year)+str(month).zfill(2)
            with open(READ_TEXT_DIR+ym+".json","r") as fread:
                tweet_dict = json.load(fread)
            mbti_dict = {}
            with open(READ_MBTI_DIR+str(ym)+".json","r") as fread:
                user_list = json.load(fread)[ym]
            for user_dict in user_list:
                mbti_dict[user_dict['user']['id_str']] = {}
                for mbti in ["EI","NS","TF","JP"]:
                    mbti_dict[user_dict['user']['id_str']]['mbti_'+mbti] = user_dict['mbti_'+mbti]
            for user_id in list(tweet_dict):
                if len(tweet_dict[user_id]) < MIN_TWEET:
                    continue
                
                count += 1
                print(count)
            
                write_dict[user_id] = {}
                for mbti in ["EI","NS","TF","JP"]:
                    write_dict[user_id]['mbti_'+mbti] = mbti_dict[user_id]['mbti_'+mbti]
                
    with open(WRITE_FILE,"w") as fwrite:
        json.dump(write_dict, fwrite, indent = 4, ensure_ascii = False)
