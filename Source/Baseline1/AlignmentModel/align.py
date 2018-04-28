import EtoV_model as etov
import VtoE_model as vtoe





def getCandidateSet(v_sent,e_sent):
    v_set = etov.getEntSet(e_sent,v_sent)
    e_set = vtoe.getEntSet(v_sent,e_sent)
    cand_set = set(v_set+e_set)
    return cand_set
