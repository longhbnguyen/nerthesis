
def getNEPair(EtoV_sent, VtoE_sent):
    '''
    Input: EtoV_sent, VtoE_sent
    Output: NE Pairs List of a sentence pair
    '''
    res = []
    CandidateSet = getCandidateSet.getCandidateSet(EtoV_sent,VtoE_sent)
    CombineScore = getCombineScore.getCombineScore(CandidateSet,EtoV_sent,VtoE_sent)
    res = getFinalRes.getFinalNEPair(CombineScore,CandidateSet)
    return res

def getFinalPredictNEPair(align_list_EtoV, align_list_VtoE):
    '''
    Input: align lists
    Output: predict pairs list
    
    '''
    res = []
    for i in range(len(align_list_EtoV)):
        ne_pairs = getNEPair(align_list_EtoV[i],align_list_VtoE[i])

        res.append(ne_pairs)
    return res
