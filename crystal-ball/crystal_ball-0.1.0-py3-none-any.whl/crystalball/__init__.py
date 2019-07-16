import pandas as pd
import glob
import csv
import os
import seaborn as sns
import matplotlib.pyplot as plt
from  builtins import any

class CrystalBall:
    
    def __init__(self, list_of_csvs:list, csvname_to_colnames_list:dict, csvname_to_IDs:dict, csvname_to_nonIDs:dict, all_IDs:list, all_nonIDs:list, csvname_to_one_ID:list):
        # get list of all files in current directory that end in .csv
        self.list_of_csvs = list_of_csvs

        # create dictionary where csvname maps to colnames
        self.csvname_to_colnames_list = csvname_to_colnames_list

        # create dictionary where csvname maps to colnames that have the substring "ID"
        self.csvname_to_IDs = csvname_to_IDs

        # create dictionary where csvname maps to colnames that do not have the substring "ID"
        self.csvname_to_nonIDs = csvname_to_nonIDs

        # create list of only unique IDs
        self.all_IDs = all_IDs

        # create list of only unique nonIDs
        self.all_nonIDs = all_nonIDs
        
        # create list of all column names (IDs + nonIDs)
        self.all_colnames = list(all_IDs.union(all_nonIDs))

        # create dictionary that maps out relationship, one csvname to one ID
        self.csvname_to_one_ID = csvname_to_one_ID
    
    @classmethod
    def run(self, rel_dir):
        list_of_csvs = sorted(glob.glob(rel_dir))
        csvname_to_colnames_list = {}
        csvname_to_IDs = {}
        csvname_to_nonIDs = {}
        all_IDs = set()
        all_nonIDs = set()
        csvname_to_one_ID = []
        for csv_name in list_of_csvs:
            with open(csv_name, "rt") as f:
                reader = csv.reader(f)
                try:
                    col_names = next(reader)
                    csvname_to_colnames_list[csv_name] = col_names
                    ids = []
                    non_ids = []
                    for col_name in col_names:
                        if 'ID' in col_name or 'Id' in col_name:
                            csvname_to_one_ID.append([os.path.split(csv_name)[1], col_name])
                            ids.append(col_name)
                        else:
                            non_ids.append(col_name)
                    csvname_to_IDs[csv_name] = ids
                    csvname_to_nonIDs[csv_name] = non_ids
                    all_IDs.update(ids)
                    all_nonIDs.update(non_ids)
                    continue
                except StopIteration:
                    continue
                except:
                    continue
        return CrystalBall(list_of_csvs, csvname_to_colnames_list, csvname_to_IDs, csvname_to_nonIDs, all_IDs, all_nonIDs, csvname_to_one_ID)

    def contains(self, keywords: list, all_colnames: list=None) -> list:    

        """
        PURPOSE: 
        - Determine whether a keyword (substring) exists in a given list of column names (strings). 
        - Note: This search is case sensitive!
        
        PARAMETERS:
        - keywords [list of strings]: a key word
        - all_colnames [list of strings]: 
            List of column names of a table, or for many tables. 
            If no argument is provided, this function will use the column names generated when the run method was called.

        RETURNS:
        - a boolean: True if substring exists in list of strings, otherwise False.

        EXAMPLES:
        - Example 1:
            colnames = ['id', 'name', 'title']
            CrystalBall.contains('name', colnames) returns True
            CrystalBall('Name', colnames) returns False
        """
        
        if all_colnames is None:
            return [any(keyword in colname for colname in self.all_colnames) for keyword in keywords]
        else:
            return [any(keyword in colname for colname in all_colnames) for keyword in keywords]

        
    def featureSearch(self, keyword_list, all_colnames=None, mode='UNION'):
        ##implement INTERSECTION mode later
        if type(keyword_list) is not list:
            raise Exception('keyword_list argument expects a list')
        
        if all_colnames is None:
            suggested_colnames = set()
            for colname in self.all_colnames:
                for keyword in keyword_list:
                    if keyword in colname:
                        suggested_colnames.add(colname)
            return list(suggested_colnames)
        
        else:
            suggested_colnames = set()
            for colname in all_colnames:
                for keyword in keyword_list:
                    if keyword in colname:
                        suggested_colnames.add(colname)
            return list(suggested_colnames)

        
    
    def tableSearch(self, keyword_list, csvname_to_colnames_list=None, mode='UNION'):
        def columnNamesContainKeyword(keyword, colname_list):
            return any(keyword in colname for colname in colname_list)
        
        if mode is 'UNION':
            if csvname_to_colnames_list is None:
                return list(filter(lambda x: x is not None, [key if False not in [True if any(keyword in colname for colname in self.csvname_to_colnames_list[key]) else False for keyword in keyword_list] else None for key in self.csvname_to_colnames_list]))
            else:
                return list(filter(lambda x: x is not None, [key if False not in [True if any(keyword in colname for colname in csvname_to_colnames_list[key]) else False for keyword in keyword_list] else None for key in csvname_to_colnames_list]))
        elif mode is 'INTERSECTION':
            csv_matches = []
            if csvname_to_colnames_list is None:
                for csvname in self.csvname_to_colnames_list:
                    keyword_checklist = []
                    for keyword in keyword_list:
                        keyword_checklist.append(columnNamesContainKeyword(keyword, self.csvname_to_colnames_list[csvname]))
                    if False not in keyword_checklist:
                        csv_matches.append(csvname)
                return csv_matches
            else:
                print("implement later")

        
    def openTable(self, rel_dir):
        return pd.read_csv(rel_dir, engine='python', encoding='utf-8', error_bad_lines=False)
        
        
    def subTable(self, supertable, primary_keys:list, columns:list):
        """
        PURPOSE:
        
        PARAMETERS:
        - supertable: table from which to select columns from in order to form a subtable
        - primary_keys: index for the new subtable.
        - columns: columns that the subtable should contain.
            
        RETURNS:
            DataFrame: the newly formed subtable
        
        EXAMPLES:
        """
        combined = primary_keys.copy()
        combined.extend(columns)
        subtable = supertable[combined].set_index(primary_keys)
        return subtable
        
        
    def mergeTables(self, tables:list):
        """
        default inner join.
        merges by index.
        """
        if len(tables) < 2:
            raise Exception("need at least two tables in order to merge")
        
        num_of_dropped_rows = 0
        max_num_of_rows = max(len(tables[0]), len(tables[1]))
        
        current_merge = tables[0].merge(tables[1], how='inner', left_index=True, right_index=True)
        
        diff = max_num_of_rows - len(current_merge)
        max_num_of_rows = len(current_merge)
        num_of_dropped_rows += diff
        
        if len(tables) - 2 > 0:
            for i in range(2, len(tables)):
                current_merge = current_merge.merge(table[i], how='inner', left_index=True, right_index=True)
                diff = max_num_of_rows - len(current_merge)
                max_num_of_rows = len(current_merge)
                num_of_dropped_rows += diff
        print('Number of Dropped Rows: ',num_of_dropped_rows)
        return current_merge
    
    
    def analyzeRelationships(self, to_analyze:dict, visualize=True):
        """
        compare and contrast basic stats of two different indexes
        should be able to determine if these two indexes are related or not.
        potential_relations: list of Series
        """
        descriptions = []
        boxplot_data = []
        boxplot_xtick_labels = []
        for pair in to_analyze:
            new_name = pair[1].name + ' from ' + pair[0]
            descriptions.append(pair[1].describe().rename(new_name))
            boxplot_data.append(pair[1])
            boxplot_xtick_labels.append(new_name)
        
        if visualize:
            g = sns.boxplot(data=boxplot_data)
            g.set(
                title='Relationship Analysis',
                xlabel='Features', 
                ylabel='Numerical Values',
                xticklabels=boxplot_xtick_labels
            )
            plt.xticks(rotation=-10)

        description_table = pd.concat(descriptions, axis=1)
        return description_table

    
    def compareRelationship(self, to_analyze1, to_analyze2, visualize=False):
        """
        to_analyze1 = [csv_name, series]
        to_analyze2 = [csv_name, series]
        """
        descriptions = []
        boxplot_data = []
        boxplot_xtick_labels = []
        
        new_name = to_analyze1[1].name + ' from ' + to_analyze1[0]
        description1 = to_analyze1[1].describe().rename(new_name)
        descriptions.append(description1)
        boxplot_data.append(to_analyze1[1])
        boxplot_xtick_labels.append(new_name)
        
        new_name = to_analyze2[1].name + ' from ' + to_analyze2[0]
        description2 = to_analyze2[1].describe().rename(new_name)
        descriptions.append(description2)
        boxplot_data.append(to_analyze2[1])
        boxplot_xtick_labels.append(new_name)
        
        if visualize:
            g = sns.boxplot(data=boxplot_data)
            g.set(
                title='Relationship Analysis',
                xlabel='Features', 
                ylabel='Numerical Values',
                xticklabels=boxplot_xtick_labels
            )
            plt.xticks(rotation=-10)
        
        diff_description = description1 - description2
        diff_description.name = "Difference"
        descriptions.append(diff_description)
        description_table = pd.concat(descriptions, axis=1)
        return description_table
        
    