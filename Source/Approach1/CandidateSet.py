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

candidate_set_file = 'Candidate_Set_Stanford_Test.json'
Candidate_Set_Table = None

EtoV_model.createEntListTable_Stanford()
VtoE_model.createEntListTable_Stanford()
EtoV_model.createEntListTable_Spacy()
VtoE_model.createEntListTable_Spacy()

# print(EtoV_model.initial_ent_list_spacy)
# print(VtoE_model.initial_ent_list_spacy)

def createCandidateSetForTraining(EtoV_List,VtoE_List):
    global Candidate_Set_Table
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
    '''


    EtoV_set = EtoV_model.getEntSetFromFile(EtoV_sent['Source'],EtoV_sent['Target'], sent_index)
    VtoE_set = VtoE_model.getEntSetFromFile(VtoE_sent['Source'],VtoE_sent['Target'], sent_index)
    V_Ent_List = []
    E_Ent_List = []
    # print('EtoVSet')
    for pair in EtoV_set:
        # print('Pair ' ,pair)
        v_ent = (pair[1],pair[2],pair[4])
        e_ent = (pair[0],pair[2],pair[3])
        if e_ent not in E_Ent_List:
            E_Ent_List.append(e_ent)
        if v_ent not in V_Ent_List:
            V_Ent_List.append(v_ent)
    # print('VtoESet')
    for pair in VtoE_set:
        # print('Pair ' ,pair)        
        e_ent = (pair[1],pair[2],pair[4])
        v_ent = (pair[0],pair[2],pair[3])
        if e_ent not in E_Ent_List:
            E_Ent_List.append(e_ent)
        if v_ent not in V_Ent_List:
            V_Ent_List.append(v_ent)
    # V_Ent_List = (set(V_Ent_List))
    # E_Ent_List = (set(E_Ent_List))
    # print('E_Ent_List ',E_Ent_List)
    # print('V_Ent_List ',V_Ent_List)
    res = []
    for en_ent in E_Ent_List:
        for vn_ent in V_Ent_List:
            res.append((en_ent[0],vn_ent[0],en_ent[1],en_ent[2],vn_ent[2],vn_ent[1]))
    return res

def getCandidateSetFromFile(sent_index):
    return Candidate_Set_Table[sent_index]


# EtoV_dev_list = utilities.read_align_file('../../Alignment_Split/EtoV_Dev.txt')
# VtoE_dev_list = utilities.read_align_file('../../Alignment_Split/VtoE_Dev.txt')

# tmp = getCandidateSet(EtoV_dev_list[0],VtoE_dev_list[0],0)
# print(tmp)
# print(len(tmp))