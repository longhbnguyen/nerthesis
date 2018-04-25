
def getTransliterationProb(enNE, vnNE):
    n = len(enNE.split())
    word_count = 0
    enNE = enNE.lower()
    vnNE = vnNE.lower()
    # Count Word 
    for enword in enNE.split():
        for vnword in vnNE.split():
            if (enword == vnword):
                word_count += 1
                break

    return word_count / n
