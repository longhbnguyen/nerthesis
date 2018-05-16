from utilities import read_align_file
import predict as getPredict
import TrueSet as TrueSet
import ScoreTable
import CandidateSet
import config
import evaluate_TypeInSens
import evaluate_TypeSens
import training_TypeInSens
import training_TypeSens
import sys

align_file_EtoV = config.align_file_EtoV_test
align_file_VtoE = config.align_file_VtoE_test
test_file_en = config.en_file_test
test_file_vn = config.vn_file_test

config_file = 'config.ini'



outputfile = ''
list_lambda = config.getWeight()
# for key,value in list_lambda.items():
#     list_lambda[key] = float(list_lambda[key])

# for key,value in list_lambda.items():    
#     print(list_lambda[key])
#     print(type(list_lambda[key]))


test_list_EtoV = read_align_file(align_file_EtoV)
test_list_VtoE = read_align_file(align_file_VtoE)


def main(lambda_list_to_update):
    print(lambda_list_to_update)
    # list_lambda = training_TypeInSens.getBestLambda(lambda_list_to_update)

    CandidateSet.createCandidateSet(test_list_EtoV,test_list_VtoE,'test')
    print("Create Candidate Set")
    ScoreTable.createScoreTable_TypeInSens(test_list_EtoV,test_list_VtoE,'test')
    ScoreTable.createScoreTable_TypeSens(test_list_EtoV,test_list_VtoE,'test')
    print("Created Score Table")
    print(list_lambda)
    predict_set = getPredict.getFinalPredictNEPairList(test_list_EtoV, test_list_VtoE,list_lambda,'test',train_mode_InSens = True, train_mode_Sens=True)
    true_set = TrueSet.getFileTrueSet(test_file_en,test_file_vn)
    # print(predict_set[0])
    # print(true_set[0])
    # EvaluationRes = {'TP':,'TN':,}
    # for i in range(len(predict_set)):
    #     print('=============')
    #     print('Predict', i , len(predict_set[i]))
    #     print(predict_set[i])
    EvaluationRes_type_insen = evaluate_TypeInSens.getMetrics(predict_set,true_set)
    EvaluationRes_type_sen = evaluate_TypeSens.getMetrics(predict_set,true_set)
    print('Type-insensitive ', EvaluationRes_type_insen)
    print('Type-sensitive ', EvaluationRes_type_sen)

if __name__ == '__main__':
    lambda_list_to_update = sys.argv[1:]
    main(lambda_list_to_update)

