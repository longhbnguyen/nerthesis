import pandas as pd 
input_loc = './count_LOC'
input_per = './count_PER'
input_org = './count_ORG'
import numpy as np
df_loc = pd.read_csv(input_loc,sep = '\t', encoding='utf-8', header = None, names=['Eng','Vie'])
df_loc = df_loc.assign(Label = ['LOCATION']*len(df_loc.index))

df_per = pd.read_csv(input_per,sep = '\t', encoding='utf-8', header = None, names=['Eng','Vie'])
df_per = df_per.assign(Label = ['PERSON']*len(df_per.index))


df_org = pd.read_csv(input_org,sep = '\t', encoding='utf-8', header = None, names=['Eng','Vie'])
df_org = df_org.assign(Label = ['ORGANIZATION']*len(df_org.index))

frames = [df_loc,df_org,df_per]
result = pd.concat(frames).reset_index()
result_count = pd.DataFrame({ 'count' : result.groupby(['Label','Eng','Vie',]).size()}).reset_index()
result_count.to_csv('count_result.tsv',sep = '\t',index= False)

e_type = result_count['Eng'] == 'LOCATION'
v_type = result_count['Vie'] == 'ORGANIZATION'

tmp = result_count[e_type & v_type]

sum_ = np.sum(list(tmp['count']))
loc = float((tmp[tmp['Label'] == 'LOCATION']['count'].astype(int) / sum_).values)
org = float((tmp[tmp['Label'] == 'ORGANIZATION']['count'].astype(int) / sum_).values)
per = float((tmp[tmp['Label'] == 'PERSON']['count'].astype(int) / sum_).values)

print(loc)