import pandas as pd
import jieba
import re
import jieba.analyse
import numpy as np

#jieba.load_userdict("../data/baidu.txt")

allow_pos = ('nr')
# get data
data = pd.read_csv('../data/all_docs.txt',sep='\001',header=None)
data.columns = ['id','title','doc']

#get train
train = pd.read_csv('../data/train_docs_keywords.txt',sep='\t',header=None)
train.columns = ['id','label']
train_id_list = list(train['id'].unique())

train_title_doc = data[data['id'].isin(train_id_list)]

test_title_doc = data[~data['id'].isin(train_id_list)]

train_title_doc = pd.merge(train_title_doc,train,on=['id'],how='inner')




#1.  exclude useless numbers
train_title_doc['title_cut'] = train_title_doc['title'].apply(lambda x:''.join(filter(lambda ch: ch not in ' \t1234567890', x)))


#2. extract key words
train_title_doc['title_cut'] = train_title_doc['title_cut'].apply(lambda x:','.join(jieba.analyse.textrank(x,allowPOS=('nr','nt','ns','nz','s','n', 'vn','v'),topK = 8)))



#3. extract quotes
train_title_doc['title_regex'] = train_title_doc['title'].apply(lambda x:','.join(re.findall(r"《(.+?)》",x)))


# we run train
train_offline_result = train_title_doc[['id','label','title_cut','title_regex']]

print(train_offline_result)



#-----------------------------
#-----------------------------
#put those words more frequency in the front


count = 0
for i in train_offline_result.values:
    print("i is",i)
    result = str(i[1]).split(',')
    print(result)
    title_cut = str(i[2]).split(',')
    print(title_cut)
    title_regex = str(i[3]).split(',')
    print(title_regex)
    # dic={}
    # tmp_result=[]
    # for x in jieba.posseg.cut(" ".join(title_cut)):
    #     dic[x.word]=x.flag
    # print(dic)
    # if title_regex[0] == '':
    #     for v in title_cut:
    #         if  'a' in dic[v] or 'n' in dic[v]:
    #             tmp_result.append(v)
    # else:
    #     tmp_result = title_regex + title_cut
    if title_regex[0] == '':
        tmp_result = title_cut
    else:
        tmp_result = title_regex + title_cut

    count = count + len(set(result[:])&set(tmp_result[:2]))
    print(count)