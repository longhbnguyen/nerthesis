
inputfile = 'NER.5000.txt'
outputfile = 'NER_Spacy.out'

def process(line):
    '''process to raw line'''
    res =''
    ents = line.split()
    for ent in ents:
        pos = ent.rfind('/')
        res = res + ent[:pos].replace('_',' ') + ' '
    # process ""
    res = res.replace('"','\"')
    return res

def getType(ent):
    # print('==============')
    # print('GetType: ',ent)
    '''return type of the entity BIO'''
    # tmp = ent.split('/')
    pos = ent.rfind('/')
    # print('Pos:', pos)
    tmp = []
    # print('len: ',len(ent))
    tmp.append(ent[:pos])
    tmp.append(ent[pos+1:])
    # print('tmp: ',tmp)
    pos = tmp[1].rfind('_')
    if pos == -1:
        return tmp[1]
    tmp2 = []
    tmp2.append(tmp[1][:pos])
    tmp2.append(tmp[1][pos+1:])
    if len(tmp2) < 2:
        return ''
    # print('Type pos: ',pos)
    # print('tmp2: ',tmp2)
  
    return tmp2[1]

def getlen(ent):
    ''' return len of that ent'''
    pos = ent.rfind('/')
    # print('Getlen: ',ent)
    # print('len:',pos)
    return pos

def getEnt(ent):
    ''' return entity label PER LOC'''
    pos = ent.rfind('/')
    # print('Pos:', pos)
    tmp = []
    # print('len: ',len(ent))
    tmp.append(ent[:pos])
    tmp.append(ent[pos+1:])
    pos = tmp[1].rfind('_')
    # print('------')
    # print('Ent: ',ent)
    # print('GetEnt tmp: ',tmp)
    if (pos == -1):
        return ''
    tmp2 = []
    tmp2.append(tmp[1][:pos])
    tmp2.append(tmp[1][pos+1:])
    # print('GetEnt tmp2: ',tmp2)
    if len(tmp) < 2: return ''
    return tmp2[0]

def getEntString(ent):
    pos = ent.rfind('/')
    return ent[:pos]

def listents(ents,line):
    org_line = process(line)
    org_line = org_line.replace(' ','_')    
    res = ''
    ''' return string of list ent '''
    cur_ent = ''
    start = 0
    end = 0
    i = 0
    start_ent = 0
    n = len(ents)
    while (i < n):
        # when begin entity
        cur_type = getType(ents[i])
        if (cur_type == 'B'):
            #begin new Entity
            # start = end
            cur_ent = getEntString(ents[i])
            # end = end + getlen(ents[i])
            while(True):
                i += 1
                cur_type = getType(ents[i])
                if (cur_type == 'I'):
                    # end = end + getlen(ents[i]) + 1
                    cur_ent = cur_ent + '_' + getEntString(ents[i])
                else:
                    # end = end + getlen(ents[i-1]) + 1
                    break
            
            #end entity
            start_ent = org_line.find(cur_ent,start_ent)
            res = res + '(' + str(start_ent) + ',' +str(start_ent + len(cur_ent)) + ', \'' + getEnt(ents[i-1]) + '\')' + ','
        else: 
            #Begin O
            # end = end + getlen(ents[i])
            i += 1
            
    # res = res + '(' + str(start) + ',' + str(end) + ',' + getEnt(ents[i]) + ')' + ','

    return res

def convertspacy(line):
    result = '('
    ents = line.split()
    org_line = process(line)
    # print('ORG: ',org_line)
    result = result + '"' + org_line + '"' + ','+ '{ \'entities\':' + '[' + listents(ents,line) + ']' + '})'
    return result

k = 0
fout = open(outputfile,'w',encoding='utf-8')
with open(inputfile,'r',encoding='utf-8') as fin:
    for line in fin:
        outputline = convertspacy(line)
        # print(outputline)
        # k = k + 1
        # if (k > 3):
        #     break
        fout.write(outputline)
        fout.write('\n')
fout.close()
