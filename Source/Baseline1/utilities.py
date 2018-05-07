import re
import ast

source_length_pattern = re.compile(r'(?:source length\s+)(\d+)')
target_length_pattern = re.compile(r'(?:target length\s+)(\d+)')
score_pattern = re.compile(r'(?:alignment score\s:\s)([\d.e-]+)')

def wordLen(Sent):
    return len(Sent.split(' '))



def getSourceLength(info_line):
    source_length = re.search(source_length_pattern,info_line)
    # print(source_length)
    if source_length:
        return int(ast.literal_eval(source_length.group(1)))
    return 0


def getTargetLength(info_line):
    target_length = re.search(target_length_pattern,info_line)
    if target_length:
        return int(ast.literal_eval(target_length.group(1)))
    return 0

def getScore(info_line):
    score = re.search(score_pattern,info_line)
    if score:
        return float(ast.literal_eval(score.group(1)))
    return 0.0

def getSourceList(source_line):
    '''
    '''
    source_line_tokens = source_line.split()
    # print(sent_tokens)
    tp_list = []
    idx_seq = ''
    idx_flag = False
    word = ''
    for i in range(len(source_line_tokens)):
        if source_line_tokens[i] == '({':
            idx_flag = True
            word = source_line_tokens[i-1]
            continue
        elif source_line_tokens[i] == '})':
            word_dict = {'Word':word,'Index':[int(idx) for idx in idx_seq.split()]}
            tp_list.append(word_dict)
            idx_flag = False
            idx_seq = ''
            word = ''
        if idx_flag == True:
            idx_seq += source_line_tokens[i] + ' '
    return tp_list
    

def read_align_file(align_file):
    '''
    transform align file of Giza++ to align list
    Output:
    [
        {
            'Source_len':
            'Target_len':
            'Score':
            'Target': [words]
            'Source':
            [
                {
                    'Word':
                    'Index':[]
                }
            ]
        }
    ]
    '''
    res = []
    list_sent = open(align_file,encoding='utf-8').read().split('#')
    for i in range(1,len(list_sent)):
        item = {}
        cur_sent = list_sent[i]
        line_list = cur_sent.split('\n')
        info_line = line_list[0]
        target_line = line_list[1]
        source_line = line_list[2]
        source_len = getSourceLength(info_line)
        target_len = getTargetLength(info_line)
        score = getScore(info_line)
        target = target_line.split()
        source = getSourceList(source_line)
        item['Source_len'] = source_len
        item['Target_len'] = target_len
        item['Score']  = score
        item['Target'] = target
        item['Source'] = source
        res.append(item)
    return res

def make_unique(original_list):
    '''
    Remove duplicate element from list
    '''
    unique_list = []
    [unique_list.append(obj) for obj in original_list if obj not in unique_list]
    return unique_list