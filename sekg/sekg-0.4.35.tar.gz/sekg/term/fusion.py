#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import textdistance
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
import itertools

from sekg.term.synset import Synset
from kgtools.annotation import Parallel, Cache, TimeLog


class Fusion:
    def __init__(self):
        self.DL = textdistance.DamerauLevenshtein()
        self.lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)

    @Cache
    def check_synonym(self, long_term, short_term, max_dis=2, threshold=1 / 4):
        long_name = self.lemmatizer(long_term, 'NOUN')[0].lower()
        short_name = self.lemmatizer(short_term, 'NOUN')[0].lower()
        long_name, short_name = re.sub(r'[-/]', "", long_name), re.sub(r'[-/]', "", short_name)
        long_name, short_name = re.sub(r"\s+", " ", long_name), re.sub(r"\s+", " ", short_name)
        if long_name == short_name:
            return True
        if long_name.replace(" ", "") == short_name.replace(" ", ""):
            return True
        if long_term.lower().rstrip("s") == short_term.lower().rstrip("s"):
            return True
        if long_term.isupper() and short_term.isupper():
            return False

        long_words, short_words = long_name.split(), short_name.split()

        if len(long_words) != len(short_words):
            return False
        for word1, word2 in zip(long_words, short_words):
            if word1[0] != word2[0]:
                return False
            if re.findall(r'[0-9]+', word1) != re.findall(r'[0-9]+', word2):
                return False
            if self.DL.distance(word1, word2) > max_dis or self.DL.normalized_distance(word1, word2) >= threshold:
                return False
        return True

    @Cache
    def check_abbr(self, long_term, short_term, stopwords=None):
        def __check_prefix(long_name, short_name):
            if len(short_name) >= 2 and len(short_name) / len(long_name) < 2 / 3 and long_name.startswith(short_name):
                return True
            return False

        def __check_phrase_word(phrase, word, stopwords):
            long_words = phrase.split()
            if len(word) < len(long_words):
                return False
            if len(long_words) == 1:
                return __check_word_word(phrase, word, stopwords)
            else:
                all_pairs = itertools.combinations([i for i in range(1, len(word), 1)], len(long_words) - 1)
                queue = []
                for pair in all_pairs:

                    temp = []
                    pair = (0, ) + pair + (len(word), )
                    # print(pair)
                    long_word = long_words[0]
                    segment = word[pair[0]:pair[1]]
                    if long_word[0] == segment[0] or (len(long_word) > 1 and long_word[0] in set("aeiou") and segment[0] == long_word[1]):
                        temp.append((long_word, segment))
                    else:
                        continue
                    for i in range(1, len(pair) - 1):
                        long_word = long_words[i]
                        segment = word[pair[i]:pair[i + 1]]
                        if long_word[0] == segment[0]:
                            temp.append((long_word, segment))
                        else:
                            break
                    else:
                        queue.append(temp)
                # print(queue)
                for pairs in queue:
                    for long_word, segment in pairs:
                        # print(segment)
                        if not __check_word_word(long_word, segment, stopwords):
                            return False
                        if len(segment) > 1 and segment != "re":
                            return False
                    else:
                        return True
                return False

        def __check_word_word(long_word, word, stopwords):
            if (len(word) == 1 and (word[0] == long_word[0])) or __check_prefix(long_word, word):
                return True
            return False

        def __in(short_name, long_name):
            beg = 0
            length = len(long_name)
            for ch in short_name:
                index = long_name.find(ch, beg)
                if index == -1:
                    return False
                beg = index + 1
                if beg >= length:
                    return False
            return True

        long_name = self.lemmatizer(long_term, 'NOUN')[0].lower()
        short_name = self.lemmatizer(short_term, 'NOUN')[0].lower()
        long_name, short_name = re.sub(r'[-/]', "", long_name), re.sub(r'[-/]', "", short_name)
        long_name, short_name = re.sub(r"\s+", " ", long_name), re.sub(r"\s+", " ", short_name)

        if not __in(short_name, long_name):
            return False

        # print(long_name, short_name)

        if len(short_name.split()) == 1:
            return __check_phrase_word(long_name, short_name, stopwords)
        else:
            short_words = short_name.split()
            long_words = long_name.split()
            if len(long_words) < len(short_words):
                return False
            while len(short_words) > 0 and short_words[0] == long_words[0]:
                short_words.pop(0)
                long_words.pop(0)
            while len(short_words) > 0 and short_words[-1] == long_words[-1]:
                short_words.pop(-1)
                long_words.pop(-1)
            if len(short_words) == 1:
                # print(long_words, short_words)
                return __check_phrase_word(" ".join(long_words), short_words[0], stopwords)
            else:
                return False

    def handle_pairs(self, pair_list, stopwords):
        inner_synonyms = set()
        inner_abbreviations = set()
        for t1, t2 in pair_list:
            # print("%s, %s" % (t1.text, t2.text))
            if len(t1) == 1 or len(t2) == 1:
                continue
            short_term, long_term = (t1, t2) if len(t1) <= len(t2) else (t2, t1)
            if self.check_synonym(long_term, short_term):
                inner_synonyms.add((long_term, short_term))
            elif self.check_abbr(long_term, short_term, stopwords):
                inner_abbreviations.add((short_term, long_term))
        return inner_synonyms, inner_abbreviations

    def detect_relations(self, terms, stopwords):
        pairs = [(t1, t2) for t1, t2 in itertools.combinations(terms, 2)]
        return self.handle_pairs(pairs, stopwords)

    def merge_synonyms(self, synonyms_relations):
        queue = [set(r) for r in synonyms_relations]
        # print(queue)
        # print("Merge synonyms")

        def __merge(queue):
            synonyms = []
            done = True
            while len(queue) > 0:
                now = queue.pop(0)
                # print("now:", now)
                merged = []
                for r in queue:
                    if len(r & now) > 0:
                        now |= r
                        merged.append(r)
                        done = False
                for r in merged:
                    queue.remove(r)
                synonyms.append(now)
            if done:
                return synonyms
            else:
                return __merge(synonyms)
        synonyms = set([Synset(synonym) for synonym in __merge(queue)])
        return synonyms

    def merge_abbrs(self, abbr_relations, synonyms, threshold=0.5):
        term2synset = {}
        for synset in synonyms:
            for term in synset.terms:
                term2synset[term] = synset

        abbr2fullname = {}
        for start, end in abbr_relations:
            if start not in term2synset:
                term2synset[start] = Synset(set([start]))
            if end not in term2synset:
                term2synset[end] = Synset(set([end]))
            start_synset = term2synset[start]
            end_synset = term2synset[end]
            if start_synset not in abbr2fullname:
                abbr2fullname[start_synset] = set()
            abbr2fullname[start_synset].add(end_synset)

        abbrs = set()
        for abbr, fullnames in abbr2fullname.items():
            for fn in fullnames:
                fn += abbr
        synsets = set(term2synset.values())
        return synsets

    @TimeLog
    def fuse(self, terms, term_count=None, stopwords=None):

        synonym_relations, abbr_relations = self.detect_relations(terms, stopwords)
        # print("syn: ", [(t1.text, t2.text) for t1, t2 in synonym_relations])
        # print("abbr:", [(t1.text, t2.text) for t1, t2 in abbr_relations])
        synonyms = self.merge_synonyms(synonym_relations)
        synsets = self.merge_abbrs(abbr_relations, synonyms)

        visited = set()
        for synset in synsets:
            visited.update(synset.terms)
        for term in terms - visited:
            synsets.add(Synset({term}))

        if term_count is not None:
            for synset in synsets:
                synset.init_count(term_count)
        return synsets



