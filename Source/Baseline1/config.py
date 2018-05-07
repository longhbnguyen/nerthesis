import configparser

config_file = 'config.ini'

config = configparser.ConfigParser()
config.read(config_file)

def getInitWeightTypeSens():
    weight = config['Best Weight TypeInSens']
    res = {}
    for key,value in weight.items():
        res[key] = float(value)
    return res

def getWeight():
    weight = config['Best Weight TypeSens']
    res = {}
    for key,value in weight.items():
        # print('Key ',key)
        # print('Value ',value)
        res[key] = float(value)
    # print('Res ',res)
    return res

def getWeightZero():
    weight = config['Weight Zero']
    res = {}
    for key,value in weight.items():
        # print('Key ',key)
        # print('Value ',value)
        res[key] = float(value)
    # print('Res ',res)
    return res

def WriteBestLambda(best_lambda):
    w = open(config_file,'a',encoding='utf-8')
    w.write('\n[Best Weight]\n')
    for key,value in best_lambda.items():
        w.write(key)
        w.write('=')
        w.write(str(value))
        w.write('\n')
    w.close()

def WriteBestLambda_TypeSens(best_lambda):
    w = open(config_file,'a',encoding='utf-8')
    w.write('\n[Best Weight TypeSens]\n')
    for key,value in best_lambda.items():
        w.write(key)
        w.write('=')
        w.write(str(value))
        w.write('\n')
    w.close()

def WriteBestLambda_TypeInSens(best_lambda):
    w = open(config_file,'a',encoding='utf-8')
    w.write('\n[Best Weight TypeInSens]\n')
    for key,value in best_lambda.items():
        w.write(key)
        w.write('=')
        w.write(str(value))
        w.write('\n')
    w.close()