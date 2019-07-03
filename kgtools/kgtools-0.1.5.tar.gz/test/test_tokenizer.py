#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kgtools.nlp.tokenizer import CompoundTokenizer

tokenizer = CompoundTokenizer()
sent = tokenizer.word_tokenize("The word-frequency returns the sequence element's frequency over training corpus.")
print(sent)
for token in sent:
    print(token)
