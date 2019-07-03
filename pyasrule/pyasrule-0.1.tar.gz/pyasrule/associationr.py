import pandas as pd 
import numpy as np 
from scipy.stats import entropy

class AssociationRules:
    def __init__(self, metrics = ["confidence", "lift", "information_gain", "jaccard", "cosine"],\
                 min_antecedent_support = 0.0, min_consequent_support = 0.0, \
                 min_confidence = 0.0):
        
        self.total_num_transactions = None
        self.market_basket_df = None
        self.metrics = metrics
    
    def jaccard(self, support_both, support_antecedent, support_consequent):
        return support_both / (support_antecedent + support_consequent - support_both)
        
    def informationGain(self, support_both, support_antecedent, support_consequent):
        # antecedent -> consequent
        true_true = support_both
        true_false = support_antecedent - support_both
        false_true = support_consequent - support_both
        false_false = self.total_num_transactions - support_antecedent - support_consequent \
        + support_both

        # sum over all entropy

        left = entropy([true_true + true_false, false_true + false_false], base = 2)
        middle = entropy([true_true + false_true, false_false + true_false], base = 2)
        right = entropy([true_true, true_false, false_true, false_false], base = 2)

        return left + middle - right
    
    def cosine(self, support_both, support_antecedent, support_consequent):
        return support_both / (np.sqrt(support_antecedent) * np.sqrt(support_consequent))
    
    def lift(self, support_both, support_antecedent, support_consequent):
        return (support_both * self.total_num_transactions) / \
        (support_antecedent * support_consequent)
    
    def confidence(self, support_both, support_antecedent):
        return support_both / support_antecedent
    
    def generateRules(self, transaction_df, item_col = "Item", transaction_id = "Transaction"):
        # choosen unique transaction

        transaction_df = transaction_df[[transaction_id, item_col]].drop_duplicates() # .reset_index(drop = True)

        # calculating the number of transaction occurs

        self.total_num_transactions = len(transaction_df[transaction_id].unique())
        
        # unique item
        # unique_item = transaction_df.copy()[[item_col]].drop_duplicates().reset_index(drop = True)

        # support 

        support_per_item = transaction_df.copy()\
        .groupby(item_col, as_index = False).count()
        support_per_item.rename(columns = {transaction_id: "Support_Item"}, inplace = True)

        # support_both

        support_both = transaction_df.copy().rename(columns = {item_col: "Antecedent"})\
        .merge(transaction_df.copy().rename(columns = {item_col : "Consequent"}), how = "inner")\
        .sort_values(by = transaction_id).reset_index(drop = True)

        support_both = support_both.loc[support_both["Antecedent"] != support_both["Consequent"]]

        support_both = support_both.groupby(["Antecedent", "Consequent"], as_index = False).count().\
        rename(columns = {transaction_id: "Support_Both"})

        # combining all of the transaction df

        self.market_basket_df = \
        support_both.merge(\
        support_per_item.rename(columns = {item_col : "Antecedent",\
                                           "Support_Item" : "Support_Antecedent"}), \
        how = "inner").merge(\
        support_per_item.rename(columns = {item_col : "Consequent", \
                                          "Support_Item" : "Support_Consequent"}), \
        how = "inner")
        
        # adding some metrics
        
        for metric in self.metrics:
            if metric == "information_gain":
                self.market_basket_df["Information_Gain"] = self.market_basket_df.apply(lambda x:\
                                                              self.informationGain(\
                                                              x["Support_Both"], \
                                                              x["Support_Antecedent"], 
                                                              x["Support_Consequent"]), axis = 1)
            elif metric == "jaccard":
                self.market_basket_df["Jaccard"] = self.market_basket_df.apply(lambda x: self.jaccard(\
                                                              x["Support_Both"], \
                                                              x["Support_Antecedent"], 
                                                              x["Support_Consequent"]), axis = 1)
            elif metric == "cosine":
                self.market_basket_df["Cosine"] = self.market_basket_df.apply(lambda x: self.cosine(\
                                                              x["Support_Both"], \
                                                              x["Support_Antecedent"], 
                                                              x["Support_Consequent"]), axis = 1)
            elif metric == "lift":
                self.market_basket_df["Lift"] = self.market_basket_df.apply(lambda x: self.lift(\
                                                              x["Support_Both"], \
                                                              x["Support_Antecedent"], 
                                                              x["Support_Consequent"]), axis = 1)
            elif metric == "confidence":
                self.market_basket_df["Confidence"] = self.market_basket_df.apply(lambda x:\
                                                              self.confidence(\
                                                              x["Support_Both"], \
                                                              x["Support_Antecedent"]), axis = 1)
        self.market_basket_df.reset_index(drop = True, inplace = True)
