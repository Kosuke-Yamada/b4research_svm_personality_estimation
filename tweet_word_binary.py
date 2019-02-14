#-*-coding:utf-8-*-

import os, sys
import MeCab
from collections import Counter
import json
import neologdn

MAX_WORDS = 10000
MIN_TWEET = 1600
NUM_TWEET = 12

#読み込みディレクトリ，ファイル
READ_DICT_FILE = "../DATA/08.DICT_ALL/dict_tweet_"+str(NUM_TWEET).zfill(4)+"_"+str(MIN_TWEET).zfill(4)+"_"+str(MAX_WORDS)+".json"###
READ_TEXT_DIR = "../DATA/04.16P_TWEETTEXT_TEXT_FILTER/"

#書き込みディレクトリ, ファイル
WRITE_DIR = "../DATA/09.DATASET_ALL/"###
if os.path.exists(WRITE_DIR) == False:
    os.mkdir(WRITE_DIR)
WRITE_FILE = WRITE_DIR+"tweet_word_binary_"+str(NUM_TWEET).zfill(4)+"_"+str(MIN_TWEET).zfill(4)+"_"+str(MAX_WORDS)+".json"

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

    #辞書の読み込み
    with open(READ_DICT_FILE,"r") as fread:
        index_dict = json.load(fread)

    #テキストデータの読み込み
    read_ym_tweet_dict = {}
    count = 0
    write_dict = {}
    for year in range(2017, 2019):
        for month in range(1, 13):
            with open(READ_TEXT_DIR+str(year)+str(month).zfill(2)+".json","r") as fread:
                tweet_dict = json.load(fread)
            for user_id in list(tweet_dict):
                if len(tweet_dict[user_id]) < MIN_TWEET:
                    continue
                
                count += 1
                print(count)
            
                #テキストをインデックスにする処理
                user_word_list = []
                for j, text in enumerate(tweet_dict[user_id]):
                    user_word_list += tweet_text2mecab(text)
                    if j ==  NUM_TWEET-1:
                        break
                
                user_index_list = []
                for word in list(set(user_word_list)):
                    if word in index_dict:
                        user_index_list.append(int(index_dict[word]))
                user_index_list = sorted(user_index_list)

                user_word_binary_list = [0] * (max(index_dict.values())+1)
                for user_index in user_index_list:
                    user_word_binary_list[user_index] = 1

                #辞書に素性を追加する
                write_dict[user_id] = user_word_binary_list

    #データの書き込み
    with open(WRITE_FILE,"w") as fwrite:
        json.dump(write_dict, fwrite, indent = 4, ensure_ascii = False)
