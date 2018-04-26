import utilities
import predict as getPredict
import TrueSet as getLabel
import config
align_file_EtoV = '../../Alignment_Split/EtoV_test.txt'
align_file_VtoE = '../../Alignment_Split/VtoE_test.txt'

outputfile = ''
list_lambda = config.getWeight()
for key,value in list_lambda.items():
    list_lambda[key] = float(list_lambda[key])



align_list_EtoV = utilities.read_align_file(align_file_EtoV)
align_file_VtoE = utilities.read_align_file(align_file_VtoE)

predict = getPredict.getFinalPredictNEPairList(align_list_EtoV, align_list_VtoE,list_lambda,train_mode = False)
label = getLabel.getNEPair(en_test_file,vn_test_file)

# EvaluationRes = {'TP':,'TN':,}
EvaluationRes_type_sen = Evaluate.evaluate(predict,label,type_mode)
EvaluationRes_type_insen = Evaluate.evaluate(predict,label,type_mode)
