import pandas as pd
import pdb
import jieba
import re
import jieba.analyse
import jieba.posseg
import numpy as np

#get data
data = pd.read_csv('../data/all_docs.txt',sep='\001',header=None)
data.columns = ['id','title','doc']

#get train
train = pd.read_csv('../data/train_docs_keywords.txt',sep='\t',header=None)
train.columns = ['id','label']
train_id_list = list(train['id'].unique())

train_title_doc = data[data['id'].isin(train_id_list)]

test_title_doc = data[~data['id'].isin(train_id_list)]

train_title_doc = pd.merge(train_title_doc,train,on=['id'],how='inner')






# 策略 extract_tags
train_title_doc['title_cut'] = train_title_doc['title'].apply(lambda x:''.join(filter(lambda ch: ch not in ' \t1234567890', str(x))))

train_title_doc['title_cut'] = train_title_doc['title_cut'].apply(lambda x:','.join(jieba.analyse.extract_tags(str(x),topK = 10)))
# 第二规则 提取 《》
train_title_doc['title_regex'] = train_title_doc['title'].apply(lambda x:','.join(re.findall(r"《(.+?)》",str(x))))

# 利用策略 + 规则 查看训练集的准确率
train_offline_result = train_title_doc[['id','label','title_cut','title_regex']]


print(train_offline_result)


count = 0
for i in train_offline_result.values:
    print("i is",i)
    result = str(i[1]).split(',')
    print(result)
    title_cut = str(i[2]).split(',')
    print(title_cut)
    title_regex = str(i[3]).split(',')
    print(title_regex)
    dic={}
    tmp_result=[]
    for x in jieba.posseg.cut(" ".join(title_cut)):
        dic[x.word]=x.flag
    print("dic is",dic)
    if title_regex[0] == '':
        for _ in title_cut:
            try:
                if 'a' in dic[_] or 'n' in dic[_] or 't' in dic[_]:
                    tmp_result.append(_)
            except:
                pass
    else:
        # tmp_result = title_regex
        # p=0
        # while len(tmp_result)<2:
        #     if title_cut[p] in tmp_result:
        #         p+=1
        #         continue
        #     tmp_result.append(title_cut[p])
        #     p+=1
        tmp_result = title_regex + title_cut

    count = count + len(set(result[:])&set(tmp_result[:2]))
    print(count)