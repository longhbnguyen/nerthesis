import pandas as pd
from util import read_align_file
inputfile = 'Result.actual.ti.final'
align_file = ''

data = pd.read_csv(inputfile, sep = ' ', encoding = 'utf-8')
data = data.fillna('NaN')

align_list = read_align_file(align_file)

def getWordTranslationProb(vnword, enword):
    result = data[(data.VN == vnword) & (data.EN == enword)].Prob
    tmp = result.values
    if (len(tmp)) == 0:
        return 0
    else:
        return tmp[0]

def getNETranslationProb(align_index, NEPair):
    '''
    NEPair: ([index],[index])

    Align element:
    [
{
     'Source_length':15,
     'Target_length':14,
     'Score':7.84741e-23,
     'Source':[words],
     'Target':
     [
               {
                    'Word':''
                    'Align':[...]
               }
     ]
}
]
    '''
    res = 0.0
    enNE = NEPair[0]
    vnNE = NEPair[1]
    cur_align_sent = align_list[align_index]
    for index in enNE:
        cur_en_dict = cur_align_sent['Target'][index]
        cur_word = cur_en_dict['Word']
        vn_align_list = cur_en_dict['Align']
        mau = len(vn_align_list)
        if mau == 0:
            return 0.0
        tsum = 0
        for vn_word in vn_align_list:
            tsum += getWordTranslationProb(vn_word,cur_word) 

        res = res * tsum/mau
    return res