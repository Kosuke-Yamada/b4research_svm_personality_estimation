#-*-coding:utf-8-*-

import os, sys
import MeCab
from collections import Counter
import json
import neologdn#####

MAX_WORDS = 10000
MIN_TWEET = 800

#読み込みディレクトリ，ファイル
READ_TEXT_DIR = "../DATA/04.16P_TWEETTEXT_TEXT_FILTER/"
READ_MBTI_DIR = "../DATA/03.16P_MBTI/"

#書き込みディレクトリ, ファイル
WRITE_DIR = "../DATA/08.DICT_ALL/"
if os.path.exists(WRITE_DIR) == False:
    os.mkdir(WRITE_DIR)
WRITE_FILE = WRITE_DIR + "dict_des_"+str(MIN_TWEET).zfill(4)+"_"+str(MAX_WORDS)+".json"###

def tweet_text2mecab(tweet_text):
    #tweet_text = neologdn.normalize(str(tweet_text))
    tweet_text = str(tweet_text)
    chasen = MeCab.Tagger("-Ochasen")
    chasen_list = chasen.parse(tweet_text)
    chasen_list = chasen_list.split("\n")
    tweet_word_list = []
    for cha_list in chasen_list:
        cha_list = cha_list.split("\t")
        if len(cha_list) > 2:
            tweet_word_list.append(cha_list[2])
    return tweet_word_list

if __name__ == '__main__':

    total_word_list = []
    for year in range(2017,2019):
        for month in range(1,13):
            ym = str(year)+str(month).zfill(2)
            print(ym)
            with open(READ_TEXT_DIR+ym+".json","r") as fread:
                tweet_dict = json.load(fread)
            with open(READ_MBTI_DIR+str(ym)+".json","r") as fread:
                user_list = json.load(fread)[ym]
            for i, user_id in enumerate(list(tweet_dict)):
                print(ym, i)
                if len(tweet_dict[user_id]) < MIN_TWEET:
                    continue
                for user_dict in user_list:
                    if user_dict['user']['id_str'] == str(user_id):
                        user_mbti_dict = user_dict
                        break
                total_word_list += tweet_text2mecab(user_mbti_dict['user']['description_filter'])

    index_dict = {}
    counter = Counter(total_word_list)
    for index, (word, count) in enumerate(counter.most_common()):
        index_dict["des_"+word] = index
        if index == MAX_WORDS - 1:
            break
        
    with open(WRITE_FILE,"w") as fwrite:
        json.dump(index_dict, fwrite, indent = 4, ensure_ascii = False)
    
