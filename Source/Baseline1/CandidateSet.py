'''
Get Candidate Set
Input:      EtoV_sent,VtoE_sent
EtoV_sent:
    {
            'Source_len':
            'Target_len':
            'Score':
            'Source': [words]
            'Target':
            [
                'Word':
                'Index':[]
            ]
    }
output Candidate set of that sent

'''

from AlignmentModel import EtoV_model, VtoE_model

def getCandidateSet(EtoV_sent,VtoE_sent):
    '''
    '''
    EtoV_set = EtoV_model.getEntSet(EtoV_sent['Source'],EtoV_sent['Target'])
    VtoE_set = VtoE_model.getEntSet(VtoE_sent['Source'],VtoE_sent['Target'])
    res = EtoV_set + VtoE_set
    return res