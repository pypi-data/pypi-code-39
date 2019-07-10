#-*- coding:utf8 -*-
'''
g2pC: A context-aware grapheme-to-phoneme module for Chinese
https://github.com/kyubyong/g2pC
kbpark.linguist@gmail.com
'''
import pickle
import re
import os
import pkuseg
from itertools import chain


def convert_hanzi_string_to_number(string):
    return "/".join(str(ord(char)) for char in string)


def word2features(sent, i):
    word = convert_hanzi_string_to_number(sent[i][0])
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word':word,
        'postag': postag,
        }
    if i == 0:
        features['BOS'] = True
    else:
        if i > 0:
            word1 = convert_hanzi_string_to_number(sent[i-1][0])
            postag1 = sent[i-1][1]
            features.update({
                '-1:word': word1,
                '-1:postag': postag1,
            })
        if i > 1:
            word1 = convert_hanzi_string_to_number(sent[i-2][0])
            postag1 = sent[i-2][1]
            features.update({
                '-2:word': word1,
                '-2:postag': postag1,
            })
        if i > 2:
            word1 = convert_hanzi_string_to_number(sent[i-3][0])
            postag1 = sent[i-3][1]
            features.update({
                '-3:word': word1,
                '-3:postag': postag1,
            })

    if i == len(sent)-1:
        features['EOS'] = True
    else:
        if i < len(sent)-1:
            word1 = convert_hanzi_string_to_number(sent[i+1][0])
            postag1 = sent[i+1][1]
            features.update({
                '+1:word': word1,
                '+1:postag': postag1,
            })
        if i < len(sent)-2:
            word1 = convert_hanzi_string_to_number(sent[i+2][0])
            postag1 = sent[i+2][1]
            features.update({
                '+2:word': word1,
                '+2:postag': postag1,
            })
        if i < len(sent)-3:
            word1 = convert_hanzi_string_to_number(sent[i+3][0])
            postag1 = sent[i+3][1]
            features.update({
                '+3:word': word1,
                '+3:postag': postag1,
            })

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def _tone_change(hanzis, pinyins):
    '''https://en.wikipedia.org/wiki/Standard_Chinese_phonology#Tone_sandhi
    '''
    # Word-internally
    # bu4 + A4 -> (bu|yi)2 A4 (word-internally)
    pinyins = [re.sub("bu4( [^ ]+?4)", r"bu2\1", pinyin) for pinyin in pinyins]

    # yi1 + A4 -> yi2 A4 (word-internally)
    pinyins = [re.sub("yi1( [^ ]+?4)", r"yi2\1", pinyin) for pinyin in pinyins]

    # yi1 + A{1,2,3} -> yi4 A{1,2,3} (word-internally)
    pinyins = [re.sub("yi1( [^ ]+?[123])", r"yi4\1", pinyin) for pinyin in pinyins]

    # 33 -> 23
    pinyins = [re.sub("3( [^ ]+?3)", r"2\1", pinyin) for pinyin in pinyins]

    pinyins = " ".join(pinyins).split() # disregard word boundaries

    # Holistically
    # 33 -> 23
    pinyins = re.sub("3( [^ ]+?3)", r"2\1", " ".join(pinyins)).split()

    # A不A -> A bu5 A
    indices = [m.start(0)+1 for m in re.finditer(r"(.)不\1", hanzis)]
    for idx in indices:
        pinyins[idx] = "bu5"

    # A一A -> A yi5 A
    indices = [m.start(0) + 1 for m in re.finditer(r"(.)一\1", hanzis)]
    for idx in indices:
        pinyins[idx] = "yi5"

    return pinyins


def tone_change(results):
    hanzis = "".join(result[0] for result in results)
    pinyins = [result[2] for result in results]

    pinyins = _tone_change(hanzis, pinyins)

    rule_applied = []
    for result in results:
        n_syls = len(result[2].split())
        _pinyin = " ".join(pinyins[:n_syls])
        pinyins = pinyins[n_syls:]
        result = (result[0], result[1], result[2], _pinyin, result[3], result[4])
        rule_applied.append(result)
    return rule_applied


class G2pC(object):
    def __init__(self):
        '''
        self.cedict looks like:
        {行: {pron: [hang2, xing2],
        meaning: [/row/line, /to walk/to go],
        trad: [行, 行]}
        '''
        self.seg = pkuseg.pkuseg(postag=True)
        self.cedict = pickle.load(open(os.path.dirname(os.path.abspath(__file__)) + '/cedict.pkl', 'rb'))
        self.crf = pickle.load(open(os.path.dirname(os.path.abspath(__file__)) + '/crf100.bin', 'rb'))

    def __call__(self, string):
        # fragment into sentences
        sents = re.sub("([！？。])", r"\1[SEP]", string)
        sents = sents.split("[SEP]")

        _sents = []
        for sent in sents:
            if len(sent)==0: continue

            analyzed = []
            # STEP 1
            tokens = self.seg.cut(sent)

            # STEP 2
            for word, pos in tokens:
                if word in self.cedict:
                    features = self.cedict[word]
                    prons = features["pron"]
                    meanings = features["meaning"]
                    trads = features["trad"]
                    analyzed.append((word, pos, prons, meanings, trads))
                else:
                    for char in word:
                        if char in self.cedict:
                            features = self.cedict[char]
                            prons = features["pron"]
                            meanings = features["meaning"]
                            trads = features["trad"]
                        else:
                            prons = [char]
                            meanings = [""]
                            trads = [char]
                        analyzed.append((char, pos, prons, meanings, trads))
            _sents.append(analyzed)

        # STEP 3
        features = [sent2features(_sent) for _sent in _sents]
        preds = self.crf.predict(features)

        # concatenate sentences
        tokens = chain.from_iterable(_sents)
        preds = chain.from_iterable(preds)

        # determine pinyin
        ret = []
        for (word, pos, prons, meanings, trads), p in zip(tokens, preds):
            p = p.replace("-", " ")
            if p in prons:
                pinyin = p
            else:
                pinyin = prons[0]
            ind = prons.index(pinyin)
            meaning = meanings[ind]
            trad = trads[ind]
            ret.append((word, pos, pinyin, meaning, trad))

        # STEP 4
        ret = tone_change(ret)
        return ret


if __name__ == "__main__":
    # strings = ["有一次", "第一次", "十一二岁来到戏校", "同年十一月", "一九八二年英文版", "欧洲统一步伐", "吉林省一号工程", "一是选拔优秀干部"]
    strings = "邓,吴,鄂,皖,蔡,萨,廖,宋,秦,刘,滧,闫,陕,郑,郝,犇,鹏,陇,祾,渭,邹,濮,梵,佟,韩,龚,洛,湘,婍,沂,隋,洣,潘,蒋,禹,喲,闽,湳,綪,睍,孻,汶,杭,吶,黔,渝,辽,銶,滇,灞,溁,浙,渤,邵,赣,淮,郸,彭,傣,蜀,沪,癍,郦,滕,滦,榣,姈,亳,漳,邢,涪,尧,昝,羲,媃,粤,鞑"
    g2p = G2pC()
    for string in strings.split(","):
        results = g2p(string)
        print(results)
        # print(string)
        # print("original:", " ".join(result[2] for result in results))
        # print("descriptive (tone changed):", " ".join(result[3] for result in results))
        # print()

