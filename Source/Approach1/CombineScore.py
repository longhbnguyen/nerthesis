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
# import MonoReassignModel.MonoFromFile as MonoProb
# import BiReassignModel.ReassignModel as BiProb
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
    for key,value in score_dict.items():
        res = res + (score_dict[key]) * (weight_dict[key])
    return res 

def getScoreDict_TypeInSens(cur_candidate,EtoV_sent,VtoE_sent):
    '''
    '''
    translation_score = TranslationProb.getNETranslationProb(cur_candidate, VtoE_sent)
    transliteration_score = TransliterationProb.getTransliterationProb(cur_candidate,VtoE_sent)
    coocurence_score = CoocurenceProb.getCoocurenceProb(cur_candidate)
    distortion_score = DistortionProb.getDistortionprob(cur_candidate,EtoV_sent,VtoE_sent)
    # mono_score = MonoProb.getMonoProb(cur_candidate,EtoV_sent,VtoE_sent)
    # bi_score = BiProb.getBiProb(cur_candidate)
    score_dict= {}
    score_dict['translation'] = translation_score
    score_dict['transliteration'] = transliteration_score
    score_dict['coocurence'] = coocurence_score
    score_dict['distortion'] = distortion_score
    # score_dict['Mono'] = mono_score
    # score_dict['Bi'] = bi_score
    return score_dict

def getScoreDict_TypeSens(candidate,EtoV_sent,VtoE_sent):

def getScoreDictForSet_TypeInSens(CandidateSet,EtoV_sent,VtoE_sent):
    res = []
    for candidate in CandidateSet:
        res.append(getScoreDict_TypeInSens(candidate,EtoV_sent,VtoE_sent))
    return res

def getScoreDictForSet_TypeSens(candidateSet,EtoV_sent,VtoE_sent):
    res = []
    for candidate in CandidateSet:
        res.append(getScoreDict_TypeSens(candidate,EtoV_sent,VtoE_sent))
    return res

def getCombineScoreCandidate(cur_candidate,EtoV_sent,VtoE_sent,weight_dict,sent_index,candidate_index,train_mode = False):
    '''

    '''
    score = 0.0
    if train_mode:
        score_dict = ScoreTable.getScoreforOneCandidate_TypeInSens(sent_index,candidate_index)
    else:
        score_dict = getScoreDict_TypeInSens(cur_candidate, EtoV_sent, VtoE_sent)
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
