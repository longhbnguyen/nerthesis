import spacy
import sys
from collections import defaultdict
from nltk.tag.stanford import StanfordNERTagger
import json
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import MonoReassignModel.MonoFromFile as Mono
import pandas as pd 
import csv
import utilities
import config

#Load path
path_to_model = config.en_model_stanford
path_to_jar = config.path_to_jar
initial_ent_list_file_stanford_dev = config.initial_en_ent_list_file_stanford_dev
initial_ent_list_file_spacy_dev = config.initial_en_ent_list_file_spacy_dev
initial_ent_list_file_stanford_test = config.initial_en_ent_list_file_stanford_test
initial_ent_list_file_spacy_test = config.initial_en_ent_list_file_spacy_test


alignment_table_file = config.alignment_table_file

initial_ent_list_stanford = []
initial_ent_list_spacy = []

alignment_table = pd.read_csv(alignment_table_file, sep = '\t', encoding = 'utf-8',quoting=csv.QUOTE_NONE, error_bad_lines=False)

alignment_table = alignment_table.fillna('NaN')


nertagger=StanfordNERTagger(path_to_model, path_to_jar)

nlp = spacy.load('en')

v_sent = None
e_sent = None
v_ent_list = None
e_ent_list = None

def sentToTuple(source_sent):
    '''
    Tokenize the Source sentence into tuple
    Input: English sentence (output of Giza++)
    Output: tp_list = [ (word, ({idx idx})) ,]
    '''
    source_sent_tokens = source_sent.split()
    # print(sent_tokens)
    tp_list = []
    idx_seq = ''
    idx_flag = False
    word = ''
    for i in range(len(source_sent_tokens) ):
        if source_sent_tokens[i] == '({':
            idx_flag = True
            word = source_sent_tokens[i-1]
            continue
        elif source_sent_tokens[i] == '})':
            tp = (word ,idx_seq.strip())
            # print(tp)
            tp_list.append(tp)
            idx_flag = False
            idx_seq = ''
            word = ''
        if idx_flag == True:
            idx_seq += source_sent_tokens[i] + ' '
    # print(tp_list)
    del tp_list[0]
    return tp_list

# e_ent_list  = [ (idx,idx,idx,... , type), ]
def getEntList_Spacy(source_tuple_list):
    '''
    Get the entity list of Source sentence
    Input: Source Sentence
    Output: e_ent_list  = [ ('idx idx idx ... ', type), ]
    '''
    source_sent = ''
    for tp in source_tuple_list:
        if tp['Word'] == 'NULL':
            continue
        source_sent += tp['Word']+ ' '
    source_sent = source_sent.strip()
    # print(e_sent)
    
    doc = nlp(source_sent)
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

def createEntListTable_Spacy(mode):
    global initial_ent_list_spacy
    if mode == 'dev':
        initial_ent_list_file_spacy = initial_ent_list_file_spacy_dev
    elif mode == 'test':
        initial_ent_list_file_spacy = initial_ent_list_file_spacy_test
    
    json_data= open(initial_ent_list_file_spacy).read()
    initial_ent_list_spacy = json.loads(json_data)


def getEntList_Spacy_FromFile(sent_index):

    # print(initial_ent_list_spacy)
    return initial_ent_list_spacy[sent_index]

def getEntList_StanfordNER(source_tuple_list):
    '''
    Get the entity list of Source sentence
    Input: Source Sentence
    Output: e_ent_list  = [ ('idx idx idx ... ', type), ]
    '''
    source_sent = ''
    for tp in source_tuple_list:
        if tp['Word'] == 'NULL':
            continue
        source_sent += tp['Word']+ ' '
    source_sent = source_sent.strip()
    tag_list = nertagger.tag(source_sent.split())
    ent = ()
    ent_list = []
    cur_type = ''
    ent_flag = False
    # idx_seq = ''
    idx_seq = []
    word =''
    for i in range(len(tag_list)):
        if tag_list[i][1] != 'O':
            #ent of different type
            if cur_type != tag_list[i][1] and ent_flag == True:
                for idx in idx_seq:
                    word += tag_list[idx-1][0] + ' '
                word = word.strip()
                ent = (idx_seq,cur_type,word)
                # idx_seq = str(i)
                idx_seq.append(i+1)
                ent_list.append(ent)
                cur_type = tag_list[i][1]
                word = ''
            #continue of ent
            elif cur_type == tag_list[i][1] and ent_flag == True:
                # idx_seq +=  ' ' + str(i) 
                idx_seq.append(i+1)
            #begin of ent
            else:
                ent_flag = True
                cur_type = tag_list[i][1]
                # idx_seq = str(i)
                idx_seq.append(i+1)
        else:
            if ent_flag == True:
                for idx in idx_seq:
                    word += tag_list[idx-1][0] + ' '
                word = word.strip()
                ent = (idx_seq, cur_type, word)
                ent_list.append(ent)
                idx_seq = []
                ent_flag = False
                word = ''
            else:
                continue
        # print(ent_list)
    return ent_list


