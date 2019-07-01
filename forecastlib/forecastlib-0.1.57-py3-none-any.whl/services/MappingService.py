# Intro camaign distance num zrusit
# new_splah prehazet - OK
#intro campaigndistamce dat na max+1
#campaign distance gap na 0 kde je to zaporny - OK
# prihodit poradi kampane v roce
#layout-density_num_m zabit - OK




import itertools
import json

import pandas as pd
import numpy as np

from forecastlib.libs.MappingHelper import MappingHelper
from scipy.interpolate import CubicSpline

intents_dict = {
    None: 0,
    "Complimentary Product": 1,
    "Star Product": 2,
    "Units Generator": 3,
    "Anchor": 4,
    "Excitement Creator": 5,
}




class MappingService(object):
    def __init__(self, mapping_json, history: pd.DataFrame, intents: pd.DataFrame):

        self.cols = {
            'PROD_ID': "number",
            'CHAN_CD': "number",
            'CATEGORY_CD': "str",
            'SECTOR_CD': "str",
            'SEGMENT_CD': "str",
            'CONCEPT_CD': "str",
            'CAMPAIGN_CD': "number",
            'CAMPAIGN_INDEX': "number",
            'CAMPAIGN_LENGTH': "number",
            'OFFER_CODE': "str",
            'OFFER_GROUP': "str",
            'OFFER_PERC': "interval",
            'OFFER_PRICE': "interval",
            'UNITS_ACTUAL': "number",
            'UPA_ACTUAL': "number",
            'INTRO_CAMPAIGN_DISTANCE': "number",
            'NEW_SPLASH': "str",
            'SCRATCH_N_SNIFF': "str",
            'VISUAL_FOCUS': "str",
            'CONDITION_FOR_OTHER': "str",
            'LAYOUT_DENSITY': "str",
            'OFFER_DENSITY': "str",
            'OFFER_DENSITY_NUM': "interval",
            'KEY_OFFER_GROUP': "str",
            'KEY_SECTION_GROUP': "str",
            'IS_OUTLIER': "number"
        }

        self.map = mapping_json
        self.history = history
        self.history["PROD_ID"] = self.history["PROD_ID"].astype(np.int64)
        self.history["CHAN_CD"] = self.history["CHAN_CD"].astype(str)
        self.history["OFFER_PERC_M"] = self.history["OFFER_PERC_M"].astype(np.int64)
        self.history["AVG_UPA"] = self.history["AVG_UPA"].astype(float)

        self.intents = intents

        self.map_helper = MappingHelper()

        self.inverted_map = {}

        for c in self.map.keys():
            if self.cols[c] == "interval":
                d = dict((self.map_helper.try_interval(v), k) for k, v in self.map[c].items())
            else:
                d = dict((v, k) for k, v in self.map[c].items())
            self.inverted_map[c] = d

    def from_json(self, input_data) -> pd.DataFrame:
        df = pd.DataFrame.from_records(input_data)
        return df

    def to_json(self, output_data: pd.DataFrame) -> json:
        return output_data.to_json(orient='index')

    def apply_mapping(self, original_data: pd.DataFrame) -> pd.DataFrame:
        df = original_data.copy()
        for c in self.map.keys():
            if c in df.keys():
                if self.cols[c] == "interval":
                    df[c+"_M"] = self.map_helper.map_interval(df[c], self.inverted_map[c])
                else:
                    df[c+"_M"] = df[c].map(self.inverted_map[c])

                df[c+"_M"] = df[c+"_M"].astype('int32')

        return df

    def remove_mapping(self, mapped_data: pd.DataFrame) -> pd.DataFrame:
        for c in self.map.keys():
            if c in mapped_data.keys():
                mapped_data[c] = mapped_data[c].replace(self.inverted_map[c])

        return mapped_data

    def merge_history(self, df: pd.DataFrame):
        df["PROD_ID"] = df["PROD_ID"].astype(np.int64)
        df["CHAN_CD"] = df["CHAN_CD"].astype(str)
        df["OFFER_PERC_M"] = df["OFFER_PERC_M"].astype(np.int64)


        if 'CHAN_CD' in self.history.columns:
            df = df.merge(self.history[["PROD_ID", "CHAN_CD", "OFFER_PERC_M", "AVG_UPA"]], how="left", on=["PROD_ID", "CHAN_CD", "OFFER_PERC_M"])
        else:
            df = df.merge(self.history[["PROD_ID", "OFFER_PERC_M", "AVG_UPA"]], how="left", on=["PROD_ID", "OFFER_PERC_M"])

        #df['AVG_UPA'] = np.where(df["AVG_UPA"].isnull(), -1, df["AVG_UPA"])
        #df['AVG_UPA'] = df['AVG_UPA_FULL']
        #df['AVG_UPA'] = np.where(df["AVG_UPA_FULL"].isnull(), -1, df["AVG_UPA_FULL"])
        df['WITH_HISTORY'] = np.where(df["AVG_UPA"].notnull(), 1, 0)

        return df

    def merge_intents(self, df: pd.DataFrame):
        return MappingService.add_intent(df, self.intents)

    def apply(self, df: pd.DataFrame):
        mapped = self.apply_mapping(df)
        enriched = MappingService.enrich(mapped)
        with_history = self.merge_history(enriched)
        with_intent = self.merge_intents(with_history)

        return with_intent

    @staticmethod
    def map(df: pd.DataFrame):
        # backup original values

        ## Convert columns to category data type and map to integers. Save the mapping into mappings dictionary.
        mappings = {}
        for col in ['PROD_ID', 'CHAN_CD', 'CATEGORY_CD', 'SECTOR_CD', 'CAMPAIGN_CD', 'CAMPAIGN_LENGTH',
                    'SEGMENT_CD', 'CONCEPT_CD', 'CAMPAIGN_LENGTH', 'OFFER_CODE', 'OFFER_GROUP',
                    'SCRATCH_N_SNIFF', 'VISUAL_FOCUS', 'CONDITION_FOR_OTHER', 'LAYOUT_DENSITY', 'OFFER_DENSITY', 'KEY_OFFER_GROUP', 'KEY_SECTION_GROUP']:
            df[col+"_M"] = df[col].astype('category')
            mappings[col] = dict(zip(df[col+"_M"].cat.codes, df[col+"_M"]))
            df[col+"_M"] = df[col+"_M"].cat.codes

        df['OFFER_PERC_M'] = pd.cut(df['OFFER_PERC'], bins=MappingService.get_perc_bins())
        df['OFFER_PRICE_M'] = pd.cut(df['OFFER_PRICE'], bins=MappingService.get_price_bins())
        df['OFFER_DENSITY_NUM_M'] = pd.cut(df['OFFER_DENSITY_NUM'], bins=MappingService.get_offer_density_bins())

        for col in ['OFFER_PERC', 'OFFER_PRICE', 'OFFER_DENSITY_NUM']:
            mappings[col] = dict(zip(df[col+"_M"].cat.codes, df[col+"_M"]))
            df[col+"_M"] = df[col+"_M"].cat.codes


        # Manual order of NEW_SPLASH
        new_splash_type = pd.CategoricalDtype(categories=["N-0", "N-N2", "N-N"], ordered=True)
        df["NEW_SPLASH_M"] = df["NEW_SPLASH"].astype(new_splash_type)
        mappings["NEW_SPLASH"] = dict(zip(df["NEW_SPLASH_M"].cat.codes, df["NEW_SPLASH_M"]))
        df["NEW_SPLASH_M"] = df["NEW_SPLASH_M"].cat.codes


        return df, mappings

    @staticmethod
    def enrich(df: pd.DataFrame):
        temp = df['CAMPAIGN_CD'].astype(str)
        df['YEAR'] = temp.str[:4].astype(np.int64)
        df['MONTH'] = temp.str[4:].astype(np.int64)  # temporary placeholder, will be overwritten
        df['CAMPAIGN_DAY_END'] = (
                    (df['MONTH'] - 1) * 21 + 28)  # represents number of days since the beginning of the year
        df['CAMPAIGN_DAY_END'] = pd.to_datetime(df['YEAR'] * 1000 + df['CAMPAIGN_DAY_END'], format='%Y%j')
        df['CAMPAIGN_DAY_START'] = df['CAMPAIGN_DAY_END'] - pd.to_timedelta(df['CAMPAIGN_LENGTH'], unit='d')

        df['MONTH'] = df['CAMPAIGN_DAY_START'].dt.month.astype(np.int8)
        df['YEAR'] = df['YEAR'].astype(np.int16)
        df['WEEK'] = df['CAMPAIGN_DAY_START'].dt.week.astype(np.int8)

        df['CAMPAIGN_ID'] = df['CHAN_CD'].map(str) + df['CAMPAIGN_CD'].map(str)

        df['CAMPAIGN_IN_YEAR'] = df['CAMPAIGN_CD'].mod(df['YEAR'].astype(int) * 100)

        df["UPA_PER_CAMPAIGN"] = df["UPA_ACTUAL"].map(float) * 20 / df["CAMPAIGN_LENGTH"].map(float)
        df["OFFER_PRICE_ORIGINAL"] = np.where(df["OFFER_PERC"] > 0, df["OFFER_PRICE"] * 100 / (df["OFFER_PERC"]), df["OFFER_PRICE"])

        df['OFFER_PRICE_ORIGINAL'] = pd.cut(df['OFFER_PRICE_ORIGINAL'], bins=MappingService.get_price_bins())
        df['OFFER_DENSITY_NUM_ZERO'] = np.where(df['OFFER_DENSITY_NUM'] == 0, 0, 1).astype(np.int8)
        print("Change categories")

        ## Create a new column with a count of products within the same discount group and catalogue.
        temp = df.groupby(by=['OFFER_PERC_M', 'CAMPAIGN_ID']).count()[['PROD_ID_M']].to_dict()
        mapping_products_discount = {}
        for k, v in temp['PROD_ID_M'].items():
            mapping_products_discount[k] = v
        df['PRODUCTS_DISCOUNT_COUNT'] = list(zip(df['OFFER_PERC_M'], df['CAMPAIGN_ID']))
        df['PRODUCTS_DISCOUNT_COUNT'] = df['PRODUCTS_DISCOUNT_COUNT'].map(mapping_products_discount)
        print("PRODUCTS_DISCOUNT_COUNT")

        ## Create a new column with a count of products within the same price group and catalogue.
        temp = df.groupby(by=['OFFER_PRICE_M', 'CAMPAIGN_ID']).count()[['PROD_ID_M']].to_dict()
        mapping_products_price = {}
        for k, v in temp['PROD_ID_M'].items():
            mapping_products_price[k] = v
        df['PRODUCTS_PRICE_COUNT'] = list(zip(df['OFFER_PRICE_M'], df['CAMPAIGN_ID']))
        df['PRODUCTS_PRICE_COUNT'] = df['PRODUCTS_PRICE_COUNT'].map(mapping_products_price)
        print("PRODUCTS_PRICE_COUNT")

        ## Create five lags of discount, price, and number of active consultants and columns describing the gap between the current and lagged value in weeeks.
        for col in ['OFFER_PERC_M', 'OFFER_PRICE_M']:
            for i in range(1, 5):
                temp = df.groupby(by=['PROD_ID_M', 'CHAN_CD_M'])[col].shift(i).rename(col + '_LAG_' + str(i))
                df = pd.concat([df, temp], axis=1)
                temp = df.groupby(by=['PROD_ID_M', 'CHAN_CD_M'])['CAMPAIGN_DAY_START'].shift(i).rename(
                    col + '_LAG_' + str(i) + '_WEEKS_AGO')
                df = pd.concat([df, temp], axis=1)
                df[col + '_LAG_' + str(i) + '_WEEKS_AGO'] = round(
                    (df['CAMPAIGN_DAY_START'] - df[col + '_LAG_' + str(i) + '_WEEKS_AGO']).dt.days / 7)
                df[col + '_LAG_' + str(i)] = np.where(df[col + '_LAG_' + str(i)].isnull(), 0,
                                                      df[col + '_LAG_' + str(i)])
                df[col + '_LAG_' + str(i) + '_WEEKS_AGO'] = np.where(df[col + '_LAG_' + str(i) + '_WEEKS_AGO'].isnull(),
                                                                     0, df[col + '_LAG_' + str(i) + '_WEEKS_AGO'])
        print("LAGS")

        ## Count of unique products per category, sector, and segment within a single issue of catalogue.
        for col in ['CATEGORY_CD_M', 'SECTOR_CD_M', 'SEGMENT_CD_M']:
            temp = df.groupby(by=[col, 'CAMPAIGN_ID']).count()[['PROD_ID_M']].to_dict()
            mapping = {}
            for k, v in temp['PROD_ID_M'].items():
                mapping[k] = v
            df['COUNT_PRODUCTS_' + col.replace('_CD', '')] = list(zip(df[col], df['CAMPAIGN_ID']))
            df['COUNT_PRODUCTS_' + col.replace('_CD', '')] = df['COUNT_PRODUCTS_' + col.replace('_CD', '')].map(mapping)

        print("Uniques")

        ## Count total products in each campaign
        products_in_campaign = df.groupby(by=['CAMPAIGN_ID']).count()[["PROD_ID_M"]]
        mapping = {}
        for k, v in products_in_campaign['PROD_ID_M'].items():
            mapping[k] = v
        df['PRODUCTS_IN_CAMPAIGN'] = df['CAMPAIGN_ID']
        df['PRODUCTS_IN_CAMPAIGN'] = df['PRODUCTS_IN_CAMPAIGN'].map(mapping)
        print("TOTALS")

        ## Count total products in each offer discount category
        for i in range(0, MappingService.get_perc_bins().__len__()):
            items = df[df['OFFER_PERC_M'] == i]
            bycampaign = items.groupby(by=['CAMPAIGN_ID']).count()[["PROD_ID_M"]]

            mapping = {}
            for k, v in bycampaign['PROD_ID_M'].items():
                prods = np.average(df[df['CAMPAIGN_ID'] == k]['PRODUCTS_IN_CAMPAIGN'])

                mapping[k] = 0 if prods == 0 else v / prods
            df['PRODUCTS_WITH_PERC_' + str(i)] = df['CAMPAIGN_ID']
            df['PRODUCTS_WITH_PERC_' + str(i)] = df['PRODUCTS_WITH_PERC_' + str(i)].map(mapping)
            df['PRODUCTS_WITH_PERC_' + str(i)] = np.where(df['PRODUCTS_WITH_PERC_' + str(i)].isnull(), 0,
                                                          df['PRODUCTS_WITH_PERC_' + str(i)])  # remove NaNs
        print("Discount categories")


        # Remover 500 from Intro_capaign_distance
        s = df["INTRO_CAMPAIGN_DISTANCE"]
        max_campaign_distance = s[s < 500].max()
        df["INTRO_CAMPAIGN_DISTANCE_M"] = np.where(df["INTRO_CAMPAIGN_DISTANCE"] == 500, max_campaign_distance + 1,
                                                   df["INTRO_CAMPAIGN_DISTANCE"])

        ## Count gaps in campaigns
        temp = df.groupby(by=['PROD_ID_M', 'CHAN_CD_M'])
        col = temp['INTRO_CAMPAIGN_DISTANCE_M'].shift(1).rename('PREV_INTRO_CAMPAIGN_DISTANCE')
        df = pd.concat([df, col], axis=1)
        df['LAST_CAMPAIGN_GAP'] = df['INTRO_CAMPAIGN_DISTANCE_M'] - df['PREV_INTRO_CAMPAIGN_DISTANCE'] - 1

        df['LAST_CAMPAIGN_GAP'] = np.where(df['LAST_CAMPAIGN_GAP'].isnull(), 0, df['LAST_CAMPAIGN_GAP'])
        df['LAST_CAMPAIGN_GAP'] = np.where(df['LAST_CAMPAIGN_GAP'] < 0, 0, df['LAST_CAMPAIGN_GAP'])
        df['PREV_INTRO_CAMPAIGN_DISTANCE'] = np.where(df['PREV_INTRO_CAMPAIGN_DISTANCE'].isnull(), 0, df['PREV_INTRO_CAMPAIGN_DISTANCE'])


        print("GAPS")

        ## Actives count increase since last campaign
        actives = df.groupby(by=['CAMPAIGN_ID'])['ACTIVE_CONSULTANTS'].mean().shift(1).rename(
            'ACTIVE_CONSULTANTS_LAG_1')
        mapping = {}
        for k, v in actives.items():
            mapping[k] = v
        df['ACTIVE_CONSULTANTS_LAG_1'] = df['CAMPAIGN_ID']
        df['ACTIVE_CONSULTANTS_LAG_1'] = df['ACTIVE_CONSULTANTS_LAG_1'].map(mapping)
        df['ACTIVE_CONSULTANTS_LAG_1'] = np.where(df['ACTIVE_CONSULTANTS_LAG_1'].isnull(), df['ACTIVE_CONSULTANTS'],
                                                  df['ACTIVE_CONSULTANTS_LAG_1'])
        print(df.dtypes)

        df['ACTIVE_CONSULTANTS_DIFF'] = df['ACTIVE_CONSULTANTS'].map(float) / df['ACTIVE_CONSULTANTS_LAG_1'].map(float)

        return df

    @staticmethod
    def add_full_history(df: pd.DataFrame):
        nolaunch = df[df.INTRO_CAMPAIGN_DISTANCE > 0]

        #first = nolaunch[["PROD_ID", "CHAN_CD", "OFFER_PERC_M", "UPA_ACTUAL"]].groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])

        #first = first.first()
        #first = first.reset_index()

        no_last_year = nolaunch[nolaunch["YEAR"] < 2018]

        cumsum = no_last_year.groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])['UPA_ACTUAL'].cumsum()
        cumcount = no_last_year.groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])['UPA_ACTUAL'].cumcount()

        #df = df.merge(first, on=["PROD_ID", "CHAN_CD", "OFFER_PERC_M"], how="left", suffixes=("", "_FIRST"))

        df['CUMSUM'] = cumsum - nolaunch['UPA_ACTUAL']
        df['CUMSUM_WITH_FIRST'] = cumsum
        df['CUMCOUNT'] = cumcount
        df['AVG_UPA'] = df['CUMSUM'] / df['CUMCOUNT']
        #df['AVG_UPA_1'] = cumsum / (df['CUMCOUNT'] + 1)
        #df['AVG_UPA_2'] = (cumsum - df["UPA_ACTUAL_FIRST"]) / df['CUMCOUNT']

        #df['AVG_UPA_2'] = np.where(df['AVG_UPA_2'] < 0, df["UPA_ACTUAL"], df['AVG_UPA_2'])

        # Propagate last known AVG_UPA
        df['AVG_UPA'] = df.groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])['AVG_UPA'].fillna(method='ffill')
        #df['AVG_UPA_1'] = df.groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])['AVG_UPA_1'].fillna(method='ffill')
        #df['AVG_UPA_2'] = df.groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])['AVG_UPA_2'].fillna(method='ffill')

        df['WITH_HISTORY'] = np.where(df["AVG_UPA"].notnull(), 1, 0)
        #df['WITH_HISTORY_1'] = np.where(df["AVG_UPA_1"].notnull(), 1, 0)
        #df['WITH_HISTORY_2'] = np.where(df["AVG_UPA_2"].notnull(), 1, 0)
        df['CUMSUM'] = np.where(df["CUMSUM"].isnull(), 0, df["CUMSUM"])
        df['CUMCOUNT'] = np.where(df["CUMCOUNT"].isnull(), 0, df["CUMCOUNT"])


        return df

    @staticmethod
    def get_last_history(df: pd.DataFrame) -> pd.DataFrame:
        last = df[["PROD_ID", "CHAN_CD", "OFFER_PERC_M", "AVG_UPA"]].groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M'])

        last = last.last()
        last = last.reset_index()

        return last

    @staticmethod
    def get_history(df: pd.DataFrame) -> pd.DataFrame:
        # Ignore first campaign
        known = df[df.INTRO_CAMPAIGN_DISTANCE > 0]

        # Add avg_upa column per discount group
        history = known.groupby(by=['PROD_ID', 'CHAN_CD', 'OFFER_PERC_M',  "CHAN_CD"])['UPA_ACTUAL'].mean()
        history = history.reset_index()
        history.rename(columns={'UPA_ACTUAL':'AVG_UPA'}, inplace=True)

        #return history
        # Calculate missing AVG_UPAs
        history["SAMPLES"] = history.groupby(["PROD_ID"])["PROD_ID"].transform("count")
        products = df[["CHAN_CD", "PROD_ID"]].unique()
        product_list = list(itertools.product(products, range(0, 10)))
        product_discount_matrix = pd.DataFrame(data=product_list, columns=["PROD_ID",  "CHAN_CD", "OFFER_PERC_M"])

        with_history = product_discount_matrix.merge(history, how="left", on=["PROD_ID",  "CHAN_CD", "OFFER_PERC_M"])


