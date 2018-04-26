import configparser


config = configparser.ConfigParser()
config.read('config.ini')

def getWeight():
    weight = config['Weight']
    res = {}
    for key,value in weight.items():
        # print('Key ',key)
        # print('Value ',value)
        res[key] = value
    # print('Res ',res)
    return res
