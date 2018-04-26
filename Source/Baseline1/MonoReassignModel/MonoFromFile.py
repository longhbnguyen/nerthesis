import MonoReassignModel.getScoreTable

en_table = getScoreTable.getScoreTableEn()
vi_table = getScoreTable.getScoreTableVi()

def getMonoScore(ent, idx,mode):
    if mode == 'en':
        table = en_table
    elif mode == 'vi':
        table = vi_table
    per_score = 1.0
    org_score = 1.0
    loc_score = 1.0
    for i in ent[0]:
        org_score *= table[idx][i-1][2]
        per_score *= table[idx][i-1][3]
        loc_score *= table[idx][i-1][4]
    org_tp = ('ORGANIZATION',org_score)
    per_tp = ('PERSON', per_score)
    loc_tp = ('LOCATION', loc_score)
    scores = [org_tp,per_tp,loc_tp]
    scores = sorted(scores, key = lambda score: score[1], reverse = True)

    max_label = scores[0][0]
    return max_label

def getMonoProb(cur_candidate, sent_idx):
    e_ent_idx = cur_candidate[0]
    v_ent_idx = cur_candidate[1]
    e_ent_label = getMonoScore(e_ent_idx,sent_idx,'en')
    v_ent_label = getMonoScore(v_ent_idx,sent_idx,'vi')
    return e_ent_label, v_ent_label

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