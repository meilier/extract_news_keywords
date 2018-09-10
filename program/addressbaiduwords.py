import pandas as pd

label1 = []
label2 = []
data = pd.read_csv('../data/baidu-words.txt',header=None)
data.columns = ['word']
print(data)

# multipul_process = {}
# multipul_process[1] = 150000
for i in range(624620):
    label1.append('3')
    label2.append('n')


#for i  in data['word']:
	#data['word'][i] = data['word'][i] + " " + "10000" + " " + "n"
data["lable1"] = label1
data["lable2"] = label2

data.to_csv('../data/baidu.txt', sep=" " ,index=None)