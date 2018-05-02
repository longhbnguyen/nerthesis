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
    res = 0.0
    print(score_dict)
    for key,value in score_dict.items():
        res = res + (score_dict[key]) * (weight_dict[key])
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

