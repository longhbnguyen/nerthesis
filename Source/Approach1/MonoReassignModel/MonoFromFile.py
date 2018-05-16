import MonoReassignModel.getScoreTable as getScoreTable


def normalize(score,n):
    return score**(1/n)


def getMonoScore(ent, idx, mode, run_mode):
    n = len(ent)

    if n == 0:
        scores = {}
        scores['ORGANIZATION'] = 0.0
        scores['PERSON'] = 0.0
        scores['LOCATION'] = 0.0
        return scores
    
    en_table = getScoreTable.getScoreTableEn(run_mode)
    vi_table = getScoreTable.getScoreTableVi(run_mode)

    if mode == 'en':
        table = en_table
    elif mode == 'vi':
        table = vi_table
    per_score = 1.0
    org_score = 1.0
    loc_score = 1.0
    # print(ent)
    for i in ent:
        org_score *= table[idx][i-1][2]
        per_score *= table[idx][i-1][3]
        loc_score *= table[idx][i-1][4]
    scores = {}
    
    scores['ORGANIZATION'] = org_score
    scores['PERSON'] = per_score
    scores['LOCATION'] = loc_score

    # scores = sorted(scores, key = lambda score: score[1], reverse = True)
    # max_label = scores[0][0]
    # max_score = scores[0][1]
    return scores
    

def getMonoProb(cur_candidate, sent_idx,mode):
    # print(cur_candidate)
    e_ent_idx = cur_candidate[0]
    v_ent_idx = cur_candidate[1]
    e_ent_scores = getMonoScore(e_ent_idx,sent_idx,'en',mode)
    v_ent_scores = getMonoScore(v_ent_idx,sent_idx,'vi',mode)
    pair_score = {}
    pair_score['EN'] = e_ent_scores
    pair_score['VN'] = v_ent_scores
    return pair_score    

def main():
    ent = ([10,11],'PERSON')
    idx = 0
    mode = 'en'
    print(en_table[0][9][0])
    print(en_table[0][10][0])

    score = getMonoScore(ent,idx,mode)
    print(score)

if __name__ == '__main__':
    main()