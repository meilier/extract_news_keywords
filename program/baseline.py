# -*- coding: utf-8 -*-
__author__ = 'Han Wang'

import re
import jieba
import jieba.analyse
import pandas as pd
import numpy as np
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

now=1
all_docs='./data/all_docs.txt'
train_docs='./data/train_docs_keywords.txt'

data=pd.read_csv(all_docs,sep='\001',header=None,na_values=' ',keep_default_na=False)
data.columns=['id','title','content']

train_data=pd.read_csv(train_docs,sep='\t',header=None,na_values=' ',keep_default_na=False)
train_data.columns=['id','label']
train_id_list=list(train_data['id'].unique())

train_title_doc=data[data['id'].isin(train_id_list)]

test_title_doc=data[~data['id'].isin(train_id_list)]

train_title_doc=pd.merge(train_data,train_title_doc,on=['id'],how='inner')

def remove_digit(line):
    temp=line
    temp=re.sub('[0987654321]','',temp)
    return ' '.join(jieba.cut(temp))+' '


def main(data=train_title_doc,mode='check'):
    res=pd.DataFrame()
    data['title_cut'] = data['title'].apply(remove_digit)
    data['title_re'] = data['title'].apply(lambda x: '/'.join(re.findall("《(.+?)》", x)))
    data['content']=data['title_cut']*7+" "+data['content'].apply(remove_digit)
    #data['title_ext']=data['content'].apply(lambda x:','.join(jieba.analyse.extract_tags(str(x),5)))
    data_result = data[['id', 'content', 'title_re']]
    #data_result=data[['id', 'title_ext', 'title_re']]
    if mode=='check':
        data_result=data[['id','label','content','title_re']]
        #data_result=data[['id', 'label', 'title_ext', 'title_re']]
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(data['content'].values))
    #tfidf = transformer.fit_transform(vectorizer.fit_transform(data['title_cut'].values))
    words = vectorizer.get_feature_names()
    temp_res=[[],[],[]]

    cnt=0
    for i in range(len(data_result.values)):
        temp_result = []
        elem = data_result.values[i]
        weight = tfidf[i].toarray()[0]
        loc = np.argsort(-weight)
        title_re = list(set(elem[-1].split('/')))
        #words=list(set(elem[-2].split(',')))
        if title_re[0]!='':
            for _ in title_re:
                if ',' in _:
                    continue
                temp_result.append(_)
                if len(temp_result)<2:
                    break
        p = 0
        while len(temp_result) < 2:
            word = words[loc[p]]
            for _ in temp_result:
                if word in _:
                    p+=1
                    continue
            temp_result.append(word)
            p += 1
        if mode=='check':
            gold=elem[1].split(',')
            cnt += len(set(gold) & set(temp_result))
        else:
            temp_res[0].append(elem[0])
            temp_res[1].append(temp_result[0])
            temp_res[2].append(temp_result[1])
    if mode=='check':
        print(cnt*0.5)
    else:
        res['id']=temp_res[0]
        res['label1']=temp_res[1]
        res['label2']=temp_res[2]
        res.to_csv('./result/result{}.csv'.format(now),index=False)

if __name__=='__main__':
    main()
    #main(data,'test')