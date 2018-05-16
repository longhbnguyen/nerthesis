import spacy
import json
import re

# ent_pattern_start = re.compile(r"(<[A-Z]+\_\d+>)")
# ent_pattern_end = re.compile(r"(</[A-Z]+\_\d+>)")

# en_model = spacy.load('en_core_web_md')
vi_model = spacy.load('viNerFull50')

en_file = 'nlp.vi-en.tok.clean.en'
vi_file = 'nlp.vi-en.tok.clean.vi'

en_list = open(en_file,'r',encoding='utf-8').read().split('\n')
vi_list = open(vi_file,'r',encoding='utf-8').read().split('\n')

output_en = './cooc_spacy_en_list.txt'
output_vi = './cooc_spacy_vi_list.txt'

en_ent_list = []
vi_ent_list = []

for i in range(len(en_list)):
    # if i == 5:
    #     break
    # en_sent = re.sub(ent_pattern_start,' ', en_list[i])
    # en_sent = re.sub(ent_pattern_end, ' ' , en_sent)

    # vi_sent = re.sub(ent_pattern_start,' ', vi_list[i])
    # vi_sent = re.sub(ent_pattern_end,' ', vi_sent)
    
    # while '  ' in en_sent:
    #     en_sent = en_sent.replace('  ',' ')
    # while '  ' in vi_sent:
    #     vi_sent = vi_sent.replace('  ',' ')
    # en_sent=en_sent.strip()
    # vi_sent = vi_sent.strip()
    # print('En Sent ', en_sent)
    # print('Vi Sent ', vi_sent)
    # en_doc = en_model(en_list[i])
    vi_doc = vi_model(vi_list[i])
    # en_ent_list_sent = []
    vi_ent_list_sent = []
    # start = 0
    # # print('English')
    # for ent in en_doc.ents:
    #     # print(ent, ent.label_)
    #     label = ent.label_
    #     if label in ['GPE','FAC']:
    #         label = 'LOCATION'
    #     elif label == 'LOC':
    #         label = 'LOCATION'
    #     elif label == 'ORG':
    #         label = 'ORGANIZATION'
    #     elif label in ['PER','PERSON']:
    #         label = 'PERSON'
    #     else:
    #         continue
    #     # idx_seq = list(range(ent.start+1, ent.end+1))
    #     word = ent.text
    #     # idx_start = en_list[i].find(word,start)
    #     # print(idx_start)
    #     # start = idx_start
    #     # tok_start = len(en_list[i][:idx_start].split()) + 1
    #     # tok_end = tok_start + len(word.split())
    #     # idx_seq = list(range(tok_start,tok_end))
    #     entity = (word,label)
    #     en_ent_list_sent.append(entity)
    #     # print(word,idx_seq)
    # print('Vietnamese')
    start = 0
    for ent in vi_doc.ents:
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
        # idx_seq = list(range(ent.start+1, ent.end+1))
        word = ent.text
        # idx_start = vi_list[i].find(word,start)
        # print(idx_start)
        # start = idx_start
        # tok_start = len(vi_list[i][:idx_start].split()) + 1
        # tok_end = tok_start + len(word.split())
        # idx_seq = list(range(tok_start,tok_end))
        entity = (word,label)
        vi_ent_list_sent.append(entity)
        # print(word,idx_seq)
    # en_ent_list.append(en_ent_list_sent)
    vi_ent_list.append(vi_ent_list_sent)
    

# with open(output_en,'w',encoding='utf-8') as w1:
#     json.dump(en_ent_list,w1)
with open(output_vi,'w',encoding='utf-8') as w2:
    json.dump(vi_ent_list,w2)