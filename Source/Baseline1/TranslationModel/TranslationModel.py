import pandas as pd
from utilities import read_align_file
inputfile = './TranslationModel/Result.actual.ti.final'

data = pd.read_csv(inputfile, sep = ' ', encoding = 'utf-8')
data = data.fillna('NaN')

# align_list = read_align_file(align_file)

def getWordTranslationProb(vnword, enword):
    result = data[(data.VN == vnword) & (data.EN == enword)].Prob
    tmp = result.values
    if (len(tmp)) == 0:
        return 0
    else:
        return tmp[0]

def getNETranslationProb(NEPair,VtoE_sent):
    '''
    NEPair: ([index],[index])

    Align element:
    [
{
     'Source_length':15,
     'Target_length':14,
     'Score':7.84741e-23,
     'Target':[words],
     'Source':
     [
               {
                    'Word':''
                    'Align':[...]
               }
     ]
}
]
    '''
    res = 1.0
    enNE = NEPair[3].split()
    vnNE = NEPair[4].split()
    # cur_align_sent = a lign_list[align_index]
    for enWord in enNE:
        sum = 0
        for vnWord in vnNE:
            print()
            sum += getWordTranslationProb(vnWord,enWord)
        res *= sum
    res = res / (len(enNE)**len(vnWord))
    return res