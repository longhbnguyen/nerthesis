from spacy.gold import GoldParse
import spacy
from ast import literal_eval


def evaluate(ner_model, examples):
    scorer = spacy.scorer.Scorer()
    for input_, annot in examples:
        # print(input_)
        # print(annot['entities'])
        doc_gold_text = ner_model.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities = annot['entities'])
        pred_value = ner_model(input_, ent = ['PER','LOC','ORG'])
        scorer.score(pred_value, gold)
    return scorer.scores


def main():
    ner_model = spacy.load('en_core_web_md')
    train_data = []
    # i = 0
    with open('./test_eng_spacy.out','r',encoding = 'utf-8') as f:
        for line in f:
            tp = literal_eval(line)
            # print(tp)
            train_data.append(tp)
            # i += 1
            # if i > 10:
            #     break
    print('Loaded data!')
    print(evaluate(ner_model,train_data))
     

if __name__ == '__main__':
    main()