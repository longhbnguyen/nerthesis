
import CandidateSet
import CombineScore_TypeSens
import CombineScore_InSens
import json
import os.path
ScoreTable_TypeInSens = []
ScoreTable_TypeSens = []

score_table_TypeInSens_file = 'ScoreTable_TypeInSens_Test.json'
score_table_TypeSens_file = 'ScoreTable_TypeSens_Test.json'

def createScoreTable_TypeInSens(dev_list_EtoV,dev_list_VtoE):
    global ScoreTable_TypeInSens
    if os.path.isfile(score_table_TypeInSens_file):
        json_data=open(score_table_TypeInSens_file).read()
        ScoreTable_TypeInSens = json.loads(json_data)
        
    else:
        for i in range(len(dev_list_EtoV)):
            EtoV_sent = dev_list_EtoV[i]
            VtoE_sent = dev_list_VtoE[i]
            candidateSet = CandidateSet.getCandidateSet(EtoV_sent,VtoE_sent,i)
            score = CombineScore_InSens.getScoreDictForSet_TypeInSens(candidateSet,EtoV_sent,VtoE_sent)
            ScoreTable_TypeInSens.append(score)
        with open(score_table_TypeInSens_file,'w',encoding='utf-8') as f:
            json.dump(ScoreTable_TypeInSens,f)

def createScoreTable_TypeSens(dev_list_EtoV,dev_list_VtoE):
    global ScoreTable_TypeSens
    if os.path.isfile(score_table_TypeSens_file):
        json_data=open(score_table_TypeSens_file).read()
        ScoreTable_TypeSens = json.loads(json_data)
        
    else:
        for i in range(len(dev_list_EtoV)):
            EtoV_sent = dev_list_EtoV[i]
            VtoE_sent = dev_list_VtoE[i]
            candidateSet = CandidateSet.getCandidateSet(EtoV_sent,VtoE_sent,i)
            score = CombineScore_TypeSens.getScoreDictForSet_TypeSens(candidateSet,EtoV_sent,VtoE_sent,i)
            ScoreTable_TypeSens.append(score)
        with open(score_table_TypeSens_file,'w',encoding='utf-8') as f:
            json.dump(ScoreTable_TypeSens,f)




def getScoreforOneCandidate_TypeInSens(sent_index,candidate_index):
    # print(sent_index, candidate_index)
    # print(ScoreTable_TypeInSens)
    return ScoreTable_TypeInSens[sent_index][candidate_index]

    
def getScoreforOneCandidate_TypeSens(sent_index,candidate_index):
    return ScoreTable_TypeSens[sent_index][candidate_index]

def getScoreforOneCandidate(sent_index,candidate_index):
    full_score = ScoreTable_TypeInSens[sent_index][candidate_index]
    score = {}
    score['coocurence'] = full_score['coocurence']
    score['translation'] = full_score['translation']
    score['distortion'] = full_score['distortion']
    score['transliteration'] = full_score['transliteration']
    
    return score
