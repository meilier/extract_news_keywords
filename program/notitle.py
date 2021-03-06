import pandas as pd
import pdb
import jieba
import re
import jieba.analyse
import jieba.posseg
import numpy as np

# ID 标题 文本内容
data = pd.read_csv('../data/all_docs.txt',sep='\001',header=None)
data.columns = ['id','title','doc']

train = pd.read_csv('../data/train_docs_keywords.txt',sep='\t',header=None)
train.columns = ['id','label']
train_id_list = list(train['id'].unique())

train_title_doc = data[data['id'].isin(train_id_list)]

test_title_doc = data[~data['id'].isin(train_id_list)]

train_title_doc = pd.merge(train_title_doc,train,on=['id'],how='inner')

now=1
para=5 # 标题与正文的比例




# 策略 extract_tags
test_title_doc['title_cut'] = test_title_doc['title'].apply(lambda x:''.join(filter(lambda ch: ch not in ' \t1234567890', str(x))))

test_title_doc['title_cut'] = test_title_doc['title_cut'].apply(lambda x:','.join(jieba.analyse.extract_tags(str(x),topK = 4)))
# 第二规则 提取 《》
test_title_doc['title_regex'] = test_title_doc['title'].apply(lambda x:','.join(re.findall(r"《(.+?)》",str(x))))

# 利用策略 + 规则 查看训练集的准确率
test_offline_result = test_title_doc[['id','id','title_cut','title_regex']]

label1 = []
label2 = []

for i in test_offline_result.values:
    result = str(i[1]).split(',')
    title_cut = str(i[2]).split(',')
    title_regex = str(i[3]).split(',')
    dic={}
    tmp_result=[]
    for x in jieba.posseg.cut(" ".join(title_cut)):
        dic[x.word]=x.flag
    if title_regex[0] == '':
        for _ in title_cut:
            try:
                if 'a' in dic[_] or 'n' in dic[_] or 't' in dic[_]:
                    tmp_result.append(_)
            except:
                pass
    else:
        tmp_result = title_regex
        p=0
        while len(tmp_result)<2:
            if title_cut[p] in tmp_result:
                p+=1
                continue
            tmp_result.append(title_cut[p])
            p+=1

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
result['label1'] = result['label1'].replace('','nan')
result['label2'] = label2
result['label2'] = result['label2'].replace('','nan')
print('down')
result.to_csv('../result/other_result{}.csv'.format(now),index=None)