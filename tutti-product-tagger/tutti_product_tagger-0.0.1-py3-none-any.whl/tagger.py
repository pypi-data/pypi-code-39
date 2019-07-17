"""
This script assigns a product tag to each item of the test data set to compute accuracy of
our tagging algorithm
"""
import re
from collections import OrderedDict
import pandas as pd
from logging import getLogger

script_name = 'tutti-product-tagger'
log = getLogger(script_name)


# Dict that maps each tag to the related keywords for regex tagging
word_terminations = r'(\s|$|,|\.)'
tag_keyword_mapping = {
    'furniture': OrderedDict([
        ('armchair', [
            r'sessel{}'.format(word_terminations),
        ]),
        ('bean bag chair', [
            r'sitzsack{}'.format(word_terminations),
        ]),
        ('bed', [
            r'bett{}'.format(word_terminations),
            r'bettgestell{}'.format(word_terminations),
            r'lattenrost{}'.format(word_terminations),
            r'lättlirost{}'.format(word_terminations),
        ]),
        ('bench', [
            r'bank{}'.format(word_terminations),
        ]),
        ('carpet/rug', [
            r'teppich{}'.format(word_terminations),
        ]),
        ('chair', [
            r'stuhl{}'.format(word_terminations),
            r'stühle{}'.format(word_terminations),
        ]),
        ('chest/box', [
            r'kasten{}'.format(word_terminations),
        ]),
        ('clothes rack', [
            r'kleiderständer{}'.format(word_terminations),
        ]),
        ('commode', [
            r'kommode{}'.format(word_terminations),
            r'kommoden{}'.format(word_terminations),
            r'komode{}'.format(word_terminations),
        ]),
        ('cupboard', [
            r'schrank{}'.format(word_terminations),
            r'buffet{}'.format(word_terminations),
        ]),
        ('desk', [
            r'schreibtisch{}'.format(word_terminations),
            r'bürotisch{}'.format(word_terminations),
            r'sekretär{}'.format(word_terminations),
            r'pult{}'.format(word_terminations),
        ]),
        ('display cabinet', [
            r'vitrine{}'.format(word_terminations),
        ]),
        ('door', [
            r'tür{}'.format(word_terminations),
        ]),
        ('filing cabinet', [
            r'aktenschrank{}'.format(word_terminations),
            r'korpus{}'.format(word_terminations),
        ]),
        ('garden chair', [
            r'gartenstuhl{}'.format(word_terminations),
            r'gartenstühle{}'.format(word_terminations),
        ]),
        ('garden table', [
            r'gartentisch{}'.format(word_terminations),
        ]),
        ('mattress', [
            r'matratze{}'.format(word_terminations),
        ]),
        ('mirror', [
            r'spiegel{}'.format(word_terminations),
        ]),
        ('picture frame', [
            r'bilderrahmen{}'.format(word_terminations),
        ]),
        ('pillow', [
            r'kissen{}'.format(word_terminations),
        ]),
        ('shelf', [
            r'regal{}'.format(word_terminations),
            r'regale{}'.format(word_terminations),
            r'kallax{}'.format(word_terminations),
            r'ablage{}'.format(word_terminations),
        ]),
        ('shoe cabinet', [
            r'schuhschrank{}'.format(word_terminations),
            r'schuhkasten{}'.format(word_terminations),
        ]),
        ('sideboard', [
            r'sideboard{}'.format(word_terminations),
            r'sideboards{}'.format(word_terminations),
            r'tv-{}'.format(word_terminations),
            r'fernsehmöbel{}'.format(word_terminations),
            r'tv möbel{}'.format(word_terminations),
        ]),
        ('sofa', [
            r'sofa{}'.format(word_terminations),
            r'couch{}'.format(word_terminations),
            r'polstergruppe{}'.format(word_terminations),
            r'bett-sofa{}'.format(word_terminations),
        ]),
        ('stool', [
            r'hocker{}'.format(word_terminations),
            r'hoker{}'.format(word_terminations),
        ]),
        ('table', [
            r'tisch{}'.format(word_terminations),
            r'tische{}'.format(word_terminations),
            r'tischli{}'.format(word_terminations),
        ]),
        ('wardrobe', [
            r'kleiderschrank{}'.format(word_terminations),
            r'garderobe{}'.format(word_terminations),
        ]),
    ])
}

# Compile regex expressions for faster execution
tag_keyword_mapping_compiled = {
    cat: OrderedDict([
        (key, [re.compile(x) for x in val]) for key, val in tag_keyword_mapping[cat].items()
    ]) for cat in tag_keyword_mapping
}


def assign_tag_to_subject_body(df: pd.DataFrame, subject_col: str, body_col: str = None,
                               category: str = 'furniture') -> str:
    """
    Assign tag to item using tag->keyword mapping

    :param df: pd.DataFrame containing the items
    :param subject_col: name of column holding the title of ads in df
    :param body_col: name of column holding the body of ads in df
    :param category: name of the category of the ad
    """
    tags = dict()
    for tag, pattern_list in tag_keyword_mapping_compiled[category].items():
        for pattern in pattern_list:
            match = pattern.search(df[subject_col].lower())
            if match:
                tags.update({tag: match.start()})

    if body_col:
        if len(tags) == 0:
            for tag, pattern_list in tag_keyword_mapping_compiled[category].items():
                for pattern in pattern_list:
                    match = pattern.search(df[body_col].lower())
                    if match:
                        tags.update({tag: match.start()})

    if len(tags) == 0:
        return 'other'
    else:
        return min(tags, key=tags.get)


def assign_tag_to_string(text: str, category: str = 'furniture'):
    """
    Assign tag to item using tag->keyword mapping.

    :param text: string to parse
    :param category: name of the category of the ad
    """
    tags = dict()
    for tag, pattern_list in tag_keyword_mapping_compiled[category].items():
        for pattern in pattern_list:
            match = pattern.search(text.lower())
            if match:
                tags.update({tag: match.start()})

    if len(tags) == 0:
        return {'tag': 'other'}
    else:
        return {'tag': min(tags, key=tags.get)}
