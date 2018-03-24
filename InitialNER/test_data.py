from ast import literal_eval

train_data = []
with open('NER_Spacy.out','r',encoding = 'utf-8') as f:
    for line in f:
        tp = literal_eval(line)
        train_data.append(tp)
    print('Loaded data!')

for data in train_data:
    print('-------------------------')
    print("Content: ",data[0])
    for ent in data[1]['entities']:
        print(ent[2],'-', data[0][ent[0]:ent[1]])
    input()        
        
