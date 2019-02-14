#-*-coding:utf-8-*-

import os, sys
import json

P = 0.5
MIN_TWEET = 1600
MIN_RT = 50

#読み込みディレクトリ，ファイル
READ_TEXT_DIR = "../DATA/04.16P_TWEETTEXT_TEXT_FILTER/"
READ_FEE_FILE = "../DATA/19.16P_RT_FAV_USER_MBTI/new_16p_user_rt_"+str(int(P*100)).zfill(3)+"_"+str(MIN_RT).zfill(2)+".json"###
#READ_FEE_FILE = "../DATA/19.16P_RT_FAV_USER_MBTI/16p_user_rt_"+str(int(P*100)).zfill(3)+"_"+str(MIN_RT).zfill(2)+"_"+str(MIN_TWEET).zfill(4)+".json"###

#書き込みディレクトリ, ファイル
WRITE_DIR = "../DATA/09.DATASET_ALL/"
if os.path.exists(WRITE_DIR) == False:
    os.mkdir(WRITE_DIR)
WRITE_FILE = WRITE_DIR+"new_rt_mbti_ratio_"+str(int(P*100)).zfill(3)+"_"+str(MIN_RT).zfill(2)+"_"+str(MIN_TWEET).zfill(4)+".json"###
#WRITE_FILE = WRITE_DIR+"rt_mbti_ratio_"+str(int(P*100)).zfill(3)+"_"+str(MIN_RT).zfill(2)+"_"+str(MIN_TWEET).zfill(4)+".json"###

if __name__ == '__main__':

    #FEEの読み込み
    with open(READ_FEE_FILE,"r") as fread:
        fee_dict = json.load(fread)
    
    count = 0
    write_dict = {}
    for year in range(2017, 2019):
        for month in range(1, 13):
            ym = str(year)+str(month).zfill(2)
            with open(READ_TEXT_DIR+ym+".json","r") as fread:
                tweet_dict = json.load(fread)
            for user_id in list(tweet_dict):
                if len(tweet_dict[user_id]) < MIN_TWEET:
                    continue

                count += 1
                print(count)

                if not user_id in write_dict:
                    write_dict[user_id] = {}

                mbti_list = [0]*40                    
                for i, mbti in enumerate(["EI","NS","TF","JP"]):
                    if user_id in list(fee_dict):
                        ratio = fee_dict[user_id]["ratio_"+mbti[0]]
                        print(ym,ratio)
                        if ratio != -1:
                            index = [int(ratio * 10) if int(ratio * 10) != 10 else 9][0] + i*10
                            mbti_list[index] = 1
                    else:
                        continue
                write_dict[user_id] = mbti_list
                
    with open(WRITE_FILE,"w") as fwrite:
        json.dump(write_dict, fwrite, indent = 4, ensure_ascii = False)
