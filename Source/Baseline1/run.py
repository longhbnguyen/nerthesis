from utilities import read_align_file
import predict as getPredict
import TrueSet as TrueSet
import ScoreTable
import CandidateSet
import config
import evaluate


align_file_EtoV = '../../Alignment_Split/EtoV_test.txt'
align_file_VtoE = '../../Alignment_Split/VtoE_test.txt'
test_file_en = '../../Data/corpora/0_DATA/3_Test/test_eng'
test_file_vn = '../../Data/corpora/0_DATA/3_Test/test_viet'

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


def main():
    ScoreTable.createScoreTable(test_list_EtoV,test_list_VtoE)
    print("Created Score Table")
    CandidateSet.createCandidateSetForTraining(test_list_EtoV,test_list_VtoE)
    print("Create Candidate Set")
    print(list_lambda)
    predict_set = getPredict.getFinalPredictNEPairList(test_list_EtoV, test_list_VtoE,list_lambda,train_mode = True)
    true_set = TrueSet.getFileTrueSet(test_file_en,test_file_vn)

    # EvaluationRes = {'TP':,'TN':,}

    EvaluationRes_type_insen = evaluate.getMetrics(predict_set,true_set,0)
    EvaluationRes_type_sen = evaluate.getMetrics(predict_set,true_set,1)

    print('Type-insensitive ', EvaluationRes_type_insen)
    print('Type-sensitive ', EvaluationRes_type_sen)

if __name__ == '__main__':
    main()