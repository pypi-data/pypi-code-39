# Copyright (C) 2018 Majormode.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY,# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import locale
import os
import random

from majormode.perseus.model.enum import Enum


class NameGenerator:
    """
    Name generator module that analyzes sample text and produces similar
    words.
    """
    def __init__(self, language_file, forbidden_file=None):
        self.min_syl = 2
        self.max_syl = 4
        
        #load language file
        with open(language_file, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            
            self.syllables = lines[0].split(',')  #first line, list of syllables
            
            starts_ids = [int(n) for n in lines[1].split(',')]  #next 2 lines, start syllable indexes and counts
            starts_counts = [int(n) for n in lines[2].split(',')]
            self.starts = list(zip(starts_ids, starts_counts))  #zip into a list of tuples
            
            ends_ids = [int(n) for n in lines[3].split(',')]  #next 2, same for syllable ends
            ends_counts = [int(n) for n in lines[4].split(',')]
            self.ends = list(zip(ends_ids, ends_counts))
            
            #starting with the 6th and 7th lines, each pair of lines holds ids and counts
            #of the "next syllables" for a previous syllable.
            self.combinations = []
            for (ids_str, counts_str) in zip(lines[5:None:2], lines[6:None:2]):
                if len(ids_str) == 0 or len(counts_str) == 0:  #empty lines
                    self.combinations.append([])
                else:
                    line_ids = [int(n) for n in ids_str.split(',')]
                    line_counts = [int(n) for n in counts_str.split(',')]
                    self.combinations.append(list(zip(line_ids, line_counts)))
        
        #load forbidden words file if needed
        if forbidden_file is None:
            self.forbidden = ''
        else:
            self.forbidden = _load_sample(forbidden_file)
    
    def generate_name(self, no_repeat=False):
        #random number of syllables, the last one is always appended
        num_syl = random.randint(self.min_syl, self.max_syl - 1)
        
        #turn ends list of tuples into a dictionary
        ends_dict = dict(self.ends)
        
        #we may have to repeat the process if the first "min_syl" syllables were a bad choice
        #and have no possible continuations; or if the word is in the forbidden list.
        word = []
        word_str = ''

        while len(word) < self.min_syl or self.forbidden.find(word_str) != -1:
            #start word with the first syllable
            syl = _select_syllable(self.starts, 0)
            word = [self.syllables[syl]]
            
            for i in range(1, num_syl):
                #don't end yet if we don't have the minimum number of syllables
                if i < self.min_syl:
                    end = 0
                else:
                    end = ends_dict.get(syl, 0)  #probability of ending for this syllable
                
                #select next syllable
                syl = _select_syllable(self.combinations[syl], end)
                if syl is None:
                    break  #early end for this word, end syllable was chosen
                
                word.append(self.syllables[syl])
                
            else:  #forcefully add an ending syllable if the loop ended without one
                syl = _select_syllable(self.ends, 0)
                word.append(self.syllables[syl])
            
            word_str = ''.join(word)
        
        #to ensure the word doesn't repeat, add it to the forbidden words
        if no_repeat:
            self.forbidden = self.forbidden + '\n' + word_str
        
        return word_str.capitalize()

def _select_syllable(counts, end_count):
    if not counts:
        return None  #no elements to choose from
    
    #"counts" holds cumulative counts, so take the last element in the list
    #(and 2nd in that tuple) to get the sum of all counts
    chosen = random.randint(0, counts[-1][1] + end_count)
    
    for (syl, count) in counts:
        if count >= chosen:
            return syl

    return None

def _load_sample(filename):
    #get sample text
    with open(filename, 'r') as f:
        sample = ''.join(f.readlines()).lower()
    
    #convert accented characters to non-accented characters
    sample = locale.strxfrm(sample)
    
    #remove all characters except letters from A to Z
    a = ord('a')
    z = ord('z')
    sample = ''.join([
        c if (ord(c) >= a and ord(c) <= z) else ' '
            for c in sample])
    
    return sample


class NameGeneratorFactory:
    """
    Wrapper around the free module ``name-gen`` that generate names.

    Possible applications include generation of names for characters,
    places, etc., that sounds similar to a given language.

    Data files of the module ``name-gen`` MUST BE copied into the path
    ``./data/name-gen/`` relative to path of this module.

    Reference:

    * name-gen; Joao Henriques; https://code.google.com/p/name-gen/
    """
    Language = Enum(
        'Beowulf',
        'Celticmyth',
        'Elven',
        'Greek',
        'Greek2',
        'Hebrew',
        'Hebrew2',
        'Japanese',
        'Japanese2',
        'Lusiadas',
        'Lusiadas2',
        'Norse',
        'Norsemyth',
        'Odin',
        'Polish',
        'Polish2',
        'Roman',
        'Russian',
        'Saxon',
        'Welsh'
    )

    LANGUAGE_FILE_NAMES = {
        Language.Beowulf: 'beowulf.txt',
        Language.Celticmyth: 'celticmyth.txt',
        Language.Elven: 'elven.txt',
        Language.Greek: 'greek.txt',
        Language.Greek2: 'greek2.txt',
        Language.Hebrew: 'hebrew.txt',
        Language.Hebrew2: 'hebrew2.txt',
        Language.Japanese: 'japanese.txt',
        Language.Japanese2: 'japanese2.txt',
        Language.Lusiadas: 'lusiadas.txt',
        Language.Lusiadas2: 'lusiadas2.txt',
        Language.Norse: 'norse.txt',
        Language.Norsemyth: 'norsemyth.txt',
        Language.Odin: 'odin.txt',
        Language.Polish: 'polish.txt',
        Language.Polish2: 'polish2.txt',
        Language.Roman: 'roman.txt',
        Language.Russian: 'russian.txt',
        Language.Saxon: 'saxon.txt',
        Language.Welsh: 'welsh.txt',
    }


    @staticmethod
    def get_instance(language):
        """
        Create a new instance of name generator providing a language.


        :param language: a value of the enumerator ``NameGenerator.Language``.


        :return: the instance `NameGen` of the name generator.
        """
        if language not in NameGeneratorFactory.Language:
            raise ValueError('Invalid language name')

        return NameGenerator(os.path.join(os.path.abspath(
                os.path.dirname(__file__)), 'languages',
                NameGeneratorFactory.LANGUAGE_FILE_NAMES[language]))
