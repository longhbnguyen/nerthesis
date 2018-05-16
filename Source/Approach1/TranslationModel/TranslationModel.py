import pandas as pd
# import os.path, sys
# sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from utilities import read_align_file
import csv
inputfile = './TranslationModel/Result.actual.ti.final'
super_small_number = 1e-15

data = pd.read_csv(inputfile, sep = ' ', encoding = 'utf-8',quoting=csv.QUOTE_NONE, error_bad_lines=False)
data = data.fillna('NaN')

# align_list = read_align_file(align_file)

def getWordTranslationProb(vnword, enword):
    result = data[(data.VN == vnword) & (data.EN == enword)].Prob
    tmp = result.values
    if (len(tmp)) == 0:
        return 0
    else:
        return tmp[0]

def getAlignSet(enWord_index,vnNE_index,VtoE_sent):
    '''
     Get set of word in Target NE align with source word
    '''
    res = []
    source = VtoE_sent['Source']
    for index in vnNE_index:
        vnWord = source[index]
        if (enWord_index in vnWord['Index']):
            res.append(vnWord['Word'])
    return res

def normalize(res,n):
    return res**(1/n)

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
    # print(NEPair)
    # print('VtoE ', VtoE_sent)
    res = 1.0
    enNE_index = NEPair[0]
    vnNE_index = NEPair[1]
    enNE = NEPair[3].split()
    vnNE = NEPair[4].split()
    # align_enNE = eliminate_not_align(enNE)
    # cur_align_sent = a lign_list[align_index]
    for i in range(len(enNE)):
        sum = 0.0
        enWord = enNE[i]
        # print('EN Word',enWord)
        correspondvnNE = getAlignSet(enNE_index[i],vnNE_index,VtoE_sent)
        # print('Set: ',correspondvnNE)
        if len(correspondvnNE) == 0:
            sum = super_small_number
        else:
            for vnWord in correspondvnNE:
                sum += getWordTranslationProb(enWord,vnWord)
                # print('En_word',enWord)
                # print('vn_word',vnWord)
                # print('/Prob: ',getWordTranslationProb(enWord,vnWord))
            sum /= len(correspondvnNE)
        res *= (sum)
    if len(enNE) == 0:
        return 0.0
    res = normalize(res,len(enNE))
    return res



def main():
    NEPair =[[11, 12], [15, 16], "LOCATION", "El Nino", "El Nino", "LOCATION"]
    VtoE_sent = read_align_file('../../../Alignment_Split/VtoE_Dev.txt')[0]
    tmp = getNETranslationProb(NEPair,VtoE_sent)
    # print(tmp)

if __name__   == '__main__':
    main()