en_file = 'eng_test.tsv'
vi_file = 'viet_test.tsv'

def getScoreTableEn():
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

def getScoreTableVi():
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