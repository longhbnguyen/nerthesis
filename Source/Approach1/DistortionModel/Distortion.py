from utilities import wordLen

def absProb(posE,posV):
    return 1 - abs(posE - posV)

def getDistortionprob(NEPair, enSent, vnSent):
    # print('NEPair ',NEPair)
    enNE = NEPair[3]
    vnNE = NEPair[4]
    if len(NEPair[0]) < 1 or len(NEPair[1]) < 1:
        return 0.0
    enPOS = NEPair[0][0]
    vnPOS = NEPair[1][0]
    
    if len(enSent['Target'])==0 or len(vnSent['Target']) == 0:
        return 0.0
    posE = enPOS / len(enSent['Target'])
    posV = vnPOS / len(vnSent['Target'])
    result = absProb(posE,posV)
    return result


