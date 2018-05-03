'''

'''

def is_overlapping(x1,x2,y1,y2):
    return max(x1,y1) <= min(x2,y2)

def getOverLapMatrix(CandidateSet):
    # for i in range(len(CandidateSet)):
        
    #     print('CandidateSet ', i, CandidateSet[i])
    res = [[False] * len(CandidateSet)] *len(CandidateSet)
    print('Res14', res[14])
    for i in range(len(CandidateSet)-1):
        for j in range(i+1,len(CandidateSet)):
            candidate_i = CandidateSet[i]
            candidate_j = CandidateSet[j]
            # print('Candidatei00', candidate_i[0][0])
            #English NE
            if len(candidate_i[0][0]) < 1 or len(candidate_j[0][0]) < 1:
                continue
            # print('Candidate I ',candidate_i)
            # print('Candidate J ',candidate_j)
            # print(candidate_i,candi)
            candidate_i_begin = candidate_i[0][0][0]
            candidate_i_end = candidate_i[0][0][-1]
            candidate_j_begin = candidate_j[0][0][0]
            candidate_j_end = candidate_j[0][0][-1]
            # print("English")
            # print(candidate_i_begin,candidate_i_end,candidate_j_begin,candidate_j_end)
            if is_overlapping(candidate_i_begin,candidate_i_end,candidate_j_begin,candidate_j_end):
                res[i][j] = True
                print('Candidate i',i,candidate_i)
                print('Candidate j', j ,candidate_j)

                # print("True")
            #Vietnamese NE
            if len(candidate_i[0][1]) < 1 or len(candidate_j[0][1]) < 1:
                continue
            # print("Vietnamese")
            # print('Candidate I ',candidate_i)
            # print('Candidate J ',candidate_j)
            
            candidate_i_begin = candidate_i[0][1][0]
            candidate_i_end = candidate_i[0][1][-1]
            candidate_j_begin = candidate_j[0][1][0]
            candidate_j_end = candidate_j[0][1][-1]
            # print(candidate_i_begin,candidate_i_end,candidate_j_begin,candidate_j_end)

            if is_overlapping(candidate_i_begin,candidate_i_end,candidate_j_begin,candidate_j_end):
                res[i][j] = True
                # print("True")
                print('Candidate i',i,candidate_i)
                print('Candidate j', j ,candidate_j)

    print('REs', res[14])
    return res

def getFinalNEPair(CombineScore,CandidateSet):
    '''
    '''
    res = []
    CandidateSet = list(zip(CandidateSet, CombineScore['TypeSens'], CombineScore['TypeInSens']))
    CandidateSet = sorted(CandidateSet,key=lambda CandidateSet: CandidateSet[2],reverse=True)
    # print(CandidateSet)
    checkOverLap = getOverLapMatrix(CandidateSet)
    print('Candidate Set',CandidateSet[14])
    print('Check overlap' ,checkOverLap[14])
    # get cur
    # remove overlap cur
    i = 0
    free = [True] * len(CandidateSet)
    for i in range(len(CandidateSet)):
        # print('CurCandidateSet ', CandidateSet[i])
        if (free[i]):
            cur = [CandidateSet[i]]
            # print('CurPredictSet ', cur)
            # Remove Overlap with Candidate i
            for j in range(i,len(CandidateSet)):
                if CandidateSet[j][1] == cur[0][1]:
                    cur.append(CandidateSet[j])
                if checkOverLap[i][j]:
                    free[j] = False
            res = res + cur
    
    res = reassign_type(res)
    return res

def reassign_type(ne_pairs):
    # print(ne_pairs_typeinsens[0])
    res = []
    for i in range(len(ne_pairs)):
        type_sens = ne_pairs[i][1]
        max_score = type_sens['ORGANIZATION']
        max_type = 'ORGANIZATION'
        for key,value in type_sens.items():
            if value > max_score:
                max_score = value
                max_type = key
        
        pair = (ne_pairs[i][0][0],ne_pairs[i][0][1],max_type,ne_pairs[i][0][3],ne_pairs[i][0][4],max_type)
        res.append(pair)
    return res

