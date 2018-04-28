import spacy
import json
import re

ent_pattern_start = re.compile(r"(<[A-Z]+\_\d+>)")
ent_pattern_end = re.compile(r"(</[A-Z]+\_\d+>)")

en_model = spacy.load('en')
vi_model = spacy.load('viNerFull50')

en_file = '../../../Data/corpora/0_DATA/3_Test/test_eng'
vi_file = '../../../Data/corpora/0_DATA/3_Test/test_viet'

en_list = open(en_file,'r',encoding='utf-8').read().split('\n')
vi_list = open(vi_file,'r',encoding='utf-8').read().split('\n')

output_en = './en_ent_list_spacy_test.txt'
output_vi = './vi_ent_list_spacy_test.txt'

en_ent_list = []
vi_ent_list = []

for i in range(len(en_list)):
    # if i == 2:
    #     break
    en_sent = re.sub(ent_pattern_start,' ', en_list[i])
    en_sent = re.sub(ent_pattern_end, ' ' , en_sent)

    vi_sent = re.sub(ent_pattern_start,' ', vi_list[i])
    vi_sent = re.sub(ent_pattern_end,' ', vi_sent)
    
    while '  ' in en_sent:
        en_sent = en_sent.replace('  ',' ')
    while '  ' in vi_sent:
        vi_sent = vi_sent.replace('  ',' ')
    en_sent=en_sent.strip()
    vi_sent = vi_sent.strip()
    print('En Sent ', en_sent)
    print('Vi Sent ', vi_sent)
    en_doc = en_model(en_sent)
    vi_doc = vi_model(vi_sent)
    en_ent_list_sent = []
    vi_ent_list_sent = []
    for ent in en_doc.ents:
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
            continue
        idx_seq = list(range(ent.start+1, ent.end+1))
        word = ent.text
        entity = (idx_seq,label,word)
        en_ent_list_sent.append(entity)
    for ent in vi_doc.ents:
        idx_seq = list(range(ent.start+1, ent.end+1))
        label = ent.label_
        word = ent.text
        entity = (idx_seq,label,word)
        vi_ent_list_sent.append(entity)
    en_ent_list.append(en_ent_list_sent)
    vi_ent_list.append(vi_ent_list_sent)
    



with open(output_en,'w',encoding='utf-8') as w1:
    json.dump(en_ent_list,w1)
with open(output_vi,'w',encoding='utf-8') as w2:
    json.dump(vi_ent_list,w2)




        