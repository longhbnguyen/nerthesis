

'''
Return Predict Set for Test Set
Input: Alignment Result of Test Set
Output: [[([en_idx],[vi_idx],'type')],]
'''




    pass

align_file_EtoV = ''
align_file_VtoE = ''

outputfile = ''

align_list_EtoV = read_align_file(align_file_EtoV)
align_file_VtoE = read_align_file(align_file_VtoE)

predict = getPredict.getFinalPredictNEPair(align_list_EtoV,align_list_VtoE)
label = getLabel.getNEPair(en_test_file,vn_test_file)

# EvaluationRes = {'TP':,'TN':,}
EvaluationRes_type_sen = Evaluate.evaluate(predict,label,type_mode)
EvaluationRes_type_insen = Evaluate.evaluate(predict,label,type_mode)
