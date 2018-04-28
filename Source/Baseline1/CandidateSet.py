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

candidate_set_file = 'Candidate_Set_Test.json'
Candidate_Set_Table = None
def createCandidateSetForTraining(EtoV_List,VtoE_List):
    global Candidate_Set_Table
    if os.path.isfile(candidate_set_file):
        json_data=open(candidate_set_file).read()
        Candidate_Set_Table = json.loads(json_data)
    else:
        Candidate_Set_Table = []
        for i in range(len(EtoV_List)):
            Candidate_Set_Table.append(getCandidateSet(EtoV_List[i],VtoE_List[i]))
        with open(candidate_set_file,'w',encoding='utf-8') as f:
            json.dump(Candidate_Set_Table,f)

    

def getCandidateSet(EtoV_sent,VtoE_sent):
    '''
    '''
    EtoV_set = EtoV_model.getEntSet(EtoV_sent['Source'],EtoV_sent['Target'])

    VtoE_set = VtoE_model.getEntSet(VtoE_sent['Source'],VtoE_sent['Target'])
    V_Ent_List = []
    E_Ent_List = []
    # print('EtoVSet')
    for pair in EtoV_set:
        # print('Pair ' ,pair)
        V_Ent_List.append((pair[1],pair[2],pair[4]))
        E_Ent_List.append((pair[0],pair[2],pair[3]))
    # print('VtoESet')
    for pair in VtoE_set:
        # print('Pair ' ,pair)        
        E_Ent_List.append((pair[1],pair[2],pair[4]))
        V_Ent_List.append((pair[0],pair[2],pair[3]))
    # print('E_Ent_List ',E_Ent_List)
    # print('V_Ent_List ',V_Ent_List)

    res = []
    for en_ent in E_Ent_List:
        for vn_ent in V_Ent_List:
            res.append((en_ent[0],vn_ent[0],en_ent[1],en_ent[2],vn_ent[2],vn_ent[1]))
    # res = EtoV_set + VtoE_set
    return res

def getCandidateSetFromFile(sent_index):
    return Candidate_Set_Table[sent_index]


# EtoV_dev_list = utilities.read_align_file('../../Alignment_Split/EtoV_Dev.txt')
# VtoE_dev_list = utilities.read_align_file('../../Alignment_Split/VtoE_Dev.txt')

# tmp = getCandidateSet(EtoV_dev_list[0],VtoE_dev_list[0])
# print(tmp)
# print(len(tmp))