#-*-coding:utf-8-*-

import numpy as np
from sklearn.svm import LinearSVC
from keras.preprocessing import sequence
from sklearn.metrics import roc_curve, auc
import json
from sklearn.externals import joblib
import os
from statistics import mean

NUM = 16
MBTI = "TF"
P = 0.5
MIN_FR = 50
NUM_TWEET = 1600
MIN_TWEET = 1600
MAX_WORDS = 10000
WEIGHT_PARAM = None#'balanced'   

READ_DICT_DIR = "../DATA/08.DICT_ALL/"
READ_DICT_FILE_01 = READ_DICT_DIR+"dict_tweet_"+str(NUM_TWEET).zfill(4)+"_"+str(MIN_TWEET).zfill(4)+"_"+str(MAX_WORDS)+".json"
READ_DICT_FILE_02 = READ_DICT_DIR+"dict_des_"+str(MIN_TWEET).zfill(4)+"_"+str(MAX_WORDS)+".json"
READ_DICT_FILE_03 = READ_DICT_DIR+"dict_profile.json"
READ_DICT_FILE_04 = READ_DICT_DIR+"dict_fav_mbti_ratio.json"
READ_DICT_FILE_05 = READ_DICT_DIR+"dict_rt_mbti_ratio.json"
READ_DICT_LIST = [READ_DICT_FILE_01, READ_DICT_FILE_02, READ_DICT_FILE_03]

READ_FILE_DIR = "../DATA/09.DATASET_ALL/"
READ_FILE_00 = READ_FILE_DIR+"mbti_"+str(MIN_TWEET).zfill(4)+".json"
READ_FILE_01 = READ_FILE_DIR+"tweet_word_binary_"+str(NUM_TWEET).zfill(4)+"_"+str(MIN_TWEET).zfill(4)+"_"+str(MAX_WORDS)+".json"
READ_FILE_02 = READ_FILE_DIR+"des_word_binary_"+str(MIN_TWEET).zfill(4)+"_"+str(MAX_WORDS)+".json"
READ_FILE_03 = READ_FILE_DIR+"profile_binary_"+str(MIN_TWEET).zfill(4)+".json"
READ_FILE_04 = READ_FILE_DIR+"fav_mbti_ratio_"+str(int(P*100)).zfill(3)+"_"+str(MIN_FR).zfill(2)+"_"+str(MIN_TWEET).zfill(4)+".json"
READ_FILE_05 = READ_FILE_DIR+"rt_mbti_ratio_"+str(int(P*100)).zfill(3)+"_"+str(MIN_FR).zfill(2)+"_"+str(MIN_TWEET).zfill(4)+".json"
READ_FILE_LIST = [READ_FILE_00, READ_FILE_01, READ_FILE_02, READ_FILE_03]#, READ_FILE_03, READ_FILE_04, READ_FILE_05]

WRITE_BEST_MODEL_DIR = "../DATA/10.SVM_AUC_ALL/best_model/"+str(MBTI)+"_"+str(NUM).zfill(2)+"/"
if os.path.exists(WRITE_BEST_MODEL_DIR) == False:
    os.makedirs(WRITE_BEST_MODEL_DIR)
        
#辞書情報
def info_dict(dict_list):
    index_dict = {}
    max_features = 0
    for read_file in dict_list:
        with open(read_file, "r") as fread:
            read_dict = json.load(fread)
        for key in list(read_dict):
            index_dict[key] = int(read_dict[key]) + max_features
        max_features = max(index_dict.values()) + 1
    return max_features
    
#学習データ情報
def info_num_data(read_file):
    with open(read_file, "r") as fread:
        read_dict = json.load(fread)
    num_data = len(list(read_dict))
    return num_data

#特徴ベクトル作成
def make_feature_vector(read_file_list, max_features, num_data, mbti):
    x = np.empty((num_data, ), dtype = list)
    y = np.zeros((num_data, ))
    for i in range(num_data):
        x[i] = []
    for read_file in read_file_list:
        with open(read_file, "r") as fread:
            read_dict = json.load(fread)
        if "mbti_"+str(MIN_TWEET).zfill(4) in read_file:
            for i, user_id in enumerate(list(read_dict)):
                y[i] = read_dict[user_id]['mbti_'+str(mbti)]
        else:
            for i, user_id in enumerate(list(read_dict)):
                x[i] += read_dict[user_id]
    x = sequence.pad_sequences(x, maxlen = max_features)
    return x, y

