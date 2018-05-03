'''

'''
import numpy as np
import config
import ScoreTable
import utilities
import TranslationModel.TranslationModel as TranslationProb
import TransliterationModel.Transliteration as TransliterationProb
import Co_occurrenceModel.Co_occurrence as CoocurenceProb
import DistortionModel.Distortion as DistortionProb
import MonoReassignModel.MonoFromFile as MonoProb
import BiReassignModel.ReassignModel as BiProb
import CandidateSet

def getWeightDict():
    '''
    '''
    weight_dict = config.getWeight()
    return weight_dict

def getDictDot(score_dict,weight_dict):
    '''
    '''
    res = {}
    res['ORGANIZATION'] = 0.0
    res['PERSON'] = 0.0
    res['LOCATION'] = 0.0
    for key,value in score_dict.items():
        for sub_key,sub_value in score_dict[key].items():
            if sub_key == 'EN' or sub_key == 'VN':
                tmp_key = key + '_' + sub_key.lower()
                for label,label_value in score_dict[key][sub_key].items():
                    res[label] = res[label] + (score_dict[key][sub_key][label]) * (weight_dict[tmp_key])
            else:
                res[sub_key] = res[sub_key] + (score_dict[key][sub_key]) * (weight_dict[key])
                
    return res




def getScoreDictForSet_TypeSens(CandidateSet,EtoV_sent,VtoE_sent,sent_index):
    res = []
    for candidate in CandidateSet:
        res.append(getScoreDict(candidate,EtoV_sent,VtoE_sent,sent_index))
    return res

def getScoreDict(cur_candidate,EtoV_sent,VtoE_sent,sent_index):
    mono_score = MonoProb.getMonoProb(cur_candidate,sent_index)
    bi_score = BiProb.getBiProb(cur_candidate)
    score_dict= {}
    score_dict['mono'] = mono_score
    score_dict['bi'] = bi_score
    return score_dict

def getCombineScoreCandidate(cur_candidate,EtoV_sent,VtoE_sent,weight_dict,sent_index,candidate_index,train_mode = False):
    '''

    '''
    score = 0.0
    if train_mode:
        score_dict = ScoreTable.getScoreforOneCandidate_TypeSens(sent_index,candidate_index)
    else:
        score_dict = getScoreDict(cur_candidate, EtoV_sent, VtoE_sent,sent_index)
    score = getDictDot(score_dict,weight_dict)
    return score

def getCombineScore(CandidateSet,EtoV_sent,VtoE_sent,list_lambda,sent_index,train_mode = False):
    '''
    '''
    if train_mode:
        weight_dict = list_lambda
    else: 
        weight_dict = getWeightDict()
    res = []
    for i in range(len(CandidateSet)):
        cur_candidate = CandidateSet[i]
        score_cur_candidate = getCombineScoreCandidate(cur_candidate,EtoV_sent,VtoE_sent,weight_dict,sent_index,i,train_mode = True)
        res.append(score_cur_candidate)
    return res

# score_dict = {'mono': {'EN': {'ORGANIZATION': 0.9026413030157396, 'PERSON': 1.185135540950598e-10, 'LOCATION': 2.725428938048629e-16}, 'VN':{'ORGANIZATION': 1.6818753363942106e-13, 'PERSON': 8.534458703643806e-18, 'LOCATION': 2.9818008996581602e-18}}, 'bi': {'ORGANIZATION': 0.9457305502846299, 'PERSON': 0.001265022137887413, 'LOCATION': 0.0530044275774826}}
# weight_dict = config.getWeight()
# print(weight_dict)
# tmp = getDictDot(score_dict,weight_dict)
# print(tmp)