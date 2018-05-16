'''

'''
import numpy as np

# def is_overlapping(x1,x2,y1,y2):
    # return max(x1,y1) <= min(x2,y2)
def is_overlapping(id_x, id_y):
    '''
    Checked
    '''
    # print('===============')
    # print('id_x', id_x)
    # print('id_y', id_y)

    set_id_x = set(id_x)
    set_id_y = set(id_y)
    intersect = set_id_x.intersection(set_id_y)
    # print('intersect ',intersect)
    if len(intersect) > 0:
        # print('True')
        return True
    else:
        return False


def getOverLapMatrix(CandidateSet):
    '''
    Checked
    '''
    res = np.full((len(CandidateSet),len(CandidateSet)),False)
    for i in range(len(CandidateSet)-1):
        candidate_i = CandidateSet[i]
        for j in range(i+1,len(CandidateSet)):
            # print('==================')
            candidate_j = CandidateSet[j]
            tmp = (is_overlapping(candidate_i[0][0],candidate_j[0][0]) or is_overlapping(candidate_i[0][1],candidate_j[0][1]))
            # print(res[2][0])
            # print(tmp)
            # print(res[2][0])
            res[i][j] = tmp
            res[j][i] = tmp
        
    #Test
    
    # for i in range(len(CandidateSet)):
    #     for j in range(len(CandidateSet)):
    #         # print("Candidate i", CandidateSet[i])
    #         # print("Candidate j", CandidateSet[j])
    #         # print("Res i j",i,j,res[i][j])
    #         if res[i][j] != res[j][i]:
    #             print('Res',i,j,'-','Res',j,i)
    return res

def getFinalNEPair(CombineScore,CandidateSet,sent_index):
    '''

    '''
    # print('========================')
    res = []
    if (not len(CandidateSet)):
        return CandidateSet
    # print('Init', CandidateSet)
    CandidateSet = list(zip(CandidateSet, CombineScore['TypeSens'], CombineScore['TypeInSens']))
    CandidateSet = sorted(CandidateSet,key=lambda CandidateSet: CandidateSet[2],reverse=True)
    if len(CandidateSet) == 1:
        # print('LenCandidate=0',tuple(CandidateSet[0][0]) + (sent_index,0))
        return [tuple(CandidateSet[0][0]) + (sent_index,0)]
    # for i in range(len(CandidateSet)):
    #     print('Initial NE Pair', i , CandidateSet[i])
    checkOverLap = getOverLapMatrix(CandidateSet)
    # get cur
    # remove overlap cur
    i = 0
    free = [True] * len(CandidateSet)
    for i in range(len(CandidateSet)-1):
        # print('CurCandidateSet ', CandidateSet[i])
        # print('=================')
        if (free[i]):
            tmp = CandidateSet[i] + (sent_index,i)
            
            cur = [tmp]
            # print('CurCandidate ', cur)
            # Remove Overlap with Candidate i
            
            for j in range(i+1,len(CandidateSet)):
                # print('=================')
            
                # print('CurCandidate ', cur[0])
                
                # print('CompareCandidate', CandidateSet[j])
                if CandidateSet[j][0][0] == cur[0][0][0] and CandidateSet[j][0][1] == cur[0][0][1] :
                    # print(CandidateSet[j][2])
                    # print(cur[0][2])
                    # print('Same Score')
                    tmp = CandidateSet[j] + (sent_index,j)
                    # print('TMP', tmp)
                    cur.append(tmp)
                if checkOverLap[i][j] or checkOverLap[j][i]:
                    # print('Overlap')
                    free[j] = False
            # print('CurrentSet', cur)
            res = res + cur
            # print('Res', res)
    # print(CandidateSet)
    if free[len(CandidateSet)-1]:
        res = res + [CandidateSet[-1]+(sent_index,len(CandidateSet)-1)]
    # print('Before Reassign', res)
    res = reassign_type(res)
    # print('After Reassign', res)
    return res

def eliminate_duplicate_pairs(CandidateSet):
    res = []
    if len(CandidateSet) <= 1:
        return CandidateSet
    CandidateSet = sorted(CandidateSet,key=lambda CandidateSet: CandidateSet[1],reverse=True)

    # print('Before', CandidateSet)
    checkOverLap = getOverLapMatrix(CandidateSet)
    # print('CandidateSet',CandidateSet)
    i = 0
    free = [True] * len(CandidateSet)
    for i in range(len(CandidateSet)-1):
        if (free[i]):
            cur = [CandidateSet[i]]
            for j in range(i+1,len(CandidateSet)):
                # print('===============')
                # print('CurCandidate', cur)
                # print('CompareCandidate', CandidateSet[j])
                if checkOverLap[i][j] or checkOverLap[j][i]:
                    # print('Overlap')
                    free[j] = False
            res = res + cur
            # print('Res', res)
    if free[len(CandidateSet)-1]:
        res = res + [CandidateSet[-1]]
    final_res = []
    for i in range(len(res)):
        tmp = res[i][0] + (res[i][-2],res[i][-1])
        final_res.append(tmp)
    # print('EliminateDuplicate', final_res)    
    return final_res

def reassign_type(ne_pairs):
    '''checked'''
    # print('NE_Pairs',ne_pairs)
    # checkOverLap = getOverLapMatrix(ne_pairs)
    res = []
    # for i in range(len(ne_pairs)):
    #     print('NE Pair',i,ne_pairs[i])
    for i in range(len(ne_pairs)):
        # print('===============')
        # print('Initial NE Pair ',i,ne_pairs[i])
        type_sens = ne_pairs[i][1]
        max_score = type_sens['ORGANIZATION']
        max_type = 'ORGANIZATION'
        for key,value in type_sens.items():
            if value > max_score:
                max_score = value
                max_type = key
        
        # print('NE Pair',ne_pairs[i])
        pair = ((ne_pairs[i][0][0],ne_pairs[i][0][1],max_type,ne_pairs[i][0][3],ne_pairs[i][0][4],max_type),max_score,ne_pairs[i][-2],ne_pairs[i][-1])

        # print('Final NE Pair ',i,pair)        
        res.append(pair)
    res = eliminate_duplicate_pairs(res)

    return res


'''Test'''
# candidate_i = (([19], [27], 'LOCATION', 'California', 'California', 'LOCATION'), {'ORGANIZATION': 0.016824989780286063, 'PERSON': 1.7015859664557756e-05, 'LOCATION': 0.28218290409288943}, 0.36594993859649116)
# candidate_j = (([2, 3, 4], [26, 27], 'ORGANIZATION', 'National Weather Service', 'biển California', 'LOCATION'), {'ORGANIZATION': 0.1521425840107209, 'PERSON': 1.260924226036337e-10, 'LOCATION': 0.13503773007786968}, 0.13999999999999999)
# tmp = is_overlapping(candidate_i[0][0],candidate_j[0][0]) or is_overlapping(candidate_i[0][1],candidate_j[0][1])
# print(tmp)

