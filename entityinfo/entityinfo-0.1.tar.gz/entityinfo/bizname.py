# !pip install python-Levenshtein
# !pip install fuzzywuzzy
# !pip install tldextract
# !python - m spacy download en_core_web_lg
# !pip install abbreviations
from abbreviations import schwartz_hearst
from collections import Counter, defaultdict
from fuzzywuzzy import fuzz
from itertools import product
from itertools import chain
import pandas as pd
import re
from tldextract import extract
import warnings
import en_core_web_lg
nlp = en_core_web_lg.load()


class entityname:
    def __init__(self, search_result):
        entityname.sr = search_result
        self.result_count = len(entityname.sr['items'])
        entityname.search_name = entityname.sr['queries']['request'][0]['searchTerms']

    @classmethod
    def sr_from_str(cls, str_json):
        search_result = eval(str_json)
        return cls(search_result)

    def all_display_url(self):
        '''Return a list of all display url from search results'''
        display_url = []
        for index in range(self.result_count):
            temp = entityname.sr['items'][index]['displayLink']
            display_url.append(temp)
        return display_url

    def all_formatted_url(self):
        '''Return a list of all formatted url from search results'''
        self.formatted_url = []
        for index in range(self.result_count):
            temp = entityname.sr['items'][index]['formattedUrl']
            self.formatted_url.append(temp)
        return self.formatted_url

    @classmethod
    def all_domain_name(cls):
        '''Return a list of all domain name from search results'''
        all_formatted_url = cls(entityname.sr).all_formatted_url()
        display_url = all_formatted_url
        domain_name = [extract(url).domain.lower() for url in display_url]
        return domain_name

    def all_snippet(self, snippet_to_string=False):
        '''
        Return a list of all snippet(description) from search results
        Params:
        args snippet_to_string(bool):
            Default is False. If True, return a string that
            contains all snippet(description) from search result
        '''
        snippet = []
        for index in range(self.result_count):
            temp_snippet = entityname.sr['items'][index]['snippet']
            temp_snippet = re.sub(r'(\(|\))|(\n)|[\xa0...]', "", temp_snippet)
            snippet.append(temp_snippet)
        if snippet_to_string is True:
            snippet = ". ".join(snippet)
            del temp_snippet
        return snippet

    @staticmethod
    def concatenate_list_dict_key_to_string(any_list, key):
        '''
        Concatenate dict inside list to a string
        params:
          args1 any_list(list): any list that contains dict with key:value pair
          args2 key(str): key along which concatenation is required
        Returns:
            single_string: concatenation of dict inside list
        '''
        temp_list = []
        for index in range(len(any_list)):
            key_value = any_list[index][key]
            pattern = r'(\(|\))|(\n)|[\xa0...]'
            key_value_cleaned = re.sub(pattern, "", key_value)
            temp_list.append(key_value_cleaned)
            single_string = ". ".join(temp_list)
        return single_string

    @staticmethod
    def sim_score(list_1, list_2, min_ss_thres=None):
        '''
        Calculates similarity score between each element of two list

        params:
          args1 list_1(list): A list contains words
          args2 list_2(list): A list contains words
          args3 min_ss_thres(int or float):
                Default is 0. Threhold for displaying the sim_score.
                Return list includes the minimum threshold in the results

        Returns:
        ss_df(DataFrame):
            A DataFrame with a simiality score between each element of two list
        '''
        if min_ss_thres is None:
            min_ss_thres = 0
        list_product = [element for element in product(list_1, list_2)]
        list_1_column = []
        list_2_column = []
        sim_score = []
        # store index of all the element of list2 which matches the threshold
        list_2_elem_index = []

        for index, element in enumerate(list_product):
            tsr = fuzz.token_set_ratio(element[0], element[1])
            '''
            creating a list of index of all the element of list_2
            which matches the criteria
            '''
            if index < len(list_2):
                list_2_elem_index.append(index)
            else:
                new_index = index - len(list_2)
                list_2_elem_index.append(new_index)

            sim_score.append(tsr)
            list_1_column.append(element[0])
            list_2_column.append(element[1])
        ss_df = pd.DataFrame({'list_1': list_1_column,
                              'list_2': list_2_column,
                              'sim_score': sim_score,
                              'list_2_elem_index': list_2_elem_index})
        ss_df = ss_df[ss_df.sim_score >= min_ss_thres]
        if not ss_df.empty:
            return ss_df
        else:
            return None

    @staticmethod
    def clean_list_element(string_list, remove,
                           pattern=None, replacement=None):
        '''
        Takes a list of string and remove the required term from list

        params:

        args1 string_list(list): A list that contains values as a string
        args2 remove(str): string to remove from every element of list
        args3 pattern(str): string pattern to search. Default is the term
                            provided as the input.
        args4 replacement(str): replacement for the identified pattern.
                                Default is no replacement

        Returns:
            clean_list(list): a cleaned list
        '''
        if pattern is None:
            pattern = str(remove)
        if replacement is None:
            replacement = ""
        clean_list = []
        for element in string_list:
            new_element = re.sub(pattern, replacement, element).strip()
            clean_list.append(new_element)
            del new_element
        return(clean_list)

    @staticmethod
    def clean_max_count(x, remove):
        '''
        Clean a list and return max of count of each element after cleansing
        Logic:
                1) Remove string from all names
                2) Count for each element after cleansing

        args1 x(list): a list to clean and count
        args2 remove(str): string to remove from each element of list

        Return:
        frequent(str):
            An element with maximum count If cleaned list is not empty.
        '''
        if not isinstance(x, list):
            raise 'x should be a list'
        x = entityname.clean_list_element(string_list=x,
                                   remove=remove)
        if "" in x:
            x.remove("")
        x_dict = Counter(x)
        name_count = len(x_dict)
        if name_count >= 1:
            # org with maximum number presence
            frequent = max(x_dict, key=x_dict.get)
            return frequent
        else:
            return None

    @staticmethod
    def match_index(a, b):
        '''
        Search a in b and return the index of matched element from b

        params:
        args1 a(list): a list of string to search
        args2 b(list): a list to match

        Returns:
            match_index(list): index of element of b that are in a
        '''
        # create a dict of all element with its index(index of duplicate elem)
        if not isinstance(a, (list, str)):
            raise ValueError('{} should be a string or list'.format(a))
        if isinstance(a, str):
            a = [a]
        if not isinstance(b, list):
            raise ValueError('{} should be a list'.format(b))
        dd = defaultdict(list)  # a defaultdict
        for index, element in enumerate(b):
            dd[element].append(index)
        match_index = []
        # matching elements of a with the element of defaultdict
        for element in a:
            if element in dd.keys():
                match_index.append(dd[element])
        match_index = list(chain.from_iterable(match_index))
        match_index.sort()
        return match_index

    @staticmethod
    def near_element(string, split_pattern, text_document, step_size=None):
        '''
        Returns Element whose index is index(string)+step_size

        params:
        args1 string(str): a string whose nearest element is required.
        args2 split_pattern(str): pattern to split the text_document
        args3 text_document(str): a document to search the string and
                            its next element

        step_size(int): Default is 1   
        '''
        if step_size is None:
            step_size = 1
        text_split = [elem.strip() for elem in re.split(
            split_pattern, text_document)]
        #  index of search term in the text document.
        string_index = entityname.match_index(a=string, b=text_split)
        text_split_max_index = len(text_split)-1
        print(string_index)
        near_elem = []
        for index in string_index:
            req_index = index + step_size
            if req_index <= text_split_max_index:
                near_elem.append(text_split[req_index])
        return near_elem

    @staticmethod
    def complete_name(text_document, search_name):
        '''
        Name of an org that is associated with search_name

        params:
            text_document: document that contains information about org
            search_name: full name or abbreviated name of org

        Returns:
            search_name(str):
                Complete name of org if found otherwise return the search_name
        '''
        pattern = search_name.lower()
        replacement = '(' + search_name.lower() + ')'
        new_text_document = re.sub(pattern, replacement, text_document.lower())
        short_long_org = schwartz_hearst.extract_abbreviation_definition_pairs(
            doc_text=new_text_document)

        if short_long_org:
            return short_long_org

        doc = nlp(str(text_document))
        org_list = set([str(x) for x in doc.ents if x.label_ == "ORG"])
        org_list = list(org_list)
        if not org_list:
            warnings.warn('No entity found. Returning search name')
            return search_name
        # if search_name is in the org list, assign org name to search name
        # [search name long form, some_text, short form, any_other_org_name]
        full_org_name = []
        for org in org_list:
            if fuzz.token_set_ratio(search_name, org) == 100:
                full_org_name.append(org)
            else:
                continue
        # [search name long form, search_name, long form search name]
        '''
        Logic:
            remove search_name from all names & check count for each
            org_name.
        Return:
            search_name a full_org_name only if refining process leads
            to removal of all term.
            Happens only when list contains nothing but search_name
        '''
        if full_org_name:
            org_name = entityname.clean_max_count(x=full_org_name,
                                           remove=search_name)
            if org_name:
                return org_name
            else:
                return search_name
        else:
            '''
            Logic: if search name is not in the org list then check is there
            any name in the org_list that is just one step backward or forward
            to the search_name. If not then return the complete name as
            search name
            '''
            text_split_pattern = '(' + "|".join(org_list) + ')'
            near_elem = entityname.near_element(string=search_name,
                                         split_pattern=text_split_pattern,
                                         text_document=text_document)
            if near_elem:
                one_elem = near_elem[0]
                if one_elem[0] == search_name[0]:
                    return one_elem
            else:
                return search_name

    @classmethod
    def find_index(cls, search):
        '''
        Function to find index from Google API search results.

        params:
            arg1 cls(entityname): entityname class instant
            arg2 search(list): list of str to search index

        Returns:
            pg_pi_all_display_url(list): 
            list of all url that contains search term
        '''
        try:
            dis_url = cls(entityname.sr).all_display_url()
            ss_df = cls.sim_score(list_1=[search],
                                  list_2=dis_url,
                                  min_ss_thres=100)
            if ss_df is None:
                return None
            pg_df = ss_df[ss_df.list_1 == search]
            pg_list = list(pg_df.list_2.values)
            pg_pi_all_display_url = list(pg_df.list_2_elem_index.values)
            del pg_df
            del pg_list
            return pg_pi_all_display_url
        except IndexError:
            return None

    @classmethod
    def name_from_wk(cls):
        '''
        Function to return name from wiki page using GS API
        '''
        search = 'wikipedia'
        wk_hp_pi_all = cls(entityname.sr).find_index(search=search)
        if wk_hp_pi_all:
            pattern_1 = r'(https://en.wikipedia.org/wiki/)|(https://en.wikipedia.org/.../)'
            pattern_2 = r'\_|\-'
            name_wk = []
            for wiki_index in wk_hp_pi_all:
                wiki_url = entityname.sr['items'][wiki_index]['formattedUrl']
                name_wk_url = re.sub(pattern_1, "", wiki_url)
                name_wk_url = re.sub(pattern_2, " ", name_wk_url)
                if name_wk_url[0] == search[0]:
                    name_wk.append(name_wk_url)
            return name_wk
        else:
            return None

    @classmethod
    def name_from_hp(cls):
        '''
        Function to return name from home page using GS API

        Returns:
            hp_org(list): list of org from hp
        '''
        hp_pi_all = cls(entityname.sr).find_index(search=entityname.search_name)
        if hp_pi_all:
            hp_title = []
            hp_desc = []
            for hp_pi in hp_pi_all:
                temp_title = entityname.sr['items'][hp_pi]['htmlTitle']
                temp_desc = entityname.sr['items'][hp_pi]['snippet']
                hp_title.append(temp_title)
                hp_desc.append(temp_desc)
            hp_title = ". ".join(hp_title)
            hp_desc = ". ".join(hp_desc)
            clean_title = re.sub(r'[(<b>)|(</b>)]', "", hp_title)
            clean_title = re.sub(r'\.{2,}', ".", clean_title)
            clean_text = clean_title + '.' + hp_desc
            ct_nlp_doc = nlp(clean_text)

            hp_org = [str(x) for x in ct_nlp_doc.ents if x.label_ == "ORG"]
            hp_org = list(set(hp_org))
            return hp_org
        else:
            return None

    @classmethod
    def name_from_sr(cls):
        '''
        Returns fullname from search results
        Returns:
            complete_name(str): name of org associated with search_name
        '''
        name_from_wk = entityname.name_from_wk()
        name_from_hp = entityname.name_from_hp()
        if name_from_wk is None:
            name_from_wk = []
        if name_from_hp is None:
            name_from_hp = []
        name = name_from_wk + name_from_hp
        return_check = None
        if name:
            name_df = entityname.sim_score(list_1=[entityname.search_name], list_2=name,
                                    min_ss_thres=100)

            if name_df is not None:
                name_df = name_df[['list_2']]
                name_df['fuzz_ratio'] = name_df['list_2'].map(
                    lambda x: fuzz.ratio(entityname.search_name, x))
                name = name_df.sort_values(
                    by=['fuzz_ratio'], ascending=False).reset_index(drop=True).list_2[0]
                return_check = 'returning name_df'
                return name
        if return_check is None:
            text_document = cls(entityname.sr).all_snippet(snippet_to_string=True)
            complete_name = cls.complete_name(text_document=text_document,
                                              search_name=entityname.search_name)
            return complete_name
