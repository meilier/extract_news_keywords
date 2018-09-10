import pandas as pd
import jieba
import re
import jieba.analyse
import numpy as np

#jieba.load_userdict("../data/baidu.txt")

allow_pos = ('nr')
# get dict
jiebadict = pd.read_csv('../data/dict.txt',sep=' ',header=None)
jiebadict.columns = ['word',"frequency","property"]
print(jiebadict)


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

train_title_doc['title_pre']=[[] for i in range(len(train_title_doc['title']))]


#1.  exclude useless numbers
train_title_doc['title_cut'] = train_title_doc['title'].apply(lambda x:''.join(filter(lambda ch: ch not in ' \t1234567890', x)))
train_title_doc['title_pre'] = train_title_doc['title'].apply(lambda x:''.join(filter(lambda ch: ch not in ' \t1234567890', x)))

#2. extract key words
train_title_doc['title_cut'] = train_title_doc['title_cut'].apply(lambda x:','.join(jieba.analyse.extract_tags(x,allowPOS=('nr','nt','ns','nz','s','n'),topK = 10)))

# for i, words in enumerate(train_title_doc['title']):
#     train_title_doc['title_pre'][i] = jieba.analyse.extract_tags(words,allowPOS=('nr','nt','ns','nz','s','n'),topK = 8,withWeight= True)
#     print(i," ",train_title_doc['title_pre'][i])

#print(train_title_doc['title_pre'])

#3. extract quotes
train_title_doc['title_regex'] = train_title_doc['title'].apply(lambda x:','.join(re.findall(r"《(.+?)》",x)))


# we run train
train_offline_result = train_title_doc[['id','label','title_cut','title_regex']]

#print(train_offline_result)



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
    dic={}
    tmp_result=[]
    # for x in jieba.posseg.cut(" ".join(title_cut)):
    #     dic[x.word]=x.flag
    # print(dic)
    # if title_regex[0] == '':
    #     for v in title_cut:
    #         try:
    #             if  'a' in dic[v] or 'n' in dic[v]:
    #                 tmp_result.append(v)
    #         except:
    #             pass
    # else:
    #     tmp_result = title_regex + title_cut
    if title_regex[0] == '':
        tmp_result = title_cut
    else:
        tmp_result = title_regex + title_cut
    #according frequency in dict to sort tmp_result
    # icount = len(tmp_result)
    # jcount = len(tmp_result)
    # dictcount = len(jiebadict['word'])
    # tmp_frequency = []
    # #get frequency
    # for i in range(icount):
    #     for j in range(dictcount):
    #         if tmp_result[i] == jiebadict['word'][j]:
    #             print("tmp_result[i] is : ",tmp_result[i])
    #             print("jiebadict['frequency'][j] is : ",jiebadict['frequency'][j])
    #             print("tme pre befor :",tmp_frequency)
    #             tmp_frequency.append(jiebadict['frequency'][j])
    #             print("tme pre after :",tmp_frequency)
    #             break

    # # sreach for top value and second top value
    # firstindex = 0
    # secondindex = 0
    # print(tmp_frequency)
    # new_frequency = tmp_frequency[:]
    # new_frequency.sort(reverse = True)
    # for i in range(icount):
    #     if tmp_frequency[i] == new_frequency[0]:
    #         firstindex = i
    #         break
    # for j in range(jcount):
    #     if tmp_frequency[j] == new_frequency[1]:
    #         secondindex = j
    #         break
    # print("firstindex is secondindex is ",firstindex,secondindex)

    # count = count + len(set(result[:])&set((tmp_result[firstindex],tmp_result[secondindex])))
    count = count + len(set(result[:])&set(tmp_result[:2]))
    print(count)