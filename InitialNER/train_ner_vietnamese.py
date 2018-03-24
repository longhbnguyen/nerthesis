#!/usr/bin/env python
# coding: utf8
"""Example of training an additional entity type

This script shows how to add a new entity type to an existing pre-trained NER
model. To keep the example short and simple, only four sentences are provided
as examples. In practice, you'll need many more — a few hundred would be a
good start. You will also likely need to mix in examples of other entity
types, which might be obtained by running the entity recognizer over unlabelled
sentences, and adding their annotations to the training set.

The actual training is performed by looping over the examples, and calling
`nlp.entity.update()`. The `update()` method steps through the words of the
input. At each word, it makes a prediction. It then consults the annotations
provided on the GoldParse instance, to see whether it was right. If it was
wrong, it adjusts its weights so that the correct action will score higher
next time.

After training your model, you can save it to a directory. We recommend
wrapping models as Python packages, for ease of deployment.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from tqdm import tqdm
from ast import literal_eval



# new entity label
label_list = ['TTL', 'BRN', 'ABB_LOC', 'ABB_TRM', 'PER', 'ORG', 'ABB_ORG', 'ABB_TTL', 'MEA', 'ABB_PER', 'ABB_DES', 'LOC', 'TRM', 'NUM', 'DES', 'ABB', 'DTM', 'ABB_BRN']


# training data
# Note: If you're using an existing model, make sure to mix in examples of
# other entity types that spaCy correctly recognized before. Otherwise, your
# model might learn the new type, but "forget" what it previously knew.
# https://explosion.ai/blog/pseudo-rehearsal-catastrophic-forgetting

# TRAIN_DATA = [
#     ("Trường đại học KHTN ở Việt Nam", {
#         'entities': [(22, 30 , 'LOC')]
#     }),

#     ("Trường đại học KHTN ở Anh", {
#         'entities': [(22,25, 'LOC')]
#     }),

#     ("Obama là tổng thống Mỹ", {
#         'entities': [(20, 22, 'LOC')]
#     }),

#     ("Việt Nam là quê hương tôi", {
#         'entities': [(0, 8, 'LOC')]
#     }),

#     ("Việt nam là một nước nằm ở châu Á", {
#         'entities': [(0, 8, 'LOC')]
#     }),

#     ("Việt Nam?", {
#         'entities': [(0, 8, 'LOC')]
#     })
# ]


@plac.annotations(
    model=("Model name. Defaults to blank 'vi' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model=None, new_model_name='animal', output_dir=None, n_iter=20):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('vi')  # create blank Language class
        print("Created blank 'vi' model")
    print('Loading data...')
    train_data = []
    with open('/NER_Spacy.out','r',encoding = 'utf-8') as f:
        for line in f:
            tp = literal_eval(line)
            # print(tp)
            train_data.append(tp)
    print('Loaded data!')
    
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe('ner')
    for label in label_list:
        ner.add_label(label)   # add new entity label to entity recognizer

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            for text, annotations in tqdm(train_data):
                nlp.update([text], [annotations], sgd=optimizer, drop=0.35,losses=losses)
            print(losses)

    # test the trained model
    test_text = 'Tôi sống ở Việt Nam'
    doc = nlp(test_text)
    print("Entities in '%s'" % test_text)
    for ent in doc.ents:
        print(ent.label_, ent.text)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta['name'] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        doc2 = nlp2(test_text)
        for ent in doc2.ents:
            print(ent.label_, ent.text)


if __name__ == '__main__':
    plac.call(main)