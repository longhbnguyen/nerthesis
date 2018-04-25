import getScoreTable

en_table = getScoreTable.getScoreTableEn()
vi_table = getScoreTable.getScoreTableVi()

def getMonoScore(ent, idx, mode):
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
    score = {}
    score['ORGANIZATION'] = org_score
    score['PERSON']  = per_score
    score['LOCATION'] = loc_score
    return score

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