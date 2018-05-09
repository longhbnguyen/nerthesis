import configparser

config_file = 'config.ini'

config = configparser.ConfigParser()
config.read(config_file)


'''Path'''
#Algin file
#EtoV
align_file_EtoV_dev = '../../../Alignment_Split/EtoV_Dev.txt'
align_file_EtoV_test = '../../../Alignment_Split/EtoV_Test.txt'
#VtoE
align_file_VtoE_dev = '../../../Alignment_Split/VtoE_Dev.txt'
align_file_VtoE_test = '../../../Alignment_Split/VtoE_Test.txt'

#Data File
#Dev
en_file_dev = '../../../Data/corpora/0_DATA/2_Development/dev_eng'
vn_file_dev = '../../../Data/corpora/0_DATA/2_Development/dev_viet'
#Test
en_file_test = '../../../Data/corpora/0_DATA/3_Test/test_eng'
vn_file_test = '../../../Data/corpora/0_DATA/3_Test/test_viet'

#NER
en_model_stanford = '../../../stanford-ner-2018-02-27/english.all.3class.distsim.crf.ser.gz'
vn_model_stanford = '../../../stanford-ner-2018-02-27/vietnamese_new.gz'
path_to_jar = '../../../stanford-ner-2018-02-27/stanford-ner-3.9.1.jar'
vn_model_spacy = './InitialNER/viNerFull50'
#NER result file
initial_viet_ent_list_file_stanford_dev = './AlignmentModel/ner_viet_dev.tsv'
initial_viet_ent_list_file_spacy_dev = './AlignmentModel/vi_ent_list_spacy_dev.txt'
initial_viet_ent_list_file_stanford_test = './AlignmentModel/ner_viet_test.tsv'
initial_viet_ent_list_file_spacy_test = './AlignmentModel/vi_ent_list_spacy_test.txt'

initial_en_ent_list_file_stanford_dev = './AlignmentModel/ner_eng_dev.tsv'
initial_en_ent_list_file_spacy_dev = './AlignmentModel/en_ent_list_spacy_dev.txt'
initial_en_ent_list_file_stanford_test = './AlignmentModel/ner_eng_test.tsv'
initial_en_ent_list_file_spacy_test = './AlignmentModel/en_ent_list_spacy_test.txt'

#Alignment probability table 
alignment_table_file = './AlignmentModel/Result.actual.ti.final'

#Candidate Set
candidate_set_test_file = 'Candidate_Set_Test.json'
candidate_set_dev_file = 'Candidate_Set_Dev.json'

#Score Table
score_table_TypeInSens_file_test = 'ScoreTable_TypeInSens_Test.json'
score_table_TypeSens_file_test = 'ScoreTable_TypeSens_Test.json'
score_table_TypeInSens_file_dev = 'ScoreTable_TypeInSens_Dev.json'
score_table_TypeSens_file_dev = 'ScoreTable_TypeSens_Dev.json'





def getInitWeightTypeSens():
    weight = config['Best Weight TypeInSens']
    res = {}
    for key,value in weight.items():
        res[key] = float(value)
    return res

def getWeight():
    weight = config['Best Weight TypeSens']
    res = {}
    for key,value in weight.items():
        # print('Key ',key)
        # print('Value ',value)
        res[key] = float(value)
    # print('Res ',res)
    return res

def getWeightZero():
    weight = config['Weight Zero']
    res = {}
    for key,value in weight.items():
        # print('Key ',key)
        # print('Value ',value)
        res[key] = float(value)
    # print('Res ',res)
    return res

def WriteBestLambda(best_lambda):
    w = open(config_file,'a',encoding='utf-8')
    w.write('\n[Best Weight]\n')
    for key,value in best_lambda.items():
        w.write(key)
        w.write('=')
        w.write(str(value))
        w.write('\n')
    w.close()

def WriteBestLambda_TypeSens(best_lambda):
    w = open(config_file,'a',encoding='utf-8')
    w.write('\n[Best Weight TypeSens]\n')
    for key,value in best_lambda.items():
        w.write(key)
        w.write('=')
        w.write(str(value))
        w.write('\n')
    w.close()

def WriteBestLambda_TypeInSens(best_lambda):
    w = open(config_file,'a',encoding='utf-8')
    w.write('\n[Best Weight TypeInSens]\n')
    for key,value in best_lambda.items():
        w.write(key)
        w.write('=')
        w.write(str(value))
        w.write('\n')
    w.close()