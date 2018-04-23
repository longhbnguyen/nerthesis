import spacy
import sys
from collections import defaultdict
from nltk.tag.stanford import StanfordNERTagger


path_to_model = '../InitialNER/stanford-ner-2018-02-27/english.all.3class.distsim.crf.ser.gz'
path_to_jar = '../InitialNER/stanford-ner-2018-02-27/stanford-ner-3.9.1.jar'
nertagger=StanfordNERTagger(path_to_model, path_to_jar)

nlp = spacy.load('en')

v_sent = None
e_sent = None
v_ent_list = None
e_ent_list = None

def sentToTuple(e_sent):
    '''
    Tokenize the English sentence into tuple
    Input: English sentence (output of Giza++)
    Output: tp_list = [ (word, ({idx idx})) ,]
    '''
    sent_tokens = e_sent.split()
    # print(sent_tokens)
    tp_list = []
    idx_seq = ''
    idx_flag = False
    word = ''
    for i in range(len(sent_tokens) ):
        if sent_tokens[i] == '({':
            idx_flag = True
            word = sent_tokens[i-1]
            continue
        elif sent_tokens[i] == '})':
            tp = (word ,idx_seq.strip())
            # print(tp)
            tp_list.append(tp)
            idx_flag = False
            idx_seq = ''
            word = ''
        if idx_flag == True:
            idx_seq += sent_tokens[i] + ' '
    # print(tp_list)
    del tp_list[0]
    return tp_list

# Đó cũng là quy luật tự nhiên của con người trong thời kỳ phát triển . 
# NULL ({ 2 3 8 9 10 }) This ({ 1 }) is ({ }) a ({ }) natural ({ 6 7 }) law ({ 4 5 }) in ({ 11 }) the ({ }) development ({ 14 15 }) period ({ 12 13 }) . ({ 16 }) 

# e_ent_list  = [ (idx,idx,idx,... , type), ]
def getEntList_Spacy(e_tuple_list):
    '''
    Get the entity list of English sentence
    Input: English Sentence
    Output: e_ent_list  = [ ('idx idx idx ... ', type), ]
    '''
    e_sent = ''
    for tp in e_tuple_list:
        if tp[0] == 'NULL':
            continue
        e_sent += tp[0]+ ' '
    e_sent = e_sent.strip()
    # print(e_sent)
    
    doc = nlp(e_sent)
    ent_list = []
    for ent in doc.ents:
        idx_seq = ''
        for i in range(ent.start,ent.end):
            idx_seq += str(i) + ' '
        idx_seq.strip()
        tp = (idx_seq,ent.label_)
        ent_list.append(tp)
    # print(ent_list)
    return ent_list

def getEntList_StanfordNER(e_tuple_list):
    '''
    Get the entity list of English sentence
    Input: English Sentence
    Output: e_ent_list  = [ ('idx idx idx ... ', type), ]
    '''
    e_sent = ''
    for tp in e_tuple_list:
        if tp[0] == 'NULL':
            continue
        e_sent += tp[0]+ ' '
    e_sent = e_sent.strip()
    tag_list = nertagger.tag(e_sent.split())
    ent = ()
    ent_list = []
    cur_type = ''
    ent_flag = False
    idx_seq = ''

    for i in range(len(tag_list)):
        if tag_list[i][1] != 'O':
            #ent of different type
            if cur_type != tag_list[i][1] and ent_flag == True:
                ent = (idx_seq,cur_type)
                idx_seq = str(i)
                ent_list.append(ent)
                cur_type = tag_list[i][1]
            #continue of ent
            elif cur_type == tag_list[i][1] and ent_flag == True:
                idx_seq +=  ' ' + str(i) 
            #begin of ent
            else:
                ent_flag = True
                cur_type = tag_list[i][1]
                idx_seq = str(i)
        else:
            if ent_flag == True:
                ent = (idx_seq, cur_type)
                ent_list.append(ent)
                idx_seq = ''
                ent_flag = False
            else:
                continue
        # print(ent_list)
    return ent_list

def getVietnameseEnt(tuple_list, v_sent, e_ent_list):
    '''
    Get the entity list of Vietnamese sentence based on word alignment
    Input: Alignment List, English entity list
    Output: Vietnamese entity list
    '''
    v_tokens = v_sent.split()
    v_ent_list = []
    # print(tuple_list[8])

    for e_ent in e_ent_list:
        res = ''
        v_ent_idx = []
        for idx in e_ent[0].split():
            list_idx = tuple_list[int(idx)][1].split()
            for index in list_idx:
                v_ent_idx.append(int(index))

        v_ent_idx = sorted(v_ent_idx, key = int)
        
        # for idx in v_ent_idx:
        #     res += v_tokens[idx-1] + ' '
        # res = res.strip()
        v_ent_list.append((v_ent_idx,e_ent[1]))
    return v_ent_list

def getVietEntSet(v_sent,e_sent):
    # e_tuple_list = sentToTuple(e_sent)
    # e_ent_list = getEntList_StanfordNER(e_tuple_list)
    e_tuple_list = sentToTuple(e_sent)
    e_ent_list = getEntList_StanfordNER(e_tuple_list)
    print(e_ent_list)
    v_ent_list = getVietnameseEnt(e_tuple_list,v_sent,e_ent_list)

    return v_ent_list

def main():
    v_sent = 'Theo ông John Rockhold thì thị trường Việt Nam ẩn chứa nhiều thách thức .'
    e_sent = 'NULL ({ }) The ({ }) Vietnamese ({ 8 9 }) market ({ 6 7 }) has ({ }) several ({ 12 }) challenges ({ 13 14 }) according ({ }) to ({ }) HCMC ({ 10 11 }) director ({ }) John ({ 3 }) Rockhold ({ 1 2 4 5 }) . ({ 15 })'
    e_tuple_list = sentToTuple(e_sent)
    e_ent_list = getEntList_StanfordNER(e_tuple_list)
    # print(e_ent_list)
    v_ent_list = getVietnameseEnt(e_tuple_list,v_sent,e_ent_list)
    # print(v_ent_list)

if __name__ == '__main__':
    main()