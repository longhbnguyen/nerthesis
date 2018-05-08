import CombineScore_InSens as getCombineScore_InSens
import CombineScore_TypeSens as getCombineScore_TypeSens
import CandidateSet as getCandidateSet
import ranking as getFinalRes
import config
import utilities
import ScoreTable

def getNEPair(EtoV_sent, VtoE_sent, list_lambda,sent_index,mode, train_mode_InSens  = False, train_mode_Sens = False):
    '''
    Input: EtoV_sent, VtoE_sent
    Output: NE Pairs List of a sentence pair
    '''
    res = []
    if train_mode_InSens or train_mode_Sens:
        CandidateSet = getCandidateSet.getCandidateSetFromFile(sent_index)
    else:
        CandidateSet = getCandidateSet.getCandidateSet(EtoV_sent,VtoE_sent, sent_index)
    
    CombineScore = {}

    CombineScore['TypeSens'] = getCombineScore_TypeSens.getCombineScore(CandidateSet,EtoV_sent,VtoE_sent, list_lambda,sent_index,mode,train_mode = train_mode_Sens)
    CombineScore['TypeInSens'] = getCombineScore_InSens.getCombineScore(CandidateSet,EtoV_sent,VtoE_sent, list_lambda,sent_index,train_mode = train_mode_InSens)
    # print('CombineScore TypeSens', CombineScore['TypeSens'])
    res = getFinalRes.getFinalNEPair(CombineScore,CandidateSet)
    res = utilities.make_unique(res)
    # print('After Reassign', res)
    return res

# def getFinalPredictNEPairList_fromScoreTable(dev_list_EtoV,dev_list_VtoE)

def getFinalPredictNEPairList(align_list_EtoV, align_list_VtoE,list_lambda,mode,train_mode_InSens = False, train_mode_Sens = False):
    '''
    Input: align lists
    Output: predict pairs list
    '''
    res = []
    for i in range(len(align_list_EtoV)):
        # print('======================')
        ne_pairs = getNEPair(align_list_EtoV[i],align_list_VtoE[i], list_lambda,i,mode,train_mode_InSens= train_mode_InSens, train_mode_Sens= train_mode_Sens)

        res.append(ne_pairs)
    return res


# EtoV_dev_list = utilities.read_align_file('../../Alignment_Split/EtoV_Test.txt')
# VtoE_dev_list = utilities.read_align_file('../../Alignment_Split/VtoE_Test.txt')
# ScoreTable.createScoreTable_TypeSens(EtoV_dev_list,VtoE_dev_list,'test')
# ScoreTable.createScoreTable_TypeInSens(EtoV_dev_list,VtoE_dev_list,'test')
# getCandidateSet.createCandidateSet(EtoV_dev_list,VtoE_dev_list,'test')
# # print(getCandidateSet.Candidate_Set_Table[-1])
# # # tmp = getCandidateSet(EtoV_dev_list[0],VtoE_dev_list[0],0)
# list_lambda = config.getWeight()
# # print(EtoV_dev_list[0])
# # print(VtoE_dev_list[0])

# res = getNEPair(EtoV_dev_list[788],VtoE_dev_list[788],list_lambda,788, train_mode_InSens=True)
# for pair in res:
#     print(pair)
# # print(len(tmp))
