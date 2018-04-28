import CombineScore as getCombineScore
import CandidateSet as getCandidateSet
import ranking as getFinalRes
def getNEPair(EtoV_sent, VtoE_sent, list_lambda,sent_index, train_mode  = False):
    '''
    Input: EtoV_sent, VtoE_sent
    Output: NE Pairs List of a sentence pair
    '''
    res = []
    if train_mode:
        CandidateSet = getCandidateSet.getCandidateSetFromFile(sent_index)
    else:
        CandidateSet = getCandidateSet.getCandidateSet(EtoV_sent,VtoE_sent, sent_index)
    CombineScore = getCombineScore.getCombineScore(CandidateSet,EtoV_sent,VtoE_sent, list_lambda,sent_index,train_mode = train_mode)
    res = getFinalRes.getFinalNEPair(CombineScore,CandidateSet)
    return res

# def getFinalPredictNEPairList_fromScoreTable(dev_list_EtoV,dev_list_VtoE)

def getFinalPredictNEPairList(align_list_EtoV, align_list_VtoE,list_lambda,train_mode = False):
    '''
    Input: align lists
    Output: predict pairs list
    '''
    res = []
    for i in range(len(align_list_EtoV)):
        ne_pairs = getNEPair(align_list_EtoV[i],align_list_VtoE[i], list_lambda,i,train_mode = train_mode)

        res.append(ne_pairs)
    return res
