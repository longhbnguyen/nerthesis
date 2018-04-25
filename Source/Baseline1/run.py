

'''
Return Predict Set for Test Set
Input: Alignment Result of Test Set
Output: [[([en_idx],[vi_idx],'type')],]
'''

def read_align_file(align_file):
    '''
    transform align file of Giza++ to align list
    Output:
    [
        {
            'Source_len':
            'Target_len':
            'Score':
            'Source': [words]
            'Target':
            [
                'Word':
                'Index':[]
            ]
        }
    ]
    '''
    pass

def evaluate(predict,label,type_mode):
    pass

align_file_EtoV = ''
align_file_VtoE = ''

outputfile = ''

align_list_EtoV = read_align_file(align_file_EtoV)
align_file_VtoE = read_align_file(align_file_VtoE)

predict = getPredict.getFinalPredictNEPair(align_list_EtoV,align_list_VtoE)
label = getLabel.getNEPair(en_test_file,vn_test_file)

# EvaluationRes = {'TP':,'TN':,}
EvaluationRes_type_sen = evaluate(predict,label,type_mode)
EvaluationRes_type_insen = evaluate(predict,label,type_mode)