def createEntListTable_Stanford(mode):
    # print('Create Ent List')
    global initial_ent_list_stanford
    initial_ent_list_stanford = []
    # print('Mode ',mode)
    if mode == 'dev':
        initial_ent_list_file_stanford = initial_ent_list_file_stanford_dev
    elif mode == 'test':
        initial_ent_list_file_stanford = initial_ent_list_file_stanford_test
    
    # print(initial_ent_list_file_stanford)
    
    line_list = []
    word_list_sent = []
    with open(initial_ent_list_file_stanford,'r',encoding='utf-8') as f:
        # print(initial_ent_list_file_stanford)
        for line in f:
            # print(line)
            if line == '\n':
                line_list.append(word_list_sent)
                word_list_sent = []
            else:
                word_list_sent.append((line.split()[0], line.split()[2]))
    
    for line in line_list:
        ent_flag = False
        cur_label = ''
        ent_word = ''
        idx_seq = []
        ent_list_sent = []
        for i in range(len(line)):
            word = line[i][0]
            label = line[i][1]
            if label == 'O':
                if ent_flag == False:
                    continue
                else:
                    ent_word = ent_word.strip()
                    ent = (idx_seq,cur_label,ent_word)
                    ent_list_sent.append(ent)
                    ent_word = ''
                    cur_label = label
                    idx_seq = []
                    ent_flag = False
            else:
                if ent_flag == True:
                    if cur_label == label:
                        ent_word += ' ' + word
                        idx_seq.append(i+1)
                        cur_label = label
                    else:
                        ent_word = ent_word.strip()
                        ent = (idx_seq,cur_label,ent_word)
                        ent_list_sent.append(ent)
                        ent_word = ''
                        cur_label = label
                        idx_seq = []
                        idx_seq.append(i+1)
                else:
                    ent_flag = True
                    ent_word += ' ' + word
                    idx_seq.append(i+1)
                    cur_label = label
        initial_ent_list_stanford.append(ent_list_sent)
    
    # print('initial_ent_list_stanford[0]', initial_ent_list_stanford[0])


def getEntList_StanfordNER_FromFile(sent_index):
    return initial_ent_list_stanford[sent_index]

def getCombineNER(tuple_list):
    spacy_list = getEntList_Spacy(tuple_list)
    stanfordner_list = getEntList_StanfordNER(tuple_list)
    return spacy_list + stanfordner_list

def getCombineNERFromFile(sent_index):

    stanfordner_list = getEntList_StanfordNER_FromFile(sent_index)
    spacy_list = getEntList_Spacy_FromFile(sent_index)
    return stanfordner_list + spacy_list

def HardAlign(source_sent, target_sent, sent_index):
    source_ent_list = getCombineNERFromFile(sent_index)
    target_ent_list = getTargetEntList(source_sent,target_sent,source_ent_list)

    for i in range(len(target_ent_list)):
        for ent in target_ent_list[i]:
            for j in range(len(ent[0])-1):
                if (ent[0][j] + 1) != (ent[0][j+1]):
                    return [], []
                    
    return source_ent_list,target_ent_list

def SoftAlign(source_sent,target_sent,sent_index):
    # ent_set = getEntSet(v_sent,e_sent)
    source_ent_list = getEntList_StanfordNER_FromFile(sent_index)
    target_ent_list = getTargetEntList(source_sent,target_sent,source_ent_list)
    # print('SourceSent', source_sent)
    # print('TargetSent', target_sent)
    res_source_ent_list = []
    res_target_ent_list = []
    for i in range(len(target_ent_list)):
        ent = target_ent_list[i]
        continuous_flag = True
        # print(ent[0])
        for j in range(len(ent[0])-1):
            # print(ent[0][j]+1, ent[0][j+1])
            if ent[0][j] + 1 != ent[0][j+1]:
                continuous_flag = False
                break
        if continuous_flag:
            res_source_ent_list.append(source_ent_list[i])
            res_target_ent_list.append(target_ent_list[i])
        
    return res_source_ent_list, res_target_ent_list