def print_confusion_matrix(xtest, ytest, model, max_features):
    tp = 0
    fn = 0
    fp = 0
    tn = 0
    for i in range(len(xtest)):
        xdata = xtest[i].reshape(1, max_features)
        ylabel = int(ytest[i])
        ypred = model.predict(xdata)[0]
        ypred = [1 if ypred >= 0.5 else 0][0]
        if (ylabel == ypred) and (ylabel == 1):
            tp += 1
        if (ylabel != ypred) and (ylabel == 1):
            fn += 1
        if (ylabel != ypred) and (ylabel == 0):
            fp += 1
        if (ylabel == ypred) and (ylabel == 0):
            tn += 1
    sum_class_p = tp + fn
    sum_class_n = fp + tn
    sum_pred_p = tp + fp
    sum_pred_n = fn + tn
    sum_all = tp + fn + fp + tn
    precision_p = [float(tp / sum_pred_p) if sum_pred_p != 0 else 0][0]
    precision_n = [float(tn / sum_pred_n) if sum_pred_n != 0 else 0][0]
    recall_p = [float(tp / sum_class_p) if sum_class_p != 0 else 0][0]
    recall_n = [float(tn / sum_class_n) if sum_class_n != 0 else 0][0]
    fscore_p = [float((2 * precision_p * recall_p) / (precision_p + recall_p)) if (precision_p + recall_p) != 0 else 0][0]
    fscore_n = [float((2 * precision_n * recall_n) / (precision_n + recall_n)) if (precision_n + recall_n) != 0 else 0][0]            
    fscore = float((fscore_p + fscore_n) / 2)
    if sum_class_p > sum_class_n:
        maj = sum_class_p
        majority = float(sum_class_p / sum_all)
    else:
        maj = sum_class_n
        majority = float(sum_class_n / sum_all)
    accuracy = (tp + tn) / sum_all
    print("***Confusion Matrix***")
    print("\t"+"pred_p"+"\t"+"pred_n"+"\t"+"sum")
    print("class_p"+"\t"+str(tp)+"\t"+str(fn)+"\t"+str(sum_class_p))
    print("class_n"+"\t"+str(fp)+"\t"+str(tn)+"\t"+str(sum_class_n))
    print("sum"+"\t"+str(sum_pred_p)+"\t"+str(sum_pred_n)+"\t"+str(sum_all))
    print("***Score***")
    print("Precision_p\t= {0:.4f}".format(precision_p)+" ("+str(tp)+"/"+str(sum_pred_p)+")")
    print("Precision_n\t= {0:.4f}".format(precision_n)+" ("+str(tn)+"/"+str(sum_pred_n)+")")
    print("Recall_p\t= {0:.4f}".format(recall_p)+" ("+str(tp)+"/"+str(sum_class_p)+")")
    print("Recall_n\t= {0:.4f}".format(recall_n)+" ("+str(tn)+"/"+str(sum_class_n)+")")
    print("F-score_p\t= {0:.4f}".format(fscore_p))
    print("F-score_n\t= {0:.4f}".format(fscore_n))
    print("F-score\t\t= {0:.4f}".format(fscore))
    print("Majority\t= {0:.4f}".format(majority)+" ("+str(maj)+"/"+str(sum_all)+")")
    print("Accuracy\t= {0:.4f}".format(accuracy)+" ("+str(tp+tn)+"/"+str(sum_all)+")")
    
#ROC,AUCの出力
def print_roc_auc(xtest, ytest, model, max_features, flag_print):

    ypred_list = []
    for i in range(len(xtest)):
        xdata = xtest[i].reshape(1, max_features)
        ypred = model.decision_function(xdata)[0]
        ypred_list.append(ypred)
    ypred_list = np.array(ypred_list)
    fpr, tpr, thresholds = roc_curve(ytest, ypred_list)

    AUC = auc(fpr, tpr)
    if flag_print == 1:
        print("AUC\t\t= {0:.4f}".format(AUC)+"\n")
    
    return AUC

#メインプログラム
if __name__ == '__main__':
    
    #辞書データ
    max_features = info_dict(READ_DICT_LIST)
    
    #学習データ
    num_data = info_num_data(READ_FILE_00)
    
    #特徴ベクトル作成
    np.random.seed(1)
    x, y = make_feature_vector(READ_FILE_LIST, max_features, num_data, MBTI)
    xy = list(zip(x,y))
    np.random.shuffle(xy)
    x, y = zip(*xy)
    x = np.array(x)
    y = np.array(y)

    x_list = np.array_split(x, 10)
    y_list = np.array_split(y, 10)
    x_list2 = x_list + x_list
    y_list2 = y_list + y_list

    AUC_list = []
    all_ytest = []
    all_ypred = []
    for i, (x_test, y_test) in enumerate(zip(x_list, y_list)):
        print(i)
        
        x_dev = x_list2[i+1]
        x_train = np.concatenate((x_list2[i+2:i+10]), axis = 0)
        y_dev = y_list2[i+1]
        y_train = np.concatenate((y_list2[i+2:i+10]), axis = 0)
        
        #SVMモデル作成,学習
        max_AUC = 0
        c_param = 1
        flag_stop = 0
        while(flag_stop < 15):
            model = LinearSVC(C = c_param, class_weight = WEIGHT_PARAM)
            model.fit(x_train, y_train)
            AUC = print_roc_auc(x_dev, y_dev, model, max_features, 0)
            if max_AUC < AUC:
                max_c_param = c_param
                max_AUC = AUC
                best_model = model
                flag_stop = 0
            else:
                flag_stop += 1
            c_param /= 2

        print("***BEST_PARAM***")
        print("C\t\t= "+str(max_c_param))
        joblib.dump(best_model, WRITE_BEST_MODEL_DIR + str(i).zfill(2)+".sav")
        
        print("*********TEST_SCORE*********")
        print_confusion_matrix(x_test, y_test, best_model, max_features)
        AUC = print_roc_auc(x_test, y_test, best_model, max_features, 1)

        AUC_list.append(AUC)
        
        all_ytest += y_test.tolist()
        for i in range(len(x_test)):
            x_data = x_test[i].reshape(1, max_features)
            y_pred = best_model.decision_function(x_data)[0]
            all_ypred.append(y_pred)

    print("*********AUC_SCORE*********")
    for i, AUC in enumerate(AUC_list):
        print(str(i)+"       : {0:.4f}".format(AUC))
    print("Ave     : {0:.4f}\n".format(mean(AUC_list)))

    all_ytest = np.array(all_ytest)
    all_ypred = np.array(all_ypred)
    fpr, tpr, thresholds = roc_curve(all_ytest, all_ypred)
    AUC = auc(fpr, tpr)
    print("All_Ave : {0:.4f}".format(AUC))

    print()
    print(NUM, MBTI, WEIGHT_PARAM)
    for dict_name in READ_DICT_LIST:
        d, f = dict_name.rsplit("/",1)
        print(f)
    for file_name in READ_FILE_LIST:
        d, f = file_name.rsplit("/",1)
        print(f)
