content = ''
ent_list = []
ent_flag = False
cur_type = ''
w = open('test_viet_spacy.out' , 'w', encoding = 'utf-8')
i = 0
with open('test_stanfordner_viet.tsv', 'r', encoding = 'utf-8') as f:
    for line in f:
        if line == '\n':
            #write to file
            w.write('("')
            content = content.replace('"','\\"')
            w.write(content.strip())
            w.write('"')
            w.write(",{ 'entities':[")
            for ent in ent_list:
                w.write('(')
                w.write(str(ent[0]))
                w.write(',')
                w.write(str(ent[1]))
                w.write(',')
                w.write("'")
                w.write(ent[2])
                w.write("'")
                w.write('),')
            w.write(']})\n')
            ent_list = []
            content = ''
            ent_flag = False
            cur_type = ''
            # i = i +1
            # if i == 194:
            #     break
            continue
        text = line.split()[0]
        print(text)
        entity = line.split()[1]
        if entity == 'PERSON':
            entity = 'PER'
        elif entity == 'LOCATION':
            entity = 'LOC'
        elif entity == 'ORGANIZATION':
            entity = 'ORG'
            
        if entity not in ['O','PER', 'ORG', 'LOC']:
            print(line)
        content += text + ' '
        if entity != 'O' and ent_flag == False:
            # print(content)
            start = len(content) - len(text) -1
            # print(start)
            cur_type = entity
            ent_flag = True
        elif entity == cur_type:
            continue
        elif entity == 'O' and cur_type != 'O' and ent_flag == True:
            # print(content)
            # print(len(content))
            # print(len((content).split()))
            end = len(content) - 1 - len(text) - 1
            # print(end)
            ent = (start,end,cur_type)
            ent_list.append(ent)
            ent_flag = False
        