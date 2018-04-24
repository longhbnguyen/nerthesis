from sklearn.metrics import classification_report

import pandas as pd 

df_pred = pd.read_csv('datatest_eng_spacy.txt',sep = '\t', encoding = 'utf-8',header  = None, names= ['Word','Predict'])
df_true = pd.read_csv('test_stanfordner_eng.txt',sep = '\t', encoding = 'utf-8',header  = None, names= ['Word','Label'])

df = pd.read_csv('stanfordner_eng_res.txt',sep = '\t', encoding = 'utf-8',header  = None, names= ['Word','Label','Predict'])

y_pred = list(df.Predict.astype(str))
y_true = list(df.Label.astype(str))
target_names = ['LOCATION','O','ORGANIZATION','PERSON',]

print(classification_report(y_true, y_pred, target_names=target_names))



# x_pred = list(df_pred['Word'].astype(str))
# y_pred = list(df_pred.Predict.astype(str))
# for i in range(len(y_pred)):
#     if y_pred[i] not in ['ORGANIZATION','O','LOCATION','PERSON']:
#         print(y_pred[i])
#         print(x_pred[i])
# # print(len(y_pred))
# # print(set(y_pred))
# y_true = list(df_true.Label.astype(str))
# # print(set(y_true))
# # print(len(y_true))

# target_names = ['LOCATION','O','ORGANIZATION','PERSON',]

# print(classification_report(y_true, y_pred, target_names=target_names))
