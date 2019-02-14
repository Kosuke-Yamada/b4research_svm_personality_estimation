#-*-coding:utf-8-*-

import os, sys
from collections import Counter
import json
import math

MIN_TWEET = 1600

#読み込みディレクトリ，ファイル
READ_TEXT_DIR = "../DATA/04.16P_TWEETTEXT_TEXT_FILTER/"
READ_MBTI_DIR = "../DATA/03.16P_MBTI/"

#書き込みディレクトリ, ファイル
WRITE_DIR = "../DATA/09.DATASET_ALL/"
if os.path.exists(WRITE_DIR) == False:
    os.mkdir(WRITE_DIR)
WRITE_FILE = WRITE_DIR+"profile_binary_"+str(MIN_TWEET).zfill(4)+".json"

if __name__ == '__main__':

    #テキストデータの読み込み
    count = 0
    write_dict = {}
    for year in range(2017, 2019):
        for month in range(1, 13):
            ym = str(year)+str(month).zfill(2)
            with open(READ_TEXT_DIR+ym+".json","r") as fread:
                tweet_dict = json.load(fread)
            with open(READ_MBTI_DIR+str(ym)+".json","r") as fread:
                user_list = json.load(fread)[ym]
            for user_id in list(tweet_dict):
                if len(tweet_dict[user_id]) < MIN_TWEET:
                    continue

                count += 1
                print(count)
            
                #MBTI_DICT
                for user_dict in user_list:
                    if user_dict['user']['id_str'] == str(user_id):
                        user_mbti_dict = user_dict
                        break
            
                profile_list = []

                p = user_mbti_dict['user']['description_char_count']
                p = [p//20 if p < 140 else 7][0]
                p_list = [0] * 8
                p_list[p] = 1
                profile_list += p_list

                c = user_mbti_dict['user']['friends_count']
                c = [c if c != 0 else 1][0]
                p = math.log2(c)
                p = [0 if p < 5 else int((p-3)//2) if p < 11 else 4][0]
                p_list = [0] * 5
                p_list[p] = 1
                profile_list += p_list
                
                c = user_mbti_dict['user']['followers_count']
                c = [c if c != 0 else 1][0]
                p = math.log2(c)
                p = [0 if p < 5 else int((p-3)//2) if p < 11 else 4][0]
                p_list = [0] * 5
                p_list[p] = 1
                profile_list += p_list

                c = user_mbti_dict['user']['friends_followers_ratio']
                c = [c if c != 0 else 1][0]
                p = math.log2(c)
                p = [0 if p < -1 else int(p*2+3) if p < 2 else 7][0]
                p_list = [0] * 8
                p_list[p] = 1
                profile_list += p_list

                c = user_mbti_dict['user']['statuses_count']
                c = [c if c != 0 else 1][0]
                p = math.log2(c)
                p = [0 if p < 7 else int((p-5)//2) if p < 17 else 6][0]
                p_list = [0] * 7
                p_list[p] = 1
                profile_list += p_list

                c = user_mbti_dict['user']['favourites_count']
                c = [c if c != 0 else 1][0]
                p = math.log2(c)
                p = [0 if p < 7 else int((p-5)//2) if p < 17 else 6][0]
                p_list = [0] * 7
                p_list[p] = 1
                profile_list += p_list
                
                c = user_mbti_dict['user']['favourites_statuses_ratio']
                c = [c if c != 0 else 1][0]
                p = math.log2(c)
                p = [0 if p < -3 else int(p*2+7) if p < 1 else 9][0]
                p_list = [0] * 10
                p_list[p] = 1
                profile_list += p_list

                c = user_mbti_dict['user']['statuses_day_ratio']
                c = [c if c != 0 else 1][0]
                p = math.log2(c)
                p = [0 if p < 0 else int(p) if p < 6 else 7][0]
                p_list = [0] * 8
                p_list[p] = 1
                profile_list += p_list

                c = user_mbti_dict['user']['favorurites_day_ratio']
                c = [c if c != 0 else 1][0]
                p = math.log2(c)
                p = [0 if p < -2 else int(p+3) if p < 6 else 9][0]
                p_list = [0] * 10
                p_list[p] = 1
                profile_list += p_list

                c = user_mbti_dict['user']['day_since_created_at']
                c = [c if c != 0 else 1][0]
                p = math.log2(c)
                p = [0 if p < 5 else int(p-5) if p < 12 else 7][0]
                p_list = [0] * 8
                p_list[p] = 1
                profile_list += p_list

                print(len(profile_list))
                write_dict[user_id] = profile_list
            
    #データの書き込み
    with open(WRITE_FILE,"w") as fwrite:
        json.dump(write_dict, fwrite, indent = 4, ensure_ascii = False)
