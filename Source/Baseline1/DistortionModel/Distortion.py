from ...utilities import wordLen

def absProb(posE,posV):
    return 1 - abs(posE - posV)

def getDistortionProb(enNE,vnNE,enSent, vnSent, enPOS,vnPOS):
    posE = enPOS / wordLen(enSent)
    posV = vnPOS / wordLen(vnSent)
    result = absProb(posE,posV)
    return result


