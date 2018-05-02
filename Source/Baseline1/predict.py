import CombineScore_InSens as getCombineScore_InSens
import CombineScore_TypeSens as getCombineScore_TypeSens
import CandidateSet as getCandidateSet
import ranking as getFinalRes
def getNEPair(EtoV_sent, VtoE_sent, list_lambda,sent_index, train_mode_InSens  = False, train_mode_Sens = False):
    '''
    Input: EtoV_sent, VtoE_sent
    Output: NE Pairs List of a sentence pair
    '''
    res = []
    if train_mode_InSens:
        CandidateSet = getCandidateSet.getCandidateSetFromFile(sent_index)
    else:
        CandidateSet = getCandidateSet.getCandidateSet(EtoV_sent,VtoE_sent, sent_index)
    
    CombineScore = {}

    CombineScore['TypeSens'] = getCombineScore_TypeSens.getCombineScore(CandidateSet,EtoV_sent,VtoE_sent, list_lambda,sent_index,train_mode = train_mode_Sens)

    CombineScore['TypeInSens'] = getCombineScore_InSens.getCombineScore(CandidateSet,EtoV_sent,VtoE_sent, list_lambda,sent_index,train_mode = train_mode_InSens)

    
    res = getFinalRes.getFinalNEPair(CombineScore,CandidateSet)
    return res

# def getFinalPredictNEPairList_fromScoreTable(dev_list_EtoV,dev_list_VtoE)

def getFinalPredictNEPairList(align_list_EtoV, align_list_VtoE,list_lambda,train_mode_InSens = False, train_mode_Sens = False):
    '''
    Input: align lists
    Output: predict pairs list
    '''
    res = []
    for i in range(len(align_list_EtoV)):
        ne_pairs = getNEPair(align_list_EtoV[i],align_list_VtoE[i], list_lambda,i,train_mode_InSens= train_mode_InSens, train_mode_Sens= train_mode_Sens)

        res.append(ne_pairs)
    return res
