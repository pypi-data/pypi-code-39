import pandas as pd
import glob
import csv
import os
import seaborn as sns
import matplotlib.pyplot as plt
from builtins import any

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
        """ Initialize the Crystal Ball object for a given directory that contains the CSVs.

        Parameters
        ----------
        rel_dir : str
            - A string that contains the relative directory, which contains the CSVs to analyze.

        Returns
        --------
        CrystalBall
            - CrystalBall that has all class variables initialized by this run script.

        Examples
        --------
        .. code-block:: python

            relative_directory = './folder1/folder2'
            crystalBall = CrystalBall.run(relative_directory)
        """

        rel_dir = rel_dir + '/*.csv'
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

        """ Check if keywords exist in all_colnames.
        
        - Determine whether a keyword (substring) exists in a given list of column names (strings). 
        - Note: This search is case sensitive!

        Parameters
        ----------
        keywords : list[str]
            - List of key words that the user is interested in
        all_colnames : list[str]
            - List of column names of a table, or for many tables. 
            - If no argument is provided, this function will use the column names generated when the run method was called.
        
        Returns
        -------
        list
            - Each index corresponds to a keyword. 
            - For each index, True if substring exists in list of strings, otherwise False.

        Examples
        --------
        >>> colnames = ['id', 'name', 'title']
        >>> cb.contains(['name'], colnames)
        [True]
        >>> cb.contains(['Name'], colnames)
        [False]
        >>> cb.contains(['name', 'Name'], colnames)
        [True, False]
        """
        
        if all_colnames is None:
            return [any(keyword in colname for colname in self.all_colnames) for keyword in keywords]
        else:
            return [any(keyword in colname for colname in all_colnames) for keyword in keywords]

        
    def featureSearch(self, keywords: list, all_colnames: list=None, mode: str='UNION') -> list:
        """ Find the columns that contain the keywords.

        - Find features (column names) that contain the substrings specified in keywords. 
        - Note: This search is case sensitive!

        Parameters
        ----------
        keywords : list[str]
            - List of key words that the user is interested in
        colnames : list[str]
            - List of column names of a table, or for many tables. 
            - If no argument is provided, this function will use the column names generated when the run method was called.
        
        Returns
        --------
        list[str]
            - List will contain all features (column names) that contains one/all substrings found in keywords.
            - List will be sorted in alphabetical order.

        Examples
        --------
        >>> colnames = ['id', 'name', 'nameType', 'subSpeciesName', 'title']
        >>> cb.featureSearch(['name'], colnames) 
        ['name', 'nameType']
        >>> cb.featureSearch(['Name'], colnames)
        ['subSpeciesName']
        >>> cb.featureSearch(['name', 'Name'], colnames)
        ['name', 'nameType', 'subSpeciesName']
        """

        ##implement INTERSECTION mode later
        def search(keywords, colnames):
            suggested_colnames = set()
            for colname in colnames:
                for keyword in keywords:
                    if keyword in colname:
                        suggested_colnames.add(colname)
            return sorted(list(suggested_colnames))


        if type(keywords) is not list:
            raise Exception('keywords argument expects a list')
        if mode is 'UNION':
            if all_colnames is None:
                return search(keywords, self.all_colnames)
            else:
                return search(keywords, all_colnames)
        elif mode is "INTERSECTION":
            print('to implement later')


        
    
    def tableSearch(self, keywords, csvname_to_colnames_list=None, mode='UNION'):
        """ Find the tables that contain the keywords.

        - Find tables that contain column names which have the substrings specified in keywords. 
        - Note: This search is case sensitive!

        Parameters
        ----------
        keywords : list[str]
            - List of key words that the user is interested in
        csvname_to_colnames_list : dict[str] = list
            - Dictionary that maps a string (table name) to a list of column names it contains.
            - If no argument is provided, this function will use the dictionary generated when the run method was called.
        mode : str
            - If mode is UNION, then return all tables that contain at least one keyword.
            - If mode is INTERSECTION, then return all tables that contain all the keywords.

        Returns
        --------
        list[str]
            - List will contain all tables that contain a match with keywords.
            - List will be sorted in alphabetical order.

        Examples
        --------
        >>> csvname_to_colnames_list = {'table1': ['colName1', 'colName2'], 'table2':['colName3', 'colName4']}
        >>> cb.tableSearch(['colName1'], csvname_to_colnames_list) 
        ['table1']
        >>> cb.tableSearch(['colName3'], csvname_to_colnames_list)
        ['table2']
        >>> cb.tableSearch(['colName1', 'colName2'], csvname_to_colnames_list)
        ['table1', 'table2']
        """
        
        def columnNamesContainKeyword(keyword, colname_list):
            return any(keyword in colname for colname in colname_list)
        
        if mode is 'UNION':
            if csvname_to_colnames_list is None:
                return list(filter(lambda x: x is not None, [key if False not in [True if any(keyword in colname for colname in self.csvname_to_colnames_list[key]) else False for keyword in keywords] else None for key in self.csvname_to_colnames_list]))
            else:
                return list(filter(lambda x: x is not None, [key if False not in [True if any(keyword in colname for colname in csvname_to_colnames_list[key]) else False for keyword in keywords] else None for key in csvname_to_colnames_list]))
        elif mode is 'INTERSECTION':
            csv_matches = []
            if csvname_to_colnames_list is None:
                for csvname in self.csvname_to_colnames_list:
                    keyword_checklist = []
                    for keyword in keywords:
                        keyword_checklist.append(columnNamesContainKeyword(keyword, self.csvname_to_colnames_list[csvname]))
                    if False not in keyword_checklist:
                        csv_matches.append(csvname)
                return sorted(csv_matches)
            else:
                print("implement later")

        
    def openTable(self, rel_dir, indices=[0], encoding='utf-8'):
        """ Open the csv that is referenced by the given relative directory.

        Parameters
        ----------
        rel_dir : str
            - A path to the table that is relative to where the user is running Crystal Ball.
        indices : list[int]
            - Sets the (multi)index by columns represented by their numerical integer-locations.

        Returns
        --------
        DataFrame
            - The DataFrame containing the contents of the csv.
        
        Examples
        --------
        (link juptyer notebook)
        """
        df = pd.read_csv(rel_dir, engine='python', encoding=encoding , error_bad_lines=False)
        df.set_index(list(df.columns[indices]), inplace=True)
        return df
        
        
    def subTable(self, supertable, chosen_index:list, chosen_columns:list):
        """ Create a subtable from a supertable.

        Parameters
        ----------
        supertable : DataFrame
            - Table from which to select chosen_columns from in order to form a subtable
        chosen_index : list[str]
            - The column names that will form the new (multi)index for the subtable.
        chosen_columns : list[str]
            - The column names that will form the new columns for the subtable.

        Returns
        --------
        DataFrame
            - DataFrame (the newly-formed subtable) that will have the (multi)index and columns specified in the arguments.

        Examples
        --------
        (link juptyer notebook)
        """

        combined = chosen_index.copy()
        combined.extend(chosen_columns)
        subtable = supertable[combined].set_index(primary_keys)
        return subtable
        
        
    def mergeTables(self, tables:list):
        """ Sequentially merge a list of tables that all share a common index.

        - Merge defaults to using inner joins over the index.

        Parameters
        ----------
        tables : list[DataFrame]
            - Contains a list of DataFrames that will be merged sequentially.

        Returns
        --------
        DataFrame
            - Table that results from sequentially merging the DataFrames given in the argument.

        Examples
        --------
        (link juptyer notebook)
        """
        # TO IMPLEMENT LATER: other types of joins, merging by non-index
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
        current_merge.index.name = tables[0].index.name
        # CHECK FOR MULTI INDEX CASE, WHETHER THE ABOVE LINE BREAKS
        return current_merge
    
    
    def analyzeRelationships(self, to_analyze:list, visualize=True):
        """ Analyze basic stats of one or more different indexes.

        By comparing boxplots, you should be able to determine which indices are related.

        Parameters
        ----------
        to_analyze : list[list[str, Series]]
            - A list of lists. The later should be of length two, in which the 0th index stores the table name and the 1st index contains a Series.
            - The Series should contain the values of the column derived from the table associated with the name stored in the 0th index.

        Returns
        --------
        DataFrame
            - Table that contains basic stats about each given Series.

        Examples
        --------
        (link juptyer notebook)
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
        """ Compare and contrast the difference between two Series.

        By comparing boxplots, you should be able to determine which indices are related.

        Parameters
        ----------
        to_analyze1 : list[str, Series]
            - A list that contains the name of the first table, and the contents of a specifc column from that table as a Series.
        to_analyze2 : list[str, Series]
            - A list that contains the name of the second table, and the contents of a specifc column from that table as a Series.

        Returns
        --------
        DataFrame
            - Table that contains basic stats about each given Series, as well as a third column that contains the difference between the stats.

        Examples
        --------
        (link juptyer notebook)
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
        
        diff_description = abs(description1 - description2)
        diff_description.name = "Difference"
        descriptions.append(diff_description)
        description_table = pd.concat(descriptions, axis=1)
        return description_table

    
    def export(self, df_to_export, write_to, export_type="CSV"):
        """ Exports contents of dataframe to relative location specified by write_to parameter.

        - Default export type is CSV

        Parameters
        ----------
        df_to_export : DataFrame
            - DataFrame whose contents will be exported into a specifed location.
        write_to : str
            - Relative location (including file) that you will write into.
        export_type : str
            - Format that contents of df_to_export will be exported as.

        Returns
        --------
        None

        Examples
        --------
        (link juptyer notebook)
        """

        if export_type is "CSV":
            df_to_export.to_csv(write_to, encoding='utf-8', index=True, index_label=df_to_export.index.name)
        else:
            print('implemnt sql format')
        
    


# to implement later
# featureSearch should return a dictionary, where key is the index and value is the name of the feature
# this makes it easier for people to select the feature they want
# search function should also have an 'is_exact' option, to make search more precise.
#   check if a lower case letter surrounds either side of the keyword, implies that it is an interjection
# create a function that let's you index into a python list with another list. useful for selecting many names at once 
# from featureSearch result