def getAlignScore(source_ent, target_ent, idx):
    '''
    '''
    final_score = 0.0
    source_ent_score = Mono.getMonoScore(source_ent,idx,'en')[source_ent[1]]
    align_score = 1.0
    target_ent_words = target_ent[2].split()
    for tok in target_ent_words:
        # print('Tok', tok)
        word_score = 0
        tmp = alignment_table[alignment_table.VN == tok].Prob
        # print('tmp',tmp)
        tmp_sum = tmp.sum()
        # print('sum',tmp_sum)
        if (tmp_sum):
            word_score = tmp_sum / tmp.size
        else:
            word_score = 0
        align_score*= word_score
    final_score = source_ent_score * align_score
    return final_score

def getTargetEntList(tuple_list, target_sent, source_ent_list):
    '''
    Get the entity list of Target sentence based on word alignment
    Input: Alignment List, Source entity list, Target Sent
    Output: Target entity list
    '''
    target_ent_list = []
    # print('TupleList',tuple_list)
    # print('TargetSent', target_sent)
    # print('SourceEntList', source_ent_list)
    for source_ent in source_ent_list:
        res = ''
        target_ent_idx = []
        # print(source_ent)
        # print(tuple_list)
        # print(source_ent[0])
        for idx in source_ent[0]:
            # print(idx)
            # idx = idx + 1
            # print(idx)
            list_idx = tuple_list[int(idx)]['Index']
            for index in list_idx:
                target_ent_idx.append(int(index))

        target_ent_idx = sorted(target_ent_idx, key = int)
            
        for idx in target_ent_idx:
            res += target_sent[idx-1] + ' '
        res = res.strip()
        
        target_ent_list.append((target_ent_idx,source_ent[1],res))

    
    return target_ent_list

def getEntSet(source_sent,target_sent):
    '''
    [([idx]_en,[idx]_vi,'type',[word_en],[word_vi])]
    '''    
    source_tuple_list = source_sent
    source_ent_list = getEntList_StanfordNER(source_tuple_list)
    # print("Source Ent List", source_ent_list)
    target_ent_list = getTargetEntList(source_tuple_list,target_sent,source_ent_list)
    ent_set = []
    for i in range(len(source_ent_list)):

        tp = (source_ent_list[i][0],target_ent_list[i][0],source_ent_list[i][1],source_ent_list[i][2],target_ent_list[i][2])

        ent_set.append(tp)
    
    return ent_set

def getEntSetFromFile(source_sent, target_sent, sent_index):
    source_ent_list = getEntList_StanfordNER_FromFile(sent_index)
    target_ent_list = getTargetEntList(source_sent,target_sent,source_ent_list)
    # source_ent_list,target_ent_list = SoftAlign(source_sent,target_sent,sent_index)
    ent_set = []
    for i in range(len(source_ent_list)):
        tp = (source_ent_list[i][0],target_ent_list[i][0],source_ent_list[i][1],source_ent_list[i][2],target_ent_list[i][2])
        ent_set.append(tp)
    return ent_set



def main():
    createEntListTable_Stanford()
    createEntListTable_Spacy()
    EtoV_dev_list = utilities.read_align_file('../../Alignment_Split/EtoV_Dev.txt')
    # pairs = getEntSetFromFile(EtoV_dev_list[0]['Source'],EtoV_dev_list[0]['Target'],0)
    # print(pairs)

    source_sent = EtoV_dev_list[0]['Source']
    target_sent = EtoV_dev_list[0]['Target']
    source_ent_list = getEntList_StanfordNER_FromFile(0)
    target_ent_list = getTargetEntList(source_sent,target_sent,source_ent_list)
    for i in range(len(source_ent_list)):
        # print('Pair', source_ent_list[i],target_ent_list[i])
        align_score = getAlignScore(source_ent_list[i],target_ent_list[i],0)
        # print('Score', align_score)
    vn_list = list(alignment_table.VN)
    en_list = list(alignment_table.EN)
    prob = list(alignment_table.Prob)
    # print(len(alignment_table.index))
    # print(len(en_list))
    # print(len(vn_list))
    # print(len(prob))
    # for i in range(6465):
    #     print(vn_list[i],en_list[i],prob[i])
    # print(len(alignment_table.index))
    # print(vn_list[153610],en_list[153610],prob[153610])
    print(alignment_table.shape)
    # alignment_table.to_csv('./AlignmentModel/tmp.tsv',sep = ' ', index = False)


if __name__ == '__main__':
    main()