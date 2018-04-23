import pandas as pd 
import numpy as np

df = pd.read_csv('count_result.tsv',sep = '\t',encoding='utf-8')

def getScore(df, v_ent, e_ent):
    v_type = v_ent[1]
    e_type = e_ent[1]
    e_cond = df['Eng'] == e_type
    v_cond = df['Vie'] == v_type
    tmp = df[e_cond & v_cond]    
    sum_ = np.sum(list(tmp['count']))
    loc = float((tmp[tmp['Label'] == 'LOCATION']['count'].astype(int) / sum_).values)
    org = float((tmp[tmp['Label'] == 'ORGANIZATION']['count'].astype(int) / sum_).values)
    per = float((tmp[tmp['Label'] == 'PERSON']['count'].astype(int) / sum_).values)

