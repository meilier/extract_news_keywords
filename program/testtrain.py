import pandas as pd
import jieba
import re
import jieba.analyse
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

# 去除文章的数字，数字没有意义，单纯一个数字，不能达到对文章内容的区分
train_title_doc['title_cut'] = train_title_doc['title'].apply(lambda x:''.join(filter(lambda ch: ch not in ' \t1234567890', x)))
# 策略 extract_tags 直接利用jieba的提取主题词的工具



train_title_doc['title_cut'] = train_title_doc['title_cut'].apply(lambda x:','.join(jieba.analyse.extract_tags(x,topK = 5)))
# 第二规则 提取 《》 通过分析发现，凡是书名号的东西都会被用来作为主题词
train_title_doc['title_regex'] = train_title_doc['title'].apply(lambda x:','.join(re.findall(r"《(.+?)》",x)))


# 利用策略 + 规则 查看训练集的准确率
train_offline_result = train_title_doc[['id','label','title_cut','title_regex']]

print(train_offline_result)

#exit(0)

# 验证我这个规则能够达到的分数 记得 * 0.5
count = 0
for i in train_offline_result.values:
    print("i is",i)
    result = str(i[1]).split(',')
    print(result)
    title_cut = str(i[2]).split(',')
    print(title_cut)
    title_regex = str(i[3]).split(',')
    print(title_regex)
    if title_regex[0] == '':
        tmp_result = title_cut
    else:
        tmp_result = title_regex + title_cut

    count = count + len(set(result[:2])&set(tmp_result[:2]))
    print(count)