'''
([],[])
'''
def evaluateSentencePair(predict,label,type_mode,tp):
    '''
    Compare predict set and true set of a sentence pair
    '''
    tp = 0
    predict = sorted(predict, key=lambda tmp: tmp[0][0])
    print('Predict Set ', predict)
    print('True Set ', label)
    for i in range(len(label)):
        true_en_begin = label[i][0][0]
        # print('True_en_begin ',true_en_begin)
        true_en_end = label[i][0][-1]
        # print('True_en_end ',true_en_end)
        sub_predict = []
        for j in range(len(predict)):
            predict_en_begin = predict[j][0][0][0]
            # print('PredictEnBegin ', predict_en_begin)
            if predict_en_begin == true_en_begin:
                sub_predict.append(predict[j])
        # print('SubPredict ',sub_predict)
        if(len(sub_predict)) > 0:
            for pair in sub_predict:
                # print(pair)
                predict_en_end = pair[0][0][-1]
                if predict_en_end == true_en_end:
                    predict_vi_begin = pair[0][1][0]
                    predict_vi_end = pair[0][1][-1]
                    true_vi_begin = label[i][1][0]
                    true_vi_end = label[i][1][-1]
                    if true_vi_begin == predict_vi_begin and true_vi_end == predict_vi_end:
                        tp += 1
    print('TP ', tp)
    return tp

def evaluate(predict_set,true_set,type_mode):
    '''
    Compare the whole predict set and true set
    '''
    tp = 0
    total_predict_pairs = 0
    total_true_pairs = 0
    for i in range(len(predict_set)):
        total_predict_pairs += len(predict_set[i])
        total_true_pairs += len(true_set[i])
    
    for i in range(len(predict_set)):
        tp = tp + evaluateSentencePair(predict_set[i],true_set[i],type_mode,tp)
    
    
    return tp, total_predict_pairs, total_true_pairs

def getMetrics(predict_set,true_set,type_mode):
    '''
    get Metrics Evaluation
    type_mode: 0:Insensitive , 1:Type-Sensitive
    '''
    tp, total_predict_pairs,total_true_pairs = evaluate(predict_set,true_set,type_mode)
    # print('True Set ',true_set)
    # print('Predict Set ', predict_set)
    # print('TP ', tp)
    recall = tp / (total_true_pairs)
    precision = tp / (total_predict_pairs)
    if recall == 0 and precision == 0:
        f1 = 0
    else:
        f1 = 2*recall*precision/(recall+precision)
    res = {}
    res['R'] = recall
    res['P'] = precision
    res['F1'] = f1
    print(res)
    return res
