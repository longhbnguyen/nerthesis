'''
Get Candidate Set
Input:      EtoV_sent,VtoE_sent
EtoV_sent:
    {
            'Source_len':
            'Target_len':
            'Score':
            'Target': [words]
            'Source':
            [
                'Word':
                'Index':[]
            ]
    }
output Candidate set of that sent

'''

from AlignmentModel import EtoV_model, VtoE_model
import utilities
import json
import os.path

candidate_set_test_file = 'Candidate_Set_Test.json'
candidate_set_dev_file = 'Candidate_Set_Dev.json'

Candidate_Set_Table = None



def createCandidateSet(EtoV_List,VtoE_List, mode):
    '''
    Create CandidateSet file
    '''
    global Candidate_Set_Table
    EtoV_model.createEntListTable_Stanford(mode)
    VtoE_model.createEntListTable_Stanford(mode)
    if mode == 'dev':
        candidate_set_file = candidate_set_dev_file
    elif mode == 'test':
        candidate_set_file = candidate_set_test_file
    if os.path.isfile(candidate_set_file):
        json_data=open(candidate_set_file).read()
        Candidate_Set_Table = json.loads(json_data)
    else:
        Candidate_Set_Table = []
        for i in range(len(EtoV_List)):
            Candidate_Set_Table.append(getCandidateSet(EtoV_List[i],VtoE_List[i],i))
        with open(candidate_set_file,'w',encoding='utf-8') as f:
            json.dump(Candidate_Set_Table,f)

    
def getCandidateSet(EtoV_sent,VtoE_sent, sent_index):
    '''
    Get Candidate Set of 1 sentence pair
    '''


    EtoV_set = EtoV_model.getEntSetFromFile(EtoV_sent['Source'],EtoV_sent['Target'], sent_index)
    VtoE_set = VtoE_model.getEntSetFromFile(VtoE_sent['Source'],VtoE_sent['Target'], sent_index)
    V_Ent_List = []
    E_Ent_List = []
    for pair in EtoV_set:
        V_Ent_List.append((pair[1],pair[2],pair[4]))
        E_Ent_List.append((pair[0],pair[2],pair[3]))
    for pair in VtoE_set:
        E_Ent_List.append((pair[1],pair[2],pair[4]))
        V_Ent_List.append((pair[0],pair[2],pair[3]))
    
    res = []
    for en_ent in E_Ent_List:
        for vn_ent in V_Ent_List:
            res.append((en_ent[0],vn_ent[0],en_ent[1],en_ent[2],vn_ent[2],vn_ent[1]))
    res = utilities.make_unique(res)
    return res

def getCandidateSetFromFile(sent_index):
    return Candidate_Set_Table[sent_index]


# EtoV_dev_list = utilities.read_align_file('../../Alignment_Split/EtoV_Test.txt')
# VtoE_dev_list = utilities.read_align_file('../../Alignment_Split/VtoE_Test.txt')

# tmp = getCandidateSet(EtoV_dev_list[-1],VtoE_dev_list[-1],len(EtoV_dev_list)-1)
# unique = utilities.make_unique(tmp)
# print('tmp',tmp)
# print('unique',unique)
# print(len(tmp))
# print(len(unique))