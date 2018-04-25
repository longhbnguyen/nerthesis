import configparser


config = configparser.ConfigParser()
config.read('config.ini')

def getWeight():
    weight = config['Weight']
    return weight
