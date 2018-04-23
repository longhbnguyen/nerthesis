import re
import AlignmentModel.align as am


test_en = './corpora/0_DATA/3_TEST/test_eng'
test_vi = './corpora/0_DATA/3_TEST/test_viet'

test_en_list = open(test_en,encoding = 'utf-8').read().split('\n')
test_vi_list = open(test_vi,encoding = 'utf-8').read().split('\n')

true_count = 0
total_predict = 0
total_true = 0


def removeDuplicatePairs(candidate_set, highest_pair):    
    #remove all duplicate pairs
    for idx in highest_pair[0]:
        for i in range(len(candidate_set)):
            if idx in candidate_set[i][0]:
                del candidate_set[i]
    for idx in highest_pair[1]:
        for i in range(len(candidate_set)):
            if idx in candidate_set[i][1]:
                del candidate_set[i]
    return candidate_set

def getPredictSetList(v_file,e_file):
    predict_set_list =[]
    en_list = open(e_file,encoding = 'utf-8').read().split('\n')
    vi_list = open(v_file,encoding = 'utf-8').read().split('\n')
    for i in range(len(en_list)):
        predict_set_list.append(en_list[i],vi_list[i])
    return predict_set_list

def getTrueSetList(v_file,e_file):



def getTrueSet()


def getScore(pair):


def predict(v_sent,e_sent):
    candidate_set = am.getCandidateSet(v_sent,e_sent)

    predict_set  = []
    for pair in candidate_set:
        
    
    return predict_set


def evalSentPair(true_set, predict_set):
    global total_predict
    global total_true
    global true_count
    for i in len(true_set):
        for j in len(predict_set):
            if true_set[i] == predict_set[j]:
                true_count += 1
                del true_set[i]
                del predict_set[j]
                break
    total_predict += len(predict_set)
    total_true += len(true_set)




def evalSentList(true_set_list,predict_set_list):
    for i in range(len(true_set_list)):
        evalSentPair(true_set_list[i],predict_set_list[i])
    
    p = true_count / total_predict
    r = true_count / total_true
    f = 2*p*r/(p+r)

def main():


if __name__ == '__main__':
    getPredictSetList()
    getTrueSetList()