'''

'''
import numpy as np
import config
import ScoreTable

def getWeightDict():
    '''
    '''
    weight_dict = config.getWeightDict()
    return weight_dict

def getDictDot(score_dict,weight_dict):
    '''
    '''
    res = 0.0
    for key,value in score_dict.items():
        res = res + score_dict[key]*weight_dict[key]
    return res 

def getScoreDict(cur_candidate,EtoV_sent,VtoE_sent):
    '''
    '''
    translation_score = TranslationProb.getTranslationProb(cur_candidate, VtoE_sent)
    transliteration_score = TransliterationProb.getTransliterationProb(cur_candidate,VtoE_sent)
    coocurence_score = CoocurenceProb.getCoocurenceProb(cur_candidate)
    distortion_score = DistortionProb.getDistortionprob(cur_candidate,EtoV_sent,VtoE_sent)
    mono_score = MonoProb.getMonoProb(cur_candidate,EtoV_sent,VtoE_sent)
    bi_score = BiProb.getBiProb(cur_candidate)
    score_dict= {}
    score_dict['Translation'] = translation_score
    score_dict['Transliteration'] = transliteration_score
    score_dict['Coocurence'] = coocurence_score
    score_dict['Distortion'] = distortion_score
    score_dict['Mono'] = mono_score
    score_dict['Bi'] = bi_score
    return score_dict

def getScoreDictForSet(CandidateSet,EtoV_sent,VtoE_sent):
    res = []
    for candidate in CandidateSet:
        res.append(getScoreDict(candidate,EtoV_sent,VtoE_sent))
    return res

def getCombineScoreCandidate(cur_candidate,EtoV_sent,VtoE_sent, train_mode = False,weight_dict,sent_index,candidate_index):
    '''

    '''
    score = 0.0
    if train_mode:
        score_dict = ScoreTable.getScoreforOneCandidate(sent_index,candidate_index)
    else:
        score_dict = getScoreDict(cur_candidate, EtoV_sent, VtoE_sent)
    score = getDictDot(score_dict,weight_dict)
    return score

def getCombineScore(CandidateSet,EtoV_sent,VtoE_sent,train_mode = False,list_lambda,sent_index):
    '''
    '''
    if train_mode:
        weight_dict = list_lambda
    else: 
        weight_dict = getWeightDict()
    res = []
    for i in range(len(CandidateSet)):
        cur_candidate = CandidateSet[i]
        score_cur_candidate = getCombineScoreCandidate(cur_candidate,EtoV_sent,VtoE_sent,weight_dict,sent_index,i)
        res.append(score_cur_candidate)
    return res