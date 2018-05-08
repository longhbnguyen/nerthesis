en_file_test = './MonoReassignModel/eng_test.tsv'
vi_file_test = './MonoReassignModel/viet_test.tsv'

en_file_dev = './MonoReassignModel/eng_dev.tsv'
vi_file_dev = './MonoReassignModel/viet_dev.tsv'

def getScoreTableEn(mode):
    if mode == 'dev':
        en_file = en_file_dev
    elif mode == 'test':
        en_file = en_file_test
    table = []
    sent = []
    with open(en_file,'r',encoding = 'utf-8') as f:
        for line in f:
            if line == '\n':
                table.append(sent)
                sent = []
                continue
            word = line.split()
            content = word[0]
            o_score = float(word[2][word[2].find('=')+1:])
            org_score = float(word[3][word[3].find('=')+1:])
            per_score = float(word[4][word[4].find('=')+1:])
            loc_score = float(word[5][word[5].find('=')+1:])
            tp = (content,o_score,org_score,per_score,loc_score)
            sent.append(tp)
            
    return table

def getScoreTableVi(mode):
    if mode == 'dev':
        vi_file = vi_file_dev
    elif mode == 'test':
        vi_file = vi_file_test
    
    table = []
    sent = []
    with open(vi_file,'r',encoding = 'utf-8') as f:
        for line in f:
            if line == '\n':
                table.append(sent)
                sent = []
                continue
            word = line.split()
            content = word[0]
            o_score = float(word[2][word[2].find('=')+1:])
            org_score = float(word[3][word[3].find('=')+1:])
            per_score = float(word[4][word[4].find('=')+1:])
            loc_score = float(word[5][word[5].find('=')+1:])
            tp = (content,o_score,org_score,per_score,loc_score)
            sent.append(tp)
    return table