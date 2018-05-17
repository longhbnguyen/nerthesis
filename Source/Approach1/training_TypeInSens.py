'''
Find the best Lambda for all features
input: dev_set, Score 
output: list_of_weight
'''
import numpy as np
from utilities import read_align_file
import predict
import evaluate_TypeInSens
import config
import TrueSet
import ScoreTable
import CandidateSet
import sys
from AlignmentModel import EtoV_model, VtoE_model

lambda_list_to_update = ['translation', ' transliteration', 'coocurence', 'distortion']

lambda_step = 0.1
cur_Count = 0
dev_file_EtoV = config.align_file_EtoV_dev
dev_file_VtoE = config.align_file_VtoE_dev
dev_file_en = config.en_file_dev
dev_file_vn = config.vn_file_dev
dev_list_EtoV = read_align_file(dev_file_EtoV)
dev_list_VtoE = read_align_file(dev_file_VtoE)
config_file = 'config.ini'

trueSet = TrueSet.getFileTrueSet(dev_file_en,dev_file_vn)

#MAIN

def train_dev(list_lambda):    
    """[summary]
    
    Arguments:
        list_lambda {[float]} -- [weight of features]
    output: 
        Final Res of that list of lambda
        res =
        {
            'F1':,
            'P':
            'R':
        }
    """
    #get list
    FinalPredictNEPairList = predict.getFinalPredictNEPairList(dev_list_EtoV,dev_list_VtoE,list_lambda,'dev',train_mode_InSens=True)
    res = evaluate_TypeInSens.getMetrics(FinalPredictNEPairList,trueSet,'dev')
    return res

def init_lambda():
    '''
    Init lambda 
    '''
    res = config.getWeightZero()
    # print(res)
    for key,value in res.items():
        res[key] = 0.0
    return res

def init_result():
    res = {
        'P': 0.0,
        'R': 0.0,
        'F1': 0.0,
    }
    return res

def better_than(res,best_res):
    return (res['F1'] > best_res['F1'])

def update_list_lambda(list_lambda,step):
    ''' 
    '''
    global cur_Count
    cur_Count += 1
    
    print('Cur Count ', cur_Count)
    tmp = cur_Count
    res = list_lambda
    # print(lambda_list_to_update)
    for key,value in res.items():
        if key in lambda_list_to_update:
            res[key] = int(tmp % 10) / 10
            tmp = int(tmp / 10)
    if (cur_Count > (10**len(lambda_list_to_update)) ):
        return None
    # if (cur_Count > 10):
    #     return None
    
    return res

def getBestLambda(lambda_list_to_update_tmp):
    global lambda_list_to_update 
    lambda_list_to_update = lambda_list_to_update_tmp
    VtoE_model.createEntListTable_Spacy('dev')
    EtoV_model.createEntListTable_Spacy('dev')
    EtoV_model.createEntListTable_Stanford('dev')
    VtoE_model.createEntListTable_Stanford('dev')
    # CandidateSet.createCandidateSet(dev_list_EtoV,dev_list_VtoE,'dev')
    ScoreTable.createScoreTable_TypeInSens(dev_list_EtoV,dev_list_VtoE,'dev')
    ScoreTable.createScoreTable_TypeSens(dev_list_EtoV,dev_list_VtoE,'dev')
    list_lambda = init_lambda()
    best_lambda = list_lambda
    best_res = init_result()
    step = 0.1
    while list_lambda != None:
        print('List Lambda ', list_lambda)
        cur_res = train_dev(list_lambda)
        if (better_than(cur_res,best_res)):
            best_lambda = dict((k,v) for k,v in list_lambda.items())
            best_res = cur_res
        list_lambda = update_list_lambda(list_lambda,step)
    print('BestRes ' ,best_res)
    print('BestLambda ', best_lambda)

    return best_lambda
#Main
def main(lambda_list_to_update_tmp):
    # CandidateSet.createCandidateSet(dev_list_EtoV,dev_list_VtoE,'dev')
    ScoreTable.createScoreTable_TypeInSens(dev_list_EtoV,dev_list_VtoE,'dev')
    ScoreTable.createScoreTable_TypeSens(dev_list_EtoV,dev_list_VtoE,'dev')
    list_lambda = init_lambda()
    best_lambda = list_lambda
    best_res = init_result()
    step = 0.1
    while list_lambda != None:
        print('List Lambda ', list_lambda)
        cur_res = train_dev(list_lambda)
        if (better_than(cur_res,best_res)):
            best_lambda = dict((k,v) for k,v in list_lambda.items())
            best_res = cur_res
        list_lambda = update_list_lambda(list_lambda,step)
        
        
    print('BestRes ' ,best_res)
    print('BestLambda ', best_lambda)
    # config.WriteBestLambda_TypeInSens(best_lambda)
    
if __name__ == '__main__':
    lambda_list_to_update_tmp = sys.argv[2:]
    main(lambda_list_to_update_tmp)
