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

# source_line = 'NULL ({ 10 18 24 }) Dịch ({ }) vụ ({ }) Thời ({ 1 }) tiết ({ }) Quốc ({ }) gia ({ }) nói ({ 5 }) với ({ }) chúng ({ 6 }) tôi ({ }) chiều ({ 8 }) nay ({ 7 }) nó ({ 9 }) là ({ }) El ({ 2 4 11 29 31 33 }) Nino ({ 3 12 32 }) gây ({ 13 }) ra ({ }) những ({ 14 }) con ({ }) sóng ({ 16 }) khổng ({ 15 }) lồ ({ }) trên ({ 17 }) bờ ({ 20 }) biển ({ }) California ({ 19 }) , ({ 21 }) và ({ 22 }) mặc ({ 23 }) dù ({ }) có ({ }) đê ({ 26 }) cát ({ 25 }) , ({ 27 }) một ({ }) số ({ 28 }) căn ({ }) nhà ({ }) phía ({ }) trước ({ 30 }) đại ({ }) dương ({ }) đã ({ }) bị ({ }) lũ ({ }) lụt ({ 34 }) nhỏ ({ }) . ({ 35 }) '

# source = getSourceList(source_line)
# print(source)

res = read_align_file('../../Alignment_Split/EtoV_Dev.txt')
print(res[0])

