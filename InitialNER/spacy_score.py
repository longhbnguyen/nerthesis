import spacy
import sys
from collections import defaultdict

nlp = spacy.load('viNerFull50')
text = u'Theo ông John Rockhold thì thị trường Việt Nam ẩn chứa nhiều thách thức .'
doc = nlp(text)

print('--- Tokens ---')
for tok in doc:
    print(tok.i, tok)  
print('')

print('--- Entities (detected with standard NER) ---')
for ent in doc.ents:
    print('%d to %d: %s (%s)' % (ent.start, ent.end - 1, ent.label_, ent.text))
print('')

# notice these 2 lines - if they're not here, standard NER
# will be used and all scores will be 1.0
with nlp.disable_pipes('ner'):
    doc = nlp(text)

(beams, somethingelse) = nlp.entity.beam_parse([ doc ], beam_width = 16, beam_density = 0.0001)

entity_scores = defaultdict(float)
for beam in beams:
    for score, ents in nlp.entity.moves.get_beam_parses(beam):
        for start, end, label in ents:
            # print(ents)
            entity_scores[(start, end, label)] += score

# print(entity_scores)
print('--- Entities and scores (detected with beam search) ---')
for key in entity_scores:
    start, end, label = key
    if end == -1:   end = len(doc)-1
    print('%d to %d: %s (%f)' % (start, end - 1, label, entity_scores[key]))
