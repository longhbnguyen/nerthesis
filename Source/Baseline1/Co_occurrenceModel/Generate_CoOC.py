

En_file_path = ''
Vn_file_path = ''

En_file = open(En_file_path,mode = 'r',encoding='utf-8').read().split('\n')
Vn_file = open(Vn_file_path,mode = 'r',encoding='utf-8').read().split('\n')

for i in enumerate(En_file):
    