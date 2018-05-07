'''
([],[])
'''
def evaluateSentencePair(predict,true_set,type_mode):
    '''
    Compare predict set and true set of a sentence pair
    '''
    
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
        tp = tp + evaluateSentencePair(predict_set[i],true_set[i],type_mode)
    
    
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
