import numpy as np

lambda_step = 0.1

dev_file_en =''
dev_file_vn = ''

def import_data(file):
    pass

#MAIN
list_en_sent = import_data(dev_file_en)
list_vn_sent = import_data(dev_file_vn)

def train_dev(list_lambda):    
    for i in range(len(list_en_sent)):
        true_label = get_true_label(list_en_sent[i],list_vn_sent[i])
        predict_label = get_predict_label(list_en_sent[i],list_vn_sent[i])

        res_list.append(evaluation(true_label,predict_label))

    res = final_evaluation(res_list)
    return res

def init_lambda(number_of_lambda):
    '''
    Init lambda 
    '''
    return np.zeros(number_of_lambda)

def init_result():
    res = {
        'P': 0,
        'R': 0,
        'F1': 0,
    }
    return res

def better_than(res,best_res):
    return res['F1'] > best_res['F1']

def update_list_lambda(list_lambda,step,number_of_lambda):
    res = list_lambda

    

    return res

#Main
def main():
    list_lambda = init_lambda()
    best_lambda = list_lambda
    best_res = init_result()

    while list_lambda != None:
        cur_res = train_dev(list_lambda)
        if (better_than(cur_res,best_res)):
            best_lambda = list_lambda
            best_res = cur_res
        list_lambda = update_list_lambda(list_lambda,step)


        