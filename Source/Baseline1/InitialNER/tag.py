
from nltk.tag.stanford import StanfordNERTagger

path_to_e_model = './stanford-ner-2018-02-27/english.all.3class.distsim.crf.ser.gz'
path_to_v_model = './stanford-ner-2018-02-27/vietnamese_new.gz'

path_to_jar = './stanford-ner-2018-02-27/stanford-ner-3.9.1.jar'

e_ner = StanfordNERTagger(path_to_e_model, path_to_jar)
v_ner = StanfordNERTagger(path_to_v_model, path_to_jar)

def getEntList(sent,ner):
    '''
    Perform NER tagging on a sentence
    Input: 
    '''
    tag_list = ner.tag(sent.split())
    ent = ()
    ent_list = []
    cur_type = ''
    ent_flag = False
    # idx_seq = ''
    idx_seq = []
    for i in range(len(tag_list)):
        if tag_list[i][1] != 'O':
            #ent of different type
            if cur_type != tag_list[i][1] and ent_flag == True:
                ent = (idx_seq,cur_type)
                # idx_seq = str(i)
                idx_seq.append(i)
                ent_list.append(ent)
                cur_type = tag_list[i][1]
            #continue of ent
            elif cur_type == tag_list[i][1] and ent_flag == True:
                # idx_seq +=  ' ' + str(i) 
                idx_seq.append(i)
            #begin of ent
            else:
                ent_flag = True
                cur_type = tag_list[i][1]
                # idx_seq = str(i)
                idx_seq.append(i)
        else:
            if ent_flag == True:
                ent = (idx_seq, ' '.join(sent.split()[idx_seq[0]:idx_seq[-1]+1]) ,cur_type)
                ent_list.append(ent)
                idx_seq = ''
                idx_seq = []
                ent_flag = False
            else:
                continue
        # print(ent_list)
    return ent_list


def tag_pairs(v_sent, e_sent):
    '''
    Perform NER tagging on a pair of sentence
    Input: pair of sentences
    Output: List entities in Vietnamese, List entities in English
    '''
    e_ents = getEntList(e_sent,e_ner)
    v_ents = getEntList(v_sent,v_ner)
    return e_ents, v_ents


def main():
    v_sent = 'Theo ông John Rockhold thì thị trường Việt Nam ẩn chứa nhiều thách thức .'
    e_sent = 'The Vietnamese market has several challenges according to HCMC director John Rockhold . '
    e_ents, v_ents = tag_pairs(v_sent,e_sent)
    print(e_ents)
    print(v_ents)

if __name__ == '__main__':
    main()
        

    
