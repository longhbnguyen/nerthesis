
input = 'viet.PER'
output = 'v_prob.PER'

w= open(output,'w',encoding= "utf-8")

i = 0
with open(input,'r',encoding = "utf-8") as f:
    for line in f:
        for tok in line.split():
            print(tok)
            w.write(tok)
            w.write('\t')
            w.write('O')
            w.write('\n')
        w.write('\n')

w.close()
