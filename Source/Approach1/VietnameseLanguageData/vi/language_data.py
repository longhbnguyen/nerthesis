# encoding: utf8
from __future__ import unicode_literals


# import base language data
#from ...import util as base


# import util functions
from ...util import update_exc, strings_to_exc


# import language-specific data from files
from .tag_map import TAG_MAP
from .stop_words import STOP_WORDS
from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS, ORTH_ONLY
from .lemmatizer import RULES as LEMMA_RULES
from .lemmatizer import INDEX as LEMMA_INDEX
from .lemmatizer import EXC as LEMMA_EXC



TOKENIZER_EXCEPTIONS = dict(TOKENIZER_EXCEPTIONS)
TAG_MAP = dict(TAG_MAP)
STOP_WORDS = set(STOP_WORDS)


# customize tokenizer exceptions
update_exc(TOKENIZER_EXCEPTIONS, strings_to_exc(ORTH_ONLY))
update_exc(TOKENIZER_EXCEPTIONS, strings_to_exc(base.EMOTICONS))


# export
__all__ = ["TOKENIZER_EXCEPTIONS", "TAG_MAP", "STOP_WORDS", "LEMMA_RULES", "LEMMA_INDEX", "LEMMA_EXC"]