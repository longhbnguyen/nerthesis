import spacy

en_model = spacy.load('en')
vi_model = spacy.load('viNerFull50')

en_file = '../../../Data/corpora/0_DATA/2_Development/dev_eng'
vi_file = '../../../Data/corpora/0_DATA/2_Development/dev_viet'

en_list = open(en_file,'r',encoding='utf-8').read()
