class LogousRFMUtils:
    def __init__(self, dataframe_X):
        self.dataframe_X = dataframe_X

    def rfm_featured_data(self):
        data = self.dataframe_X.copy()
        data_RFM = data.groupby('MUSTERI').agg(
            {'KONTOR_TARIHI': lambda y: (data['KONTOR_TARIHI'].max().date() - y.max().date()).days,
             ' TIP': lambda y: len(y.unique()),
             'YAKILAN_KONTOR': lambda y: round(y.mean(), 2)})
        data_RFM.columns = ['recency', 'frequency', 'monetary']
        return data_RFM
