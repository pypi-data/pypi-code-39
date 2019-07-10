# -*- coding: utf-8 -*-
import argparse
import os
import re
from datetime import date

from konlpy.tag import Okt

from SmiToText.tokenizer import mecab
from SmiToText.tokenizer.nltk import nltkSentTokenizer

''' 
코모란 꼬꼬마, 트위터를 이용한 명사 추출기

'''


class extractNoun(object):

    def __init__(self):
        pass

    def findKoNoun(self, sentence):
        nounSet = set([])

        # hannanum = Hannanum()
        # # print(hannanum.analyze(sentence))
        # hannanumNoun = hannanum.nouns(sentence)
        # nounSet.update(hannanumNoun)

        # kkma = Kkma()
        # # print(kkma.analyze(sentence))
        # kkmaNoun = kkma.nouns(sentence)
        # nounSet.update(kkmaNoun)

        # komoran = Komoran()
        # # print(komoran.analyze(sentence))
        # komaranNoun = komoran.nouns(sentence)
        # nounSet.update(komaranNoun)

        twitter = Okt()
        # print(twitter.analyze(sentence))
        twitterNoun = twitter.nouns(sentence)
        nounSet.update(twitterNoun)

        mecabSentence = mecab.nouns(sentence)
        mecabSentence = mecabSentence.split(" ")
        mecabSentence = [n for n in mecabSentence if len(n) > 0]
        nounSet.update(mecabSentence)

        norm_noun = []
        exception_noun = []

        for nounItem in nounSet:
            if len(nounItem) > 1:
                numList = re.findall(r'\d+', nounItem)
                if len(numList) == 0:
                    nounItem = nounItem.replace("]", "\n")
                    nounItem = nounItem.replace("[", "\n")
                    nounItem = nounItem.replace("(", "\n")
                    nounItem = nounItem.replace(")", "\n")
                    nounItem = nounItem.replace("ㆍ", "\n")
                    nounItem = nounItem.replace("·", "\n")
                    nounItem = nounItem.replace("「", "\n")
                    nounItem = nounItem.replace("」", "\n")
                    nounItem = nounItem.replace(",", "\n")
                    nounItem = nounItem.replace(":", "\n")
                    nounItem = nounItem.replace(";", "\n")
                    nounItem = nounItem.replace(".", "\n")
                    nounItem = nounItem.replace("\"", "\n")
                    nounItem = nounItem.replace("”", "\n")
                    nounItem = nounItem.replace("“", "\n")
                    nounItem = nounItem.replace("'", "\n")

                    nounItemList = nounItem.split("\n")

                    for item in nounItemList:
                        if len(item) > 1:
                            removejosa = ["은", "는",
                                          # "이",
                                          # "가",
                                          # "리노",
                                          "을", "를", "의", "또한", "에", "에게", "등", "거나", "하다", "자로",
                                          "이하", "관이", "했", "이다", "렸다", "렸", "으로", "함께", "한다고", "디뎠", "밝혔", "에서"]

                            # if not str(item).endswith(tuple(removejosa)):
                            if not str(item).endswith(tuple(removejosa)):
                                norm_noun.append(item)
                            else:
                                exception_noun.append(item)

        return_noun = [norm_noun, exception_noun]
        return return_noun


extractnoun = extractNoun()


def extract_file_noun(input, output):
    input_file = open(input, mode='r', encoding='utf-8')
    open(output, mode='w', encoding='utf-8')
    line_number = 1
    while (True):
        line = input_file.readline()
        if not line:
            break;

        line = line.strip()

        for line_array in line.split("\n"):
            sentences = nltkSentTokenizer(line_array)

            sentence_words = []
            for sent in sentences:

                word_list = extractnoun.findKoNoun(sent)

                if len(word_list[0]):
                    for word in word_list[0]:
                        word = word.strip()
                        add_flag = True
                        for char in word:
                            if char in ["‘", "`", ",", "'", "\"", "\\", "|", "!", "@", "#", "$", "%", "^", "&", "*",
                                        "(",
                                        ")", "※", "~",
                                        "-", "_", "=", "+", "<", ">", ".", ";", ":",
                                        "ㄱ", "ㄴ", "ㄲ", "ㅂ", "ㅃ", "ㅈ", "ㅉ", "ㄷ", "ㄸ", "ㄱ", "ㅁ", "ㅇ", "ㄹ", "ㅎ", "ㅅ", "ㅆ",
                                        "ㅍ", "ㅊ", "ㅌ", "ㅋ", "ㅛ", "ㅕ", "ㅑ", "ㅐ", "ㅔ", "ㅗ", "ㅓ", "ㅏ", "ㅣ", "ㅠ", "ㅜ",
                                        "ㅡ"]:
                                add_flag = False
                        if add_flag and len(word) < 4 \
                                and (not word.endswith('니다') \
                                     and not word.endswith('그후로') \
                                     and not word.endswith('가요') \
                                     and not word.endswith('고요') \
                                     and not word.endswith('구요') \
                                     and not word.endswith('나요') \
                                     and not word.endswith('다요') \
                                     and not word.endswith('마요') \
                                     and not word.endswith('바요') \
                                     and not word.endswith('사요') \
                                     and not word.endswith('어요') \
                                     and not word.endswith('자요') \
                                     and not word.endswith('차요') \
                                     and not word.endswith('타요') \
                                     and not word.endswith('해요') \
                                     and not word.endswith('세요') \
                                     and not word.endswith('네요') \
                                     and not word.endswith('케요') \
                                     and not word.endswith('군요') \
                                     and not word.endswith('하') \
                                     and not word.endswith('텐데') \
                                     and not word.endswith('건데') \
                                     and not word.endswith('을려') \
                                     and not word.endswith('을껄') \
                                     and not word.endswith('습니') \
                                     and not word.endswith('씁니') \
                                     and not word.endswith('좀') \
                                     and not word.endswith('처럼') \
                                     and not word.endswith('된') \
                                     and not word.endswith('나') \
                                     and not word.endswith('넣') \
                                     and not word.endswith('먹') \
                                     and not word.endswith('있') \
                                     and not word.endswith('볼라') \
                                     and not word.endswith('…') \
                                     and not word.endswith('비트코') \
                                     and not word.endswith('기자') \
                                     and not word.endswith('할') \
                                     and not word.endswith('위안삼') \
                                     and not word == '기자' \
                                     and not word == str(date.today().day) + '일'
                        ):
                            sentence_words.append(word)

        output_file = open(output, mode='a', encoding='utf-8')
        for word in sentence_words:
            output_file.write(word + os.linesep)
        output_file.close()

        print(line_number, sentence_words)

        line_number += 1


if __name__ == '__main__':
    # extractnoun = extractNoun()
    #
    #
    # while True:
    #     try:
    #         inputText = input("\n\n문장을 입력하세요?: \n")
    #         inputText = unicode(inputText)
    #     except UnicodeDecodeError:
    #         print("다시 입력하세요\n")
    #         continue
    #
    #     if inputText == 'exit':
    #         exit(1)
    #     print(extractnoun.findKoNoun(inputText))

    parser = argparse.ArgumentParser(description="Extract File Noun word")
    parser.add_argument('--input', type=str, required=True, default='', help='Input File')
    parser.add_argument('--output', type=str, required=True, default='', help='Output File')
    args = parser.parse_args()

    if not args.input:
        print("input file is invalid!")
        exit(1)

    if not args.output:
        print("output file is invalid!")
        exit(1)

    input = str(args.input)
    output = str(args.output)

    extract_file_noun(input, output)
