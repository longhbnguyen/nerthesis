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
def getCandidateSet(EtoV_sent,VtoE_sent):
    '''
    '''
    EtoV_set = EtoV_model.getEntSet(EtoV_sent['Source'],EtoV_sent['Target'])

    VtoE_set = VtoE_model.getEntSet(VtoE_sent['Source'],VtoE_sent['Target'])
    V_Ent_List = []
    E_Ent_List = []
    for pair in EtoV_set:
        V_Ent_List.append((pair[1],pair[2],pair[4]))
        E_Ent_List.append((pair[0],pair[2],pair[3]))
    for pair in VtoE_set:
        V_Ent_List.append((pair[1],pair[2],pair[4]))
        E_Ent_List.append((pair[0],pair[2],pair[3]))
    res = []
    for en_ent in E_Ent_List:
        for vn_ent in V_Ent_List:
            res.append((en_ent[0],vn_ent[0],en_ent[1],en_ent[2],vn_ent[2],vn_ent[1]))
    # res = EtoV_set + VtoE_set
    return res
