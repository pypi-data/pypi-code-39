#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import re
from nltk.tokenize import word_tokenize, sent_tokenize
import spacy

text = text = re.sub(r'(\([^()]*?)(\.)([^()]*?\))', r'\1__.__\3', "fjdsk fds __CODE__. fdjslk")
print(text)
print(sent_tokenize(text))
print(word_tokenize("The system's behavior after you declare a permission depends on how sensitive the permission is org.appache.hadoop.Add().add(int,int)."))
        # f_out.write(sent + "\n")
        # f_out.write(nltk_tokens + "\n")
        # f_out.write(spacy_tokens + "\n")
        # f_out.write("\n")

# from kgtools.wrapper import Lazy

# class Test:
#     def __init__(self, text):
#         self.text = text

#     @Lazy
#     def lemma(self):
#         return self.text + "lemma"

# t = Test("test")
# print(t.lemma)
