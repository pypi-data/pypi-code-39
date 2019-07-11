class DataBunch:
    def __init__(self, train_dl, valid_dl):
        self.train_dl, self.valid_dl = train_dl, valid_dl