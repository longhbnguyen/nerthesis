import importlib
from nltk.tag.stanford import StanfordNERTagger
import spacy
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import AlignmentModel.EtoV_model as alignmentmodel

spacy_vi = spacy.load('../InitialNER/viNerFull50')
spacy_en = spacy.load('en')

v_pairs = []
e_pairs = []

path_to_eng_model = '../InitialNER/stanford-ner-2018-02-27/english.all.3class.distsim.crf.ser.gz'
path_to_vie_model = '../InitialNER/stanford-ner-2018-02-27/vietnamese_new.gz'
path_to_jar = '../InitialNER/stanford-ner-2018-02-27/stanford-ner-3.9.1.jar'
tmp_file = './tmp.txt'

stanford_e = StanfordNERTagger(path_to_eng_model, path_to_jar)
stanford_v = StanfordNERTagger(path_to_vie_model, path_to_jar)

def writeToFile(tmp_file,v_sent):
    w = open('tmp.txt','w',encoding='utf-8')
    for tok in v_sent.split():
        w.write(tok)
        w.write('\t')
        w.write('O')
        w.write('\n')
    w.close()
    

def getProb_Spacy(idx):

    return 0

def getProb_Stanford(idx, org_scores, per_scores, loc_scores):
    org = float(org_scores[idx][org_scores[idx].find('=')+1:])
    per = float(per_scores[idx][per_scores[idx].find('=')+1:])
    loc = float(loc_scores[idx][loc_scores[idx].find('=')+1:])
    
    return org,per,loc

def getScore_Stanford(ent, org_scores, per_scores, loc_scores):
    per_score = 1.0
    org_score = 1.0
    loc_score = 1.0
    for idx in ent[0]:
        idx = idx - 1
        org_score *= getProb_Stanford(idx, org_scores, per_scores, loc_scores)[0]
        per_score *= getProb_Stanford(idx, org_scores, per_scores, loc_scores)[1]
        loc_score *= getProb_Stanford(idx, org_scores, per_scores, loc_scores)[2]
    
    n = 1 / len(ent[0])
    org_score = pow(org_score,n)
    
    per_score = pow(per_score,n)
    loc_score = pow(loc_score,n)
    return org_score, per_score, loc_score



def main():
    v_sent = 'Theo ông John Rockhold thì thị trường Việt Nam ẩn chứa nhiều thách thức .'
    e_sent = 'NULL ({ }) The ({ }) Vietnamese ({ 8 9 }) market ({ 6 7 }) has ({ }) several ({ 12 }) challenges ({ 13 14 }) according ({ }) to ({ }) HCMC ({ 10 11 }) director ({ }) John ({ 3 }) Rockhold ({ 1 2 4 5 }) . ({ 15 })'
    v_ent_list = alignmentmodel.getVietEntSet(v_sent,e_sent)
    # print(v_ent_list)
    v_tokens = v_sent.split()

    writeToFile(tmp_file,v_sent)
    stanfordner_command = 'java -cp ' + path_to_jar +  ' edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ' + path_to_vie_model + ' -testFile tmp.txt -printProbs > tmp.tsv'
    os.system(stanfordner_command)
    df = pd.read_csv('tmp.tsv',sep = '\t',encoding='utf-8',header = None, names=['Word','O','ORGANIZATION','PERSON','LOCATION','X'])
    words = list(df.Word.astype(str))
    org_scores = list(df.ORGANIZATION.astype(str))
    per_scores = list(df.PERSON.astype(str))
    loc_scores = list(df.LOCATION.astype(str))
    for ent in v_ent_list:
        print(ent)
        tok = ''
        for idx in ent[0]:
            tok += v_tokens[idx-1] + ' '
        tok = tok.strip()
        print(tok) 
        print(getScore_Stanford(ent,org_scores,per_scores,loc_scores))


if __name__ == '__main__':
    main()