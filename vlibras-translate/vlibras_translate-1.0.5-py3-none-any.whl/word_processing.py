#---------------------------------
#
# Author: Caio Moraes
# Email: <caiomoraes.cesar@gmail.com>
# GitHub: MoraesCaio
#
# LAViD - Laboratório de Aplicações de Vídeo Digital
#
#---------------------------------

import argparse
from os import path
import re


class WordProcessing():

    synonyms = {}
    names = []
    numbers = []
    errors = []

    def __init__(self):

        this_file_path = path.abspath(__file__)
        directory = path.dirname(this_file_path)

        with open(path.join(directory, 'sinonimos'), 'r') as f:
            for l in f:
                key, value = [word.upper() for word in l.replace('\n', '').split(':')]
                if key not in self.synonyms:
                    self.synonyms[key] = value

    def replace_synonyms(self, sentence):
        sentence = sentence.upper()

        for k, v in self.synonyms.items():
            sentence = re.sub(fr'(?<=[^A-Z]){k}(?=[^A-Z])', v, sentence)

        return sentence

    def restore_named_entities(self, sentence, name_symbol='"', number_symbol='\'', error_symbol='#'):

        # self.names = self.names[::-1]
        # self.numbers = self.numbers[::-1]
        # self.errors = self.errors[::-1]

        for name in self.names:
            sentence = re.sub(name_symbol, name, sentence, count=1)

        for number in self.numbers:
            for part in number.replace(' ', '').split(','):
                sentence = re.sub(number_symbol, part, sentence, count=1)

        for error in self.errors:
            sentence = re.sub(error_symbol, error, sentence, count=1)

        self.names, self.numbers, self.errors = [], [], []

        return sentence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sentence')
    args, _ = parser.parse_known_args()

    wp = WordProcessing()
    print(wp.replace_synonyms(args.sentence))


if __name__ == '__main__':
    main()
