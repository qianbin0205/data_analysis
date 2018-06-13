from tools import *
from nltk.text import TextCollection
from sklearn.naive_bayes import GaussianNB
import os
import pandas as pd
import nltk

data_path = './dataset'
output_text_filename = 'raw_weibo_test.csv'
output_cln_text_filename = 'clean_weibo_test.csv'
is_first_run = True


def redo_data(dataset_path=data_path):
    file_list_source = os.listdir(dataset_path)
    file_list = [f for f in file_list_source
                 if 'simplifyweibo' in f and f.endswith('.txt')]
    os.chdir(dataset_path)
    text_w_lable_df_list = []
    for f in file_list:
        label = int(f[0])
        f = open(f, 'r+', encoding='utf-8')
        lines = f.read().splitlines()
        f.close()
        labels = [label] * len(lines)
        text_ser = pd.Series(lines)
        labels_ser = pd.Series(labels)
        text_w_lable_df = pd.concat([labels_ser, text_ser], axis=1)
        text_w_lable_df_list.append(text_w_lable_df)

    result_df = pd.concat(text_w_lable_df_list, axis=0)
    result_df.columns = ['label', 'text']
    result_df.to_csv(output_text_filename, index=None, encoding='utf-8')


