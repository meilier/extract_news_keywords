import pandas as pd
import pdb
import jieba
import re
import jieba.analyse
import jieba.posseg
import numpy as np

#global
ways="just-noun-topk10"
label1 = []
label2 = []
# get data
data = pd.read_csv('../data/all_docs.txt',sep='\001',header=None)
data.columns = ['id','title','doc']

# get train
train = pd.read_csv('../data/train_docs_keywords.txt',sep='\t',header=None)
train.columns = ['id','label']
train_id_list = list(train['id'].unique())

# extract test set
test_title_doc = data[~data['id'].isin(train_id_list)]

#1. exclude number
test_title_doc['title_cut'] = test_title_doc['title'].apply(lambda x:''.join(filter(lambda ch: ch not in ' \t1234567890', str(x))))

#2. extract tags
test_title_doc['title_cut'] = test_title_doc['title_cut'].apply(lambda x:','.join(jieba.analyse.extract_tags(str(x),topK = 10)))

#3. extract quotes
test_title_doc['title_regex'] = test_title_doc['title'].apply(lambda x:','.join(re.findall(r"《(.+?)》",str(x))))

# 利用策略 + 规则 查看训练集的准确率
test_offline_result = test_title_doc[['id','id','title_cut','title_regex']]

for i in test_offline_result.values:
    result = str(i[1]).split(',')
    title_cut = str(i[2]).split(',')
    title_regex = str(i[3]).split(',')
    dic={}
    tmp_result=[]
    for x in jieba.posseg.cut(" ".join(title_cut)):
        dic[x.word]=x.flag
    if title_regex[0] == '':
        for v in title_cut:
            if  'n' in dic[v]:
                tmp_result.append(v)
    else:
        tmp_result = title_regex
        
    if len(tmp_result) > 1:
        label1.append(tmp_result[0])
        label2.append(tmp_result[1])
    elif len(tmp_result) == 1:
        label1.append(tmp_result[0])
        label2.append(tmp_result[0])
    else:
        label1.append('')
        label2.append('')

result = pd.DataFrame()

id = test_title_doc['id'].unique()

result['id'] = list(id)
result['label1'] = label1
result['label2'] = label2
result.to_csv('../result/result-{}.csv'.format(ways),index=None)