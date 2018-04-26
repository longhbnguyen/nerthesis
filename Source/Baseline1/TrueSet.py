import re

en_file = '../../Data/corpora/0_DATA/2_Development/dev_eng'
vn_file = '../../Data/corpora/0_DATA/2_Development/dev_viet'

ent_pattern = re.compile(r"(<[A-Z]+\_\d+>)([^</>]*)(</[A-Z]+\_\d+>)")
ent_type_pattern = re.compile(r"(<([A-Z]+)\_\d+>)")

def get_index(ent,sent):
    index = []
    word_list = sent.split()
    # print(ent.group(1))
    # print(word_list)
    cur_ent_word = ent.group(0)
    # print(cur_ent_word)
    for i in range(len(word_list)):
        if ent.group(1) in word_list[i]:
            index = list(range(i+1,i+len(cur_ent_word.split())+1))
            break
    return index

def clearEntityType(ent_type):
    return re.search(ent_type_pattern,ent_type).group(2)

def getSentTrueSet(en_sent,vn_sent):
    res = []
    en_list = [ent for ent in re.finditer(ent_pattern,en_sent)]
    vn_list = [ent for ent in re.finditer(ent_pattern,vn_sent)]
    # print(en_list)
    en_type_set = set([en.group(1) for en in en_list])
    vi_type_set = set([vi.group(1) for vi in vn_list])
    intersect_type_set = en_type_set.intersection(vi_type_set)
    for ent_type in list(intersect_type_set):
        for en in en_list:
            if (ent_type == en.group(1)):
                en_entity = en
                break
        for vn in vn_list:
            if (ent_type == vn.group(1)):
                vn_entity = vn
                break
        en_index = get_index(en_entity,en_sent)
        vn_index = get_index(vn_entity,vn_sent)
        cur_type = clearEntityType(ent_type)
        en_word = en_entity.group(2)
        vn_word = vn_entity.group(2)
        cur_NE_Pair = (en_index,vn_index,cur_type,en_word,vn_word)
        res.append(cur_NE_Pair)
        
    return res
        
def getFileTrueSet(en_file,vn_file):
    res = []
    en_list = open(en_file,'r',encoding='utf-8').read().split('\n')
    vn_list = open(vn_file,'r',encoding='utf-8').read().split('\n')

    for i in range(len(en_list)):
        res.append(getSentTrueSet(en_list[i],vn_list[i]))


    return res
