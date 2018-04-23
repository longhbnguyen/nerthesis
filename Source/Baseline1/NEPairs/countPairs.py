import pandas as pd 


e_prob_file = './e_prob.ORG.out'
e_predict_file = './e.ORG.out'
v_prob_file = './v_prob.ORG.out'
v_predict_file = './v.ORG.out'

e_predict_list = []
e_prob_list = []

v_predict_list = []
v_prob_list = []

output = './count_ORG'

w= open(output,'w',encoding='utf-8')

def getLabel(ents):
    org = 1.0
    per = 1.0
    loc = 1.0
    for ent in ents:
        org *= float(ent[3][ent[3].find('=')+1:])
        per *= float(ent[4][ent[4].find('=')+1:])
        loc *= float(ent[5][ent[5].find('=')+1:])
    if org == max(org,per,loc):
        res = 'ORGANIZATION'
    elif loc == max(org,per,loc):
        res = 'LOCATION'
    elif per == max(org,per,loc):
        res = 'PERSON'
    return res

def retag(predict_list,prob_list):
    type_list = []
    for i in range(len(predict_list)):
        tag_flag = False
        cur_type = predict_list[i][0][2]
        if cur_type == 'O':
            label = getLabel(prob_list[i])
            type_list.append(label)
            continue
        for j in range(len(predict_list[i])):
            if predict_list[i][j][2] != cur_type:
                label = getLabel(prob_list[i])
                type_list.append(label)
                tag_flag = True
                break
        if tag_flag == False:
            label = cur_type
            type_list.append(label)
    print(i)
    return type_list

item = []
with open(e_predict_file,'r',encoding='utf-8') as f:
    for line in f:
        if line == '\n':
            e_predict_list.append(item)
            item = []
            continue
        item.append(line.split())
        
item = []
with open(e_prob_file,'r',encoding='utf-8') as f:
    for line in f:
        if line == '\n':
            e_prob_list.append(item)
            item = []
            continue
        item.append(line.split())

item = []
with open(v_predict_file,'r',encoding='utf-8') as f:
    for line in f:
        if line == '\n':
            v_predict_list.append(item)
            item = []
            continue
        item.append(line.split())

item = []
with open(v_prob_file,'r',encoding='utf-8') as f:
    for line in f:
        if line == '\n':
            v_prob_list.append(item)
            item = []
            continue
        item.append(line.split()) 


e_type_list = retag(e_predict_list,e_prob_list)
v_type_list = retag(v_predict_list,v_prob_list)

print(len(e_predict_list))
print(len(e_prob_list))
print(len(v_predict_list))
print(len(v_prob_list))
print(len(e_type_list))
print(len(v_type_list))
for i in range(len(e_type_list)):
    w.write(e_type_list[i])
    w.write('\t')
    w.write(v_type_list[i])
    w.write('\n')