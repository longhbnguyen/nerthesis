import configparser

config_file = 'config.ini'

config = configparser.ConfigParser()
config.read(config_file)

def getWeight():
    weight = config['Best Weight (Translation+Coocurence+Distortion)']
    res = {}
    for key,value in weight.items():
        # print('Key ',key)
        # print('Value ',value)
        res[key] = float(value)
    # print('Res ',res)
    return res

def WriteBestLambda(best_lambda):
    w = open(config_file,'a',encoding='utf-8')
    w.write('\n[Best Weight (Translation+Coocurence+Distortion)]\n')
    for key,value in best_lambda.items():
        w.write(key)
        w.write('=')
        w.write(str(value))
        w.write('\n')
    w.close()