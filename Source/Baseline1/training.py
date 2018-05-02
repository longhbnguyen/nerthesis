'''
Find the best Lambda for all features
input: dev_set, Score 
output: list_of_weight
'''
import numpy as np
from utilities import read_align_file
import predict
import evaluate
import config
import TrueSet
import ScoreTable
import CandidateSet


lambda_step = 0.1
cur_Count = 0
dev_file_EtoV = '../../Alignment_Split/EtoV_Dev.txt'
dev_file_VtoE = '../../Alignment_Split/VtoE_Dev.txt'
dev_file_en = '../../Data/corpora/0_DATA/2_Development/dev_eng'
dev_file_vn = '../../Data/corpora/0_DATA/2_Development/dev_viet'
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
    FinalPredictNEPairList = predict.getFinalPredictNEPairList(dev_list_EtoV,dev_list_VtoE,list_lambda,train_mode = True)
    res = evaluate.getMetrics(FinalPredictNEPairList,trueSet,0)
    return res

def init_lambda(number_of_lambda):
    '''
    Init lambda 
    '''
    res = config.getWeight()
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

def update_list_lambda(list_lambda,step,number_of_lambda):
    ''' 
    '''
    global cur_Count
    cur_Count += 1
    
    print('Cur Count ', cur_Count)
    tmp = cur_Count
    res = list_lambda
    for key,value in res.items():
        res[key] = int(tmp % 10) / 10
        tmp = int(tmp / 10)
    if (cur_Count > (10**number_of_lambda) ):
        return None
    # if (cur_Count > 10):
    #     return None
    
    return res

#Main
def main():
    ScoreTable.createScoreTable_TypeInSens(dev_list_EtoV,dev_list_VtoE)
    CandidateSet.createCandidateSetForTraining(dev_list_EtoV,dev_list_VtoE)
    list_lambda = init_lambda(4)
    best_lambda = list_lambda
    best_res = init_result()
    step = 0.1
    while list_lambda != None:
        print('List Lambda ', list_lambda)
        cur_res = train_dev(list_lambda)
        if (better_than(cur_res,best_res)):
            best_lambda = dict((k,v) for k,v in list_lambda.items())
            best_res = cur_res
        list_lambda = update_list_lambda(list_lambda,step,4)
        
        
    print('BestRes ' ,best_res)
    print('BestLambda ', best_lambda)
    config.WriteBestLambda(best_lambda)
    
if __name__ == '__main__':
    main()