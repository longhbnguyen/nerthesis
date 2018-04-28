test_file = 'test_eng'


w = open('test_stanfordner_eng.txt', 'w', encoding = 'utf-8')

with open(test_file,'r',encoding = 'utf-8') as f:
    for line in f:
        list_word = line.split()
        ent_flag = False
        cur_ent = ''
        for token in list_word:
            if '<' in token and '</' not in token:
                entity = token[token.find('<')+1:token.find('>')-2]
                ent_flag = True
                cur_ent = entity
                word = token[token.find('>')+1:]
            elif '</' in token:
                if token.find('/') - 1 == token.find('<'):
                    entity = token[token.find('/')+1:token.find('>')-2]
                    word = token[:token.find('<')]
                else:
                    entity = token[token.find('<')+1:token.find('>')-2]
                    word = token[token.find('>')+1:token.find('/')-1]
                ent_flag = False    
            else:
                if ent_flag == True:
                    entity = cur_ent
                else:        
                    entity = 'O'
                word = token

            w.write(word)
            w.write('\t')
            w.write(entity)
            w.write('\n')
        w.write('\n')