#        # calculate reference UPA for each discount category
#        avg_upas = with_history.groupby( "CHAN_CD", "OFFER_PERC_M")["AVG_UPA"].mean()

        # get avg upa polynom
        #poly = CubicSpline(range(0, 10), avg_upas)

        #avg_discount_category = with_history[with_history["AVG_UPA"].notnull()].groupby("PROD_ID")["OFFER_PERC_M"].mean()
        #pivoted = with_history[["PROD_ID", "OFFER_PERC_M",  "CHAN_CD",  "AVG_UPA"]].pivot(index="PROD_ID", columns="OFFER_PERC_M", values="AVG_UPA")

        #summary = pivoted[[]]  # get just indices
        #summary["AVG_UPA"] = pivoted[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]].mean(axis=1)
        #summary = summary.join(avg_discount_category, how="left", rsuffix="_AVG")
        #summary["REF_UPA"] = [poly(x) for x in summary["OFFER_PERC_M"]]
        #summary["REF_MULTIPLIER"] = summary["AVG_UPA"] / summary["REF_UPA"]

        #with_history = with_history.join(avg_upas, how="left", on="OFFER_PERC_M", rsuffix="_REF")
        #with_history = with_history.join(summary[["REF_MULTIPLIER"]], how="left", on="PROD_ID")

        #with_history["AVG_UPA_CALC"] = with_history["AVG_UPA_REF"] * with_history["REF_MULTIPLIER"]
        #with_history["AVG_UPA_FULL"] = np.where(with_history["AVG_UPA"].notnull(), with_history["AVG_UPA"], with_history["AVG_UPA_CALC"])

        return with_history

    @staticmethod
    def get_intent(file: str, region: str) -> pd.DataFrame:
        intents = pd.read_excel(file)
        intents["INTENT"] = intents[region].map(intents_dict)

        intents = intents.rename(columns={"Code": "PROD_ID"})

        return intents

    @staticmethod
    def add_intent(df: pd.DataFrame, intents: pd.DataFrame):
        df = pd.merge(df, intents[["PROD_ID", "INTENT"]], how="left", on=["PROD_ID"])
        df["INTENT"] = np.where(df["INTENT"].isnull(), 0, df["INTENT"])

        return df

    @staticmethod
    def get_price_per_bp(file: str) -> pd.DataFrame:
        bps = pd.read_csv(file, sep=',')
        return bps

    @staticmethod
    def add_price_per_bp(df: pd.DataFrame, bps: pd.DataFrame):
        ppbp = pd.merge(df[["PROD_ID", "OFFER_PRICE", "OFFER_PERC"]], bps, how="left", on=["PROD_ID"])

        ppbp["OFFER_PRICE_ORIGINAL"] = np.where(ppbp["OFFER_PERC"] == 0, ppbp["OFFER_PRICE"],  ppbp["OFFER_PRICE"] * 100.0 / ppbp["OFFER_PERC"])
        df["PRICE_PER_BP"] = ppbp["BP"] / ppbp["OFFER_PRICE_ORIGINAL"]
        df["PRICE_PER_BV"] = ppbp["BV"] / ppbp["OFFER_PRICE_ORIGINAL"]

        return df

    @staticmethod
    def get_perc_bins():
        perc_bins = [x for x in range(0, 120, 10)]
        ## Put zeros into a separate bin (-1,0], otherwise they would end up as NaNs.
        perc_bins = [-1] + perc_bins

        return perc_bins

    @staticmethod
    def get_price_bins():
        price_bins = [x for x in range(0, 120, 20)]
        price_bins += [x for x in range(150, 550, 50)]
        price_bins += [x for x in range(600, 1800, 200)]
        price_bins += [x for x in range(2000, 3600, 400)]
        ## Put zeros into a separate bin (-1,0], otherwise they would end up as NaNs.
        price_bins = [-1] + price_bins

        return price_bins

    @staticmethod
    def get_layout_density_bins():
        layout_density_bins = [x for x in range(0, 10, 1)]
        layout_density_bins += [x for x in range(10, 40, 2)]
        layout_density_bins += [x for x in range(40, 60, 5)]
        layout_density_bins += [x for x in range(60, 220, 20)]
        ## Put zeros into a separate bin (-1,0], otherwise they would end up as NaNs.
        layout_density_bins = [-1] + layout_density_bins

        return layout_density_bins

    @staticmethod
    def get_offer_density_bins():
        offer_density_bins = [x for x in range(0, 10, 1)]
        offer_density_bins += [x for x in range(10, 20, 2)]
        offer_density_bins += [x for x in range(20, 40, 5)]
        offer_density_bins += [x for x in range(40, 100, 10)]
        offer_density_bins += [x for x in range(100, 200, 20)]
        ## Put zeros into a separate bin (-1,0], otherwise they would end up as NaNs.
        offer_density_bins = [-1] + offer_density_bins

        return offer_density_bins
