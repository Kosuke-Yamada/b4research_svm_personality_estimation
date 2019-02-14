#-*-coding:utf-8-*-

import os, sys
import MeCab
from collections import Counter
import json
import neologdn

MAX_WORDS = 10000#50000
MIN_TWEET = 1600
NUM_TWEET = 3

#読み込みディレクトリ，ファイル
READ_DIR = "../DATA/04.16P_TWEETTEXT_TEXT_FILTER/"

#書き込みディレクトリ, ファイル
WRITE_DIR = "../DATA/08.DICT_ALL/"
if os.path.exists(WRITE_DIR) == False:
    os.mkdir(WRITE_DIR)
WRITE_FILE = WRITE_DIR + "dict_tweet_"+str(NUM_TWEET).zfill(4)+"_"+str(MIN_TWEET).zfill(4)+"_"+str(MAX_WORDS)+".json"

def tweet_text2mecab(tweet_text):
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
    for year in range(2017, 2019):
        for month in range(1, 13):
            ym = str(year)+str(month).zfill(2)
            with open(READ_DIR+ym+".json","r") as fread:
                tweet_dict = json.load(fread)
            for i, user_id in enumerate(list(tweet_dict)):
                print(ym, i)
                if len(tweet_dict[user_id]) < MIN_TWEET:
                    continue
                for j, text in enumerate(tweet_dict[user_id]):
                    total_word_list += tweet_text2mecab(text)
                    if j ==  NUM_TWEET-1:
                        break
                    
    counter = Counter(total_word_list)
    index_dict = {}
    for index, (word, count) in enumerate(counter.most_common()):
        index_dict[word] = index
        if index == MAX_WORDS - 1:
            break
        
    with open(WRITE_FILE,"w") as fwrite:
        json.dump(index_dict, fwrite, indent = 4, ensure_ascii = False)
    
