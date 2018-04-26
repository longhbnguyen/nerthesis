from ..utilities import wordLen

def absProb(posE,posV):
    return 1 - abs(posE - posV)

def getDistortionprob(NEPair, enSent, vnSent):
    enNE = NEPair[3]
    vnNE = NEPair[4]
    enPOS = NEPair[0][0]
    vnPOS = NEPair[1][0]
    posE = enPOS / wordLen(enSent)
    posV = vnPOS / wordLen(vnSent)
    result = absProb(posE,posV)
    return result


