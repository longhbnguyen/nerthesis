import InitialNER.tag as tag
import pandas as pd 

En_file_path = './corpora/0_DATA/1_Training/1_WordAlignment/nlp.vi-en.tok.clean.en'
Vn_file_path = './corpora/0_DATA/1_Training/1_WordAlignment/nlp.vi-en.tok.clean.vi'

En_file = open(En_file_path,mode = 'r',encoding='utf-8').read().split('\n')
Vn_file = open(Vn_file_path,mode = 'r',encoding='utf-8').read().split('\n')

def getCrossProduct(e_sent,v_sent):
    e_ents,v_ents = tag.tag_pairs(v_sent,e_sent)

    return [(x[1],y[1]) for x in e_ents for y in v_ents]
    

res = []
for i in range(len(En_file)):
    if i== 5:
        break
    # print(En_file[i])
    en_vi_list = getCrossProduct(En_file[i],Vn_file[i])
    for tp in en_vi_list:
        res.append(tp)

res_en, res_vi = zip(*res)
res_en = list(res_en)
res_en.append('Siemens Company')
res_vi = list(res_vi)
res_vi.append('Việt Nam')

df = pd.DataFrame({'NEE': res_en, 'NEV': res_vi})

df_count = pd.DataFrame({'Count' : df.groupby( [ "NEE", "NEV"] ).size()}).reset_index()
tmp = df_count[(df_count.NEV == 'Việt Nam') & (df_count.NEE == 'Siemens Company')].Count
print(df_count[df_count.NEE == 'Siemens Company'].Count.sum())

# print(df_count)