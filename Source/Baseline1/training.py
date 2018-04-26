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


lambda_step = 0.1
cur_Count = 0
dev_file_EtoV =''
dev_file_VtoE = ''
dev_file_en = ''
dev_file_vn = ''
dev_list_EtoV = read_align_file(dev_file_EtoV)
dev_list_VtoE = read_align_file(dev_file_VtoE)

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
    FinalPredictNEPairList = predict.getFinalPredictNEPairList(dev_list_EtoV,dev_list_VtoE,train_mode = True)
    trueSet = TrueSet.getFileTrueSet(dev_file_en,dev_file_vn)
    res = evaluate.getMetrics(FinalPredictNEPairList,trueSet,0)
    return res

def init_lambda(number_of_lambda):
    '''
    Init lambda 
    '''
    res = config.getWeight()
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
    return res['F1'] > best_res['F1']

def update_list_lambda(list_lambda,step,number_of_lambda):
    ''' 
    Chua code xong
    '''
    global cur_Count
    cur_Count += 1
    tmp = cur_Count
    res = list_lambda
    for key,value in res.items():
        res[key] = (tmp % 10) / 10
        tmp = tmp / 10

    if (cur_Count > number_of_lambda**10):
        return None
    return res

#Main
def main():
    ScoreTable.createScoreTable(dev_list_EtoV,dev_list_VtoE)
    list_lambda = init_lambda()
    best_lambda = list_lambda
    best_res = init_result()

    while list_lambda != None:
        cur_res = train_dev(list_lambda)
        if (better_than(cur_res,best_res)):
            best_lambda = list_lambda
            best_res = cur_res
        list_lambda = update_list_lambda(list_lambda,step)


        