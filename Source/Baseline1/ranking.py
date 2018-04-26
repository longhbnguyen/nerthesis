'''

'''

def is_overlapping(x1,x2,y1,y2):
    return max(x1,y1) <= min(x2,y2)

def getOverLapMatrix(CandidateSet):
    res = [[False] * len(CandidateSet)] *len(CandidateSet)
    for i in range(len(CandidateSet)):
        for j in range(i+1,len(CandidateSet)):
            candidate_i = CandidateSet[i]
            candidate_j = CandidateSet[j]
            # print('Candidate I ',candidate_i)
            # print('Candidate J ',candidate_j)
            candidate_i_begin = candidate_i[0][0][0]
            candidate_i_end = candidate_i[0][0][-1]
            candidate_j_begin = candidate_j[0][0][0]
            candidate_j_end = candidate_j[0][0][-1]
            if is_overlapping(candidate_i_begin,candidate_i_end,candidate_j_begin,candidate_j_end):
                res[i][j] = True
    return res
def getFinalNEPair(CombineScore,CandidateSet):
    '''
    '''
    res = []
    CandidateSet = zip(CandidateSet,CombineScore) 
    CandidateSet = sorted(CandidateSet,key=lambda CandidateSet: CandidateSet[1],reverse=True)
    checkOverLap = getOverLapMatrix(CandidateSet)
    # get cur
    # remove overlap cur
    i = 0
    free = [True] * len(CandidateSet)
    for i in range(len(CandidateSet)):
        if (free[i]):
            cur = CandidateSet[i]
            # Remove Overlap with Candidate i
            for j in range(i,len(CandidateSet)):
                if checkOverLap[i][j]:
                    free[i] = False
            res.append(cur)
    return res