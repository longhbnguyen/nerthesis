import CombineScore_InSens as getCombineScore_InSens
import CombineScore_TypeSens as getCombineScore_TypeSens
import CandidateSet as getCandidateSet
import ranking as getFinalRes
import config
import utilities
import ScoreTable

#Test
import DistortionModel.Distortion as Distortion

def getNEPair(EtoV_sent, VtoE_sent, list_lambda,sent_index,mode, train_mode_InSens  = False, train_mode_Sens = False):
    '''
    Input: EtoV_sent, VtoE_sent
    Output: NE Pairs List of a sentence pair
    '''
    res = []
    if train_mode_InSens or train_mode_Sens:
        CandidateSet = getCandidateSet.getCandidateSetFromFile(sent_index, mode)
    else:
        CandidateSet = getCandidateSet.getCandidateSet(EtoV_sent,VtoE_sent, sent_index)
    
    CombineScore = {}

    CombineScore['TypeSens'] = getCombineScore_TypeSens.getCombineScore(CandidateSet,EtoV_sent,VtoE_sent, list_lambda,sent_index,mode,train_mode = train_mode_Sens)
    CombineScore['TypeInSens'] = getCombineScore_InSens.getCombineScore(CandidateSet,EtoV_sent,VtoE_sent, list_lambda,sent_index,train_mode = train_mode_InSens)
    # print('CombineScore TypeSens', CombineScore['TypeSens'])
    res = getFinalRes.getFinalNEPair(CombineScore,CandidateSet,sent_index)
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

def main():
    # EtoV_dev_list = utilities.read_align_file('../../../Alignment_Split/EtoV_Dev.txt')
    # VtoE_dev_list = utilities.read_align_file('../../../Alignment_Split/VtoE_Dev.txt')
    # getCandidateSet.createCandidateSet(EtoV_dev_list,VtoE_dev_list,'dev')
    ScoreTable.createScoreTable_TypeSens(EtoV_dev_list,VtoE_dev_list,'dev')
    ScoreTable.createScoreTable_TypeInSens(EtoV_dev_list,VtoE_dev_list,'dev')
    # k = 0
    for i in range(len(EtoV_dev_list)):
        # k +=1
        # if (k>100):
            # break
        cur_candidate_list = getCandidateSet.getCandidateSetFromFile(i)
        for candidate in cur_candidate_list:
            tmp  = Distortion.getDistortionprob(candidate,EtoV_dev_list[i],VtoE_dev_list[i])
                # print('=============================')
                # print('Candidate: ',candidate)
        

if __name__ == '__main__':
    main()