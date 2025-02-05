import spacy
from ast import literal_eval

nlp  = spacy.load('viNerFull50')

w = open('datatest_viet_spacy.txt', 'w', encoding = 'utf-8')
i = 0
with open('test_viet_sent.txt','r',encoding = 'utf-8') as f:
    for line in f:
        doc = nlp(line)
        ent_flag = False
        for tok in doc:
            if str(tok) == '\n':
                continue
            label = 'O'
            # for tok in doc:
            #     print(tok)
            for ent in doc.ents:
                if tok in ent:
                    label = ent.label_
                    if label in ['GPE','FAC']:
                        label = 'LOCATION'
                    elif label == 'LOC':
                        label = 'LOCATION'
                    elif label == 'ORG':
                        label = 'ORGANIZATION'
                    elif label == 'PER':
                        label = 'PERSON'
                    else:
                        label = 'O'
                    break
            w.write(str(tok))
            w.write('\t')
            w.write(str(label))
            w.write('\n')        
        w.write('\n')
        # i = i+1
        # if i == 158:
        #     break
