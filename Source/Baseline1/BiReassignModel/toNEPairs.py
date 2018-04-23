dev_file_eng = './dev_eng'
dev_file_viet = './dev_viet'



get 


e_sents = open(dev_file_eng, encoding= 'utf-8').read().split('\n')
v_sents = open(dev_file_viet, encoding= 'utf-8').read().split('\n')
for i in range(len(e_sents)):
    e_tokens = e_sents[i].spit()
    v_tokens = v_sents[i].split()
    ent_list = []
    for tok in e_tokens:
        if '<' in tok:
            if '</' 
