import importlib
from nltk.tag.stanford import StanfordNERTagger
import spacy
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd

spacy_vi = spacy.load('../InitialNER/viNerFull50')
spacy_en = spacy.load('en')

v_pairs = []
e_pairs = []

path_to_eng_model = '../stanford-ner-2018-02-27/english.all.3class.distsim.crf.ser.gz'
path_to_vie_model = '../stanford-ner-2018-02-27/vietnamese_new.gz'
path_to_jar = '../stanford-ner-2018-02-27/stanford-ner-3.9.1.jar'
tmp_file = './tmp.txt'

stanford_e = StanfordNERTagger(path_to_eng_model, path_to_jar)
stanford_v = StanfordNERTagger(path_to_vie_model, path_to_jar)

org_scores = None
per_scores = None
loc_scores = None

def writeToFile(tmp_file,v_sent):
    w = open(tmp_file,'w',encoding='utf-8')
    for tok in v_sent.split():
        w.write(tok)
        w.write('\t')
        w.write('O')
        w.write('\n')
    w.close()
    

def getProb_Spacy(idx):

    return 0

def getProb_Stanford(idx):
    org = float(org_scores[idx][org_scores[idx].find('=')+1:])
    per = float(per_scores[idx][per_scores[idx].find('=')+1:])
    loc = float(loc_scores[idx][loc_scores[idx].find('=')+1:])
    
    return org,per,loc

def getScore_Stanford(ent):
    per_score = 1.0
    org_score = 1.0
    loc_score = 1.0
    for idx in ent:
        idx = idx - 1
        org_score *= getProb_Stanford(idx)[0]
        per_score *= getProb_Stanford(idx)[1]
        loc_score *= getProb_Stanford(idx)[2]
    
    # n = 1 / len(ent[0])
    # org_score = pow(org_score,n)
    
    # per_score = pow(per_score,n)
    # loc_score = pow(loc_score,n)
    return {'ORGANIZATION':org_score, 'PERSON':per_score, 'LOCATION':loc_score}


def tag_sent(sent, model):
    global org_scores
    global loc_scores
    global per_scores
    writeToFile(tmp_file,v_sent)
    stanfordner_command = 'java -cp ' + path_to_jar +  ' edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ' + model + ' -testFile tmp.txt -printProbs > tmp.tsv'
    os.system(stanfordner_command)
    df = pd.read_csv('tmp.tsv',sep = '\t',encoding='utf-8',header = None, names=['Word','O','ORGANIZATION','PERSON','LOCATION','X'])
    words = list(df.Word.astype(str))
    org_scores = list(df.ORGANIZATION.astype(str))
    per_scores = list(df.PERSON.astype(str))
    loc_scores = list(df.LOCATION.astype(str))


def main():
    
if __name__ == '__main__' :
    main()