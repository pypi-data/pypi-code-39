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
from .singleton import Singleton


class WordProcessing(metaclass=Singleton):

    synonyms = {}
    sorted_synonyms_keys = []
    names = []
    numbers = []
    errors = []

    def __init__(self):

        this_file_path = path.abspath(__file__)
        directory = path.dirname(this_file_path)

        with open(path.join(directory, 'palavras_compostas_e_sinonimos'), 'r') as file:

            for line in file:

                key, value = [part for part in line.replace('\n', '').upper().split(';')]

                if key not in self.synonyms:
                    self.synonyms[key] = value
                    self.sorted_synonyms_keys.append(key)

            self.sorted_synonyms_keys.sort(key=lambda x: -len(x))

    def replace_synonyms(self, sentence):

        for key in self.sorted_synonyms_keys:
            # replace only if is not part of a word
            # underline prevents errors like
            #  prisão domiciliar -> prisão_casa (right translation: prisão_domiciliar)
            sentence = re.sub(fr'(?:^|(?<=[^A-Z_])){key}(?=[^A-Z_]|$)', self.synonyms[key], sentence)

        return sentence

    def restore_named_entities(self, sentence, name_symbol='"', number_symbol='\'', error_symbol='#'):

        for name in self.names:
            sentence = re.sub(name_symbol, name.upper(), sentence, count=1)

        for number in self.numbers:
            for part in number.replace(' ', '').split(','):
                sentence = re.sub(number_symbol, part, sentence, count=1)

        for error in self.errors:
            sentence = re.sub(error_symbol, error.upper(), sentence, count=1)

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
