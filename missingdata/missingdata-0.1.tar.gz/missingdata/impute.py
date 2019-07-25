"""Module for imputation methods. """

from sklearn.impute import SimpleImputer

class Imputer(SimpleImputer):
    """Imputer class

    Could used independently as well as part of a sklearn pipeline.
    """

