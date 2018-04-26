
import CandidateSet
import CombineScore
ScoreTable = []

def createScoreTable(dev_list_EtoV,dev_list_VtoE):
    global ScoreTable
    for i in range(len(dev_list_EtoV)):
        EtoV_sent = dev_list_EtoV[i]
        VtoE_sent = dev_list_VtoE[i]
        candidateSet = CandidateSet.getCandidateSet(EtoV_sent,VtoE_sent)
        score = CombineScore.getScore(candidateSet,EtoV_sent,VtoE_sent)
        ScoreTable.append(score)

def getScoreforOneCandidate(sent_index,candidate_index):
    return ScoreTable[sent_index][candidate_index]