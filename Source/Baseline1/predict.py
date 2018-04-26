import CombineScore as getCombineScore
import CandidateSet as getCandidateSet
import ranking as getFinalRes
def getNEPair(EtoV_sent, VtoE_sent,train_mode  = False, list_lambda,sent_index):
    '''
    Input: EtoV_sent, VtoE_sent
    Output: NE Pairs List of a sentence pair
    '''
    res = []
    CandidateSet = getCandidateSet.getCandidateSet(EtoV_sent,VtoE_sent)
    CombineScore = getCombineScore.getCombineScore(CandidateSet,EtoV_sent,VtoE_sent,train_mode = train_mode=, list_lambda,sent_index)
    res = getFinalRes.getFinalNEPair(CombineScore,CandidateSet)
    return res

# def getFinalPredictNEPairList_fromScoreTable(dev_list_EtoV,dev_list_VtoE)

def getFinalPredictNEPairList(align_list_EtoV, align_list_VtoE,train_mode = False,list_lambda):
    '''
    Input: align lists
    Output: predict pairs list
    '''
    res = []
    for i in range(len(align_list_EtoV)):
        ne_pairs = getNEPair(align_list_EtoV[i],align_list_VtoE[i],train_mode = train_mode, list_lambda,i)

        res.append(ne_pairs)
    return res
